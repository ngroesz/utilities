#!/usr/bin/env python

import argparse
from datetime import datetime
import pandas as pd

default_missing = pd._libs.parsers.STR_NA_VALUES
default_missing.add('\\N')

def parse_options():
  parser = argparse.ArgumentParser('Convert CSV to parquet')
  parser.add_argument('csv_file', help='CSV file')
  parser.add_argument('parquet_file', help='Parquet file')

  return parser.parse_args()


def csv_to_parquet(csv_file, parquet_file):
  print(f'reading {csv_file}')
  df = pd.read_csv(
    csv_file,
    sep=',',
    dtype={
      'tv_market_no': 'int32',
      'network_no': 'int32',
      'mso_no': 'int32',
    },
    converters={
      'is_hidden': lambda x: True if x == 't' else False,
      'from_date': lambda x: None if x == '\\N' else datetime.strptime(x, '%Y-%m-%d').date(),
      'to_date': lambda x: None if x == '\\N' else datetime.strptime(x, '%Y-%m-%d').date()
    }
  )
  with pd.option_context(
    'display.max_rows', 10,
    'display.max_columns', None,
    'display.precision', 3,
  ):
    print(df)


  print(f'writing {parquet_file}')
  df.to_parquet(parquet_file)

if __name__ == '__main__':
  args = parse_options()

  csv_to_parquet(args.csv_file, args.parquet_file)

