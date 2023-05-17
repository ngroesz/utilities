#!/usr/bin/env python

import argparse
import boto3
import sys

from common import search_for_matching_stacks

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


def search_and_delete_stacks(args):
    stacks_to_delete = search_for_matching_stacks(stack_session, args.keyword or MATCHING_STACK_KEYWORD, args.exact)

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
    parser = argparse.ArgumentParser(description='delete some stacks')
    parser.add_argument('--keyword', '-k', help='matching keyword')
    parser.add_argument('--exact', '-x', action='store_true', help='exact ending matches only')

    args = parser.parse_args()

    search_and_delete_stacks(args)
