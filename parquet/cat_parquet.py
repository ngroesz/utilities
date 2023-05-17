#!/usr/bin/env python

import argparse
import pandas as pd

def parse_options():
  parser = argparse.ArgumentParser('Concatenate parquet')
  parser.add_argument('parquet_file', help='Parquet file')

  return parser.parse_args()


def cat_parquet(parquet_file):
  df = pd.read_parquet(parquet_file)
  with pd.option_context(
    'display.max_rows', 10,
    'display.max_columns', None,
    'display.precision', 3,
  ):
    print(df.dtypes)
    print(df)

if __name__ == '__main__':
  args = parse_options()

  cat_parquet(args.parquet_file)

