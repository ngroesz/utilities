#!/usr/bin/env python

import boto3
import sys

MATCHING_STACK_KEYWORD = 'ngroesz'

session = boto3.Session(region_name='us-west-2')
stack_session = session.client('cloudformation')

# from https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def query_yes_no(question, default='no'):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def search_and_delete_stacks():
    stacks_to_delete = []

    paginator = stack_session.get_paginator('list_stacks')
    response_iterator = paginator.paginate(StackStatusFilter=['CREATE_COMPLETE'])
    for page in response_iterator:
        stacks_to_delete.extend(filter(lambda s: MATCHING_STACK_KEYWORD in s['StackName'], page['StackSummaries']))

    if len(stacks_to_delete) == 0:
        print('No matching stacks found.')
        return

    for stack in stacks_to_delete:
        print('{stack_name} ({stack_id})'.format(stack_name=stack['StackName'], stack_id=stack['StackId']))

    if query_yes_no('Delete ALL of these stacks?'):
        delete_stacks(stacks_to_delete)

def delete_stacks(stacks_to_delete):
    for stack in stacks_to_delete:
       stack_session.delete_stack(StackName=stack['StackId'])

if __name__ == '__main__':
    search_and_delete_stacks()
