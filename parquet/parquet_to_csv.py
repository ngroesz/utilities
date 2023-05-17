#!/usr/bin/env python

import argparse
from datetime import datetime
import pandas as pd

default_missing = pd._libs.parsers.STR_NA_VALUES
default_missing.add('\\N')

def parse_options():
  parser = argparse.ArgumentParser('Convert parquet to CSV')
  parser.add_argument('parquet_file', help='Parquet file')
  parser.add_argument('csv_file', help='CSV file')

  return parser.parse_args()


def parquet_to_csv(parquet_file, csv_file):
  print(f'reading {parquet_file}')
  df = pd.read_parquet(parquet_file)

  with pd.option_context(
    'display.max_rows', 10,
    'display.max_columns', None,
    'display.precision', 3,
  ):
    print(df)


  print(f'writing {csv_file}')
  df.to_csv(csv_file)

if __name__ == '__main__':
  args = parse_options()

  parquet_to_csv(args.parquet_file, args.csv_file)

