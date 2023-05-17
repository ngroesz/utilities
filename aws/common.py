import re


def stack_matches(stack_name, search_keyword, exact_match=False):
    # we don't want to delete any frontend stacks
    if re.match('^fe-', stack_name):
        return False

    if exact_match:
        regex = re.escape(search_keyword) + r'$'
        return re.search(regex, stack_name)
    else:
        return search_keyword in stack_name


def search_for_matching_stacks(stack_session, stack_keyword, exact_match=False):
    stacks = []

    paginator = stack_session.get_paginator('list_stacks')
    response_iterator = paginator.paginate(StackStatusFilter=['CREATE_COMPLETE'])
    for page in response_iterator:
        stacks.extend(filter(lambda s: stack_matches(s['StackName'], stack_keyword, exact_match), page['StackSummaries']))

    return stacks
