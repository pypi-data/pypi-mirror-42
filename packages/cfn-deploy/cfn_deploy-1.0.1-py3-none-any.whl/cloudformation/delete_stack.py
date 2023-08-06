import sys
import time

import boto3
from botocore.exceptions import ClientError


def main(stack_name):
    """Wait for a cloudformation stack delete to complete.

    Parameters
    ----------
    stack_name : str
        Name of the stack to montior.
    """
    max_attempts = 120
    delay = 30
    num_attempts = 0

    print("Waiting for stack to be deleted...")
    cf = boto3.client('cloudformation')
    cf.delete_stack(StackName=stack_name)
    while True:
        num_attempts += 1
        # query stack status
        try:
            stacks = cf.describe_stacks(StackName=stack_name)['Stacks']
            if len(stacks) == 0:
                print("Delete complete")
        except ClientError as e:
            if e.response['Error']['Message'] != "Stack with id {} does not exist".format(stack_name):  # nopep8
                print("Unexpected error: %s" % e)
            else:
                print("Delete complete")

        if stacks[0]['StackStatus'] == 'DELETE_FAILED':
            print("Failed to delete stack: {}".format(
                stacks[0]['StackStatusReason']))
            raise Exception('Stack deletion failed')
        elif stacks[0]['StackStatus'] == 'DELETE_COMPLETE':
            print("Delete complete")

        sys.stdout.write('.')
        time.sleep(delay)

        if num_attempts >= max_attempts:
            raise Exception('Max attempts exceeded')
