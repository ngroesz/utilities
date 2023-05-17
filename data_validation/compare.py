#!/usr/bin/env python3

import argparse
from pyspark.sql import SparkSession, SQLContext
import pyspark.sql.functions as F
from functools import reduce
from operator import or_

TOLERANCE_PERCENTAGE = 3

def main():
    args = parse_options()

    join_columns = args.join_columns.split(',')
    compare_columns = args.compare_columns.split(',')

    filters = {}
    for f in args.filters:
        k, v = f.split('=')
        filters[k] = v

    compare_dataframes(join_columns, compare_columns, filters, args.dataset_one_location, args.dataset_two_location, args.output_file)

def parse_options():
    parser = argparse.ArgumentParser('Compare Dataframes')
    parser.add_argument('--join-columns', required=True, help='columns to join by')
    parser.add_argument('--compare-columns', required=True, help='columns to compare')
    parser.add_argument('--filters', action='append', help='filter data by given columns and values')
    parser.add_argument('--output-file', required=False, help='location of file to write comparison dataframe in CSV format')
    parser.add_argument('dataset_one_location', help='location of dataset one')
    parser.add_argument('dataset_two_location', help='location of dataset two')

    return parser.parse_args()

def spark_session():
    return SparkSession.builder \
      .master('local') \
      .appName('ngroesz') \
      .getOrCreate()

def add_filters(dataframe, filters):
    for column, value in filters.items():
        dataframe = dataframe.filter(F.col(column).isin(value))

    return dataframe
            
def compare_dataframes(join_columns, compare_columns, filters, dataset_one_location, dataset_two_location, output_file=None):
    spark = spark_session()
    df_one = spark.read.parquet(dataset_one_location)
    df_two = spark.read.parquet(dataset_two_location)

    df_one_columns = [c for l in (join_columns, [F.col(c).alias(c + '_df_one') for c in compare_columns]) for c in l]
    df_one_renamed = df_one.select(df_one_columns)
    df_one_filtered = add_filters(df_one_renamed, filters)

    df_two_columns = [c for l in (join_columns, [F.col(c).alias(c + '_df_two') for c in compare_columns]) for c in l]
    df_two_renamed = df_two.select(df_two_columns)
    df_two_filtered = add_filters(df_two_renamed, filters)

    joined_df = df_one_filtered.join(
            df_two_filtered,
            join_columns,
            'full_outer'
          )

    calculated_columns = join_columns
    for c in compare_columns:
        calculated_columns.extend([
                F.col(c + '_df_one'),
                F.col(c + '_df_two'),
                F.round(F.abs(F.col(c + '_df_one') - F.col(c + '_df_two')), 2).alias(c + '_difference')
            ])

    calculated_df = joined_df.select(calculated_columns)

    filtered_df = calculated_df.filter(
            reduce(
                or_,
                [F.col(c + '_difference') > F.greatest(F.col(c + '_df_one'), F.col(c + '_df_two')) * (TOLERANCE_PERCENTAGE * .01) for c in compare_columns]
            )
        ).orderBy([F.col(c + '_difference').desc() for c in compare_columns])

    print("DF one count ({})  - DF two count ({}): {}".format(df_one.count(), df_two.count(), df_one.count() - df_two.count()))
    print("Difference count: {}".format(filtered_df.count()))

    if filterd_df.count() > 0:
        filtered_df.show()

    if output_file:
        filtered_df \
            .repartition(1) \
            .write \
            .option('header', True) \
            .csv(output_file)

if __name__ == '__main__':
    main()
