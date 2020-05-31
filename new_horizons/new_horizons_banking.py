#!/usr/bin/env python3
"""
new_horizons_banking.py
A program to add up our sick money activities
"""

import re
import sys
import argparse
import logging
import operator
from functools import reduce
logger = logging.getLogger(__name__)


def _generate_options():
    parser = argparse.ArgumentParser(description='Options for money stuff')
    parser.add_argument('--csv_file', help='name of the csv file to use')
    parser.add_argument(
        '--log_level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='INFO,DEBUG,WARNING,ERROR,CRITICAL')
    parser.add_argument('--balance_req',
                        help='what will determine what is spendable',
                        default=750.0)
    return parser


def parse_csv(csv_file):
    def trim(csv):
        total = ''.join(csv[-1])
        if total == '':
            return trim(csv[:-1])
        return csv

    logger.info('Parsing csv file: %s' % str(csv_file))
    csv_contents = None
    with open(csv_file, 'r') as f:
        csv_contents = f.read()
    csv = trim([x.split(',') for x in csv_contents.split('\n')])
    # logger.debug('All data: %s' % str(csv))
    logger.debug('Total number of cells: %i' % len(csv))
    return csv


def split_arr(arr, predicate):
    """
    We could do this with a for loop, but that wouldn't be fun, right?
    @param arr: Input data
    @param predicate: Function that returns bool takes in element at index for each iteration
    @returns: 2-tuple of 2 arrays, one for which every element in 'arr'
     matched True for (left side) other for False (right, side)
    """
    if len(arr) == 0:
        return ([], [])
    (a, b) = split_arr(arr[1:], predicate)
    return ([arr[0]] + a, b) if predicate(arr[0]) else (a, [arr[0]] + b)


def extract_column(csv, column_id):
    """
    Pulls a column from a csv, for example (input must be 2-D array):
    cola | colb | colc
     x      y      z
     a      b      c
    @returns: If column_id == 2 -> ['y', 'b']
    """
    if len(csv) == 0:
        return []
    return [csv[0][column_id]] + extract_column(csv[1:], column_id)


def parse_data(csv, user_a_predicate):
    heading = csv[0]
    data_fields = csv[1:]
    # The following throw exception if any fields are missing, this is expected behavior
    idx_map = {
        'description': heading.index('Description'),
        'amount': heading.index('Amount'),
        'balance': heading.index('Balance')
    }

    def internal_predicate(row):
        description_field = row[idx_map['description']]
        return user_a_predicate(description_field)

    # Split all transactions into two columns
    return (idx_map, split_arr(data_fields, internal_predicate))


# These methods ensure proper casts are performed and truncate the data sets before aggregating
def calculate_deposits(idx_map, data):
    charges = extract_column(data, idx_map['amount'])
    charges = [float(charge) for charge in charges if float(charge) > 0]
    return reduce(operator.add, charges)


def calculate_expenses(idx_map, data):
    charges = extract_column(data, idx_map['amount'])
    charges = [float(charge) for charge in charges if float(charge) < 0]
    return reduce(operator.add, charges)


def calculate_account_balance(idx_map, data):
    charges = extract_column(data, idx_map['amount'])
    charges = [float(charge) for charge in charges]
    return reduce(operator.add, charges)


def balance_from_csvfile(idx_map, allData):
    cellData = allData[1][idx_map['balance']]
    if cellData is None or cellData == '':
        return -1
    return float(cellData)


def pretty_col(rows):
    pretty_str = ""
    for row in rows:
        pretty_str += row + '\n'
    return pretty_str


def main():
    parser = _generate_options()
    options, program_options = parser.parse_known_args()
    formatter = '%(levelname)s:%(asctime)s - %(filename)s:%(lineno)d] %(message)s'
    logging.basicConfig(stream=sys.stdout,
                        level=options.log_level,
                        format=formatter)
    csv = parse_csv(options.csv_file)

    # This method is the predicate for selecting which transactions belong to Rob
    def user_a_re(description):
        res = [
            re.compile('.*....5590.*'),
            re.compile('.*AUTOPAYBUS.*'),
            re.compile('.*ending in 4984.*')
        ]
        return any([x.search(description) for x in res])

    # a will be the CSV for which transcations match the predicate for Rob
    # b will be all other transactions which are assumed to be for Fabian
    (idx_map, (a, b)) = parse_data(csv, user_a_re)
    logger.debug('All of a\'s charges: %s' %
                 pretty_col(extract_column(a, idx_map['description'])))
    logger.debug('All of b\'s charges: %s' %
                 pretty_col(extract_column(b, idx_map['description'])))

    # Call the functions on the data set, idx_map selects which column to 'parse_data' from
    # mapping between string and column index, created by 'parse_data' function
    deposits_a = calculate_deposits(idx_map, a)
    deposits_b = calculate_deposits(idx_map, b)
    expenses_a = calculate_expenses(idx_map, a)
    expenses_b = calculate_expenses(idx_map, b)
    logger.info('Total number of transactions by user a: %i', len(a))
    logger.info('Total number of transactions by user b: %i', len(b))
    logger.info('Total amount of deposits by user a: $%f', deposits_a)
    logger.info('Total amount of deposits by user b: $%f', deposits_b)
    logger.info('Total amount of expenses by user a: $%f', expenses_a)
    logger.info('Total amount of expenses by user b: $%f', expenses_b)

    calculated_account_balance_a = round(calculate_account_balance(idx_map, a),
                                         3)
    calculated_account_balance_b = round(calculate_account_balance(idx_map, b),
                                         3)
    if calculated_account_balance_a != round((deposits_a + expenses_a), 3):
        logger.fatal(
            'Mismatch between expected balance A and observed: calculated_account_balance_a == %f seen: %f'
            % (calculated_account_balance_a, (deposits_a + expenses_a)))
        sys.exit(1)
    if calculated_account_balance_b != round((deposits_b + expenses_b), 3):
        logger.fatal(
            'Mismatch between expected balance B and observed: calculated_account_balance_b == %f seen: %f'
            % (calculated_account_balance_b, (deposits_b + expenses_b)))
        sys.exit(1)

    logger.info('User a\'s account balance: $%f' %
                calculated_account_balance_a)
    logger.info('User b\'s account balance: $%f' %
                calculated_account_balance_b)

    logger.info('User a\'s spendable balance: $%f' %
                (calculated_account_balance_a - options.balance_req))
    logger.info('User b\'s spendable balance: $%f' %
                (calculated_account_balance_b - options.balance_req))

    calculated_total_account_balance = round(
        (calculated_account_balance_a + calculated_account_balance_b), 3)
    total_account_balance = round(calculate_account_balance(idx_map, a + b), 3)
    balance_from_csv = round(balance_from_csvfile(idx_map, csv), 3)
    if not (calculated_total_account_balance == total_account_balance ==
            (balance_from_csv if balance_from_csv != -1 else total_account_balance)):
        logger.fatal(
            'Mismatch between calculated_total_account_balance: %f , observed number: %f , and top csv balance number: %f '
            % (calculated_total_account_balance, total_account_balance,
               balance_from_csv))
        sys.exit(1)

    logger.info('Total account balance: $%f' % total_account_balance)
    sys.exit(0)


if __name__ == '__main__':
    main()
