#!/usr/bin/env python

import argparse
import boto3
import sys

from common import search_for_matching_stacks

MATCHING_STACK_KEYWORD = 'ngroesz'

session = boto3.Session(region_name='us-west-2')
stack_session = session.client('cloudformation')

def list_stacks(args):
    stacks = search_for_matching_stacks(stack_session, args.keyword or MATCHING_STACK_KEYWORD, args.exact)

    if len(stacks) == 0:
        print('No matching stacks found.')

    for stack in stacks:
        print('{stack_name} ({stack_id})'.format(stack_name=stack['StackName'], stack_id=stack['StackId']))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='list some stacks')
    parser.add_argument('--keyword', '-k', help='matching keyword')
    parser.add_argument('--exact', '-x', action='store_true', help='exact ending matches only')

    args = parser.parse_args()

    list_stacks(args)
