#!/usr/bin/env python

import boto3
import sys

MATCHING_STACK_KEYWORD = 'ngroesz'

session = boto3.Session(region_name='us-west-2')
stack_session = session.client('cloudformation')

# TODO: common search and list function
def search_and_list_stacks():
    stacks = []

    paginator = stack_session.get_paginator('list_stacks')
    response_iterator = paginator.paginate(StackStatusFilter=['CREATE_COMPLETE'])
    for page in response_iterator:
        stacks.extend(filter(lambda s: MATCHING_STACK_KEYWORD in s['StackName'], page['StackSummaries']))

    if len(stacks) == 0:
        print('No matching stacks found.')
        return

    for stack in stacks:
        print('{stack_name} ({stack_id})'.format(stack_name=stack['StackName'], stack_id=stack['StackId']))

if __name__ == '__main__':
    search_and_list_stacks()
