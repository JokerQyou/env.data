# coding: utf-8
import csv
from datetime import datetime
import os
import sys

import click
from dotenv import load_dotenv
import leancloud
from loguru import logger

load_dotenv()
logger.remove()
logger.add(
    sys.stdout,
    format='<green>{time:YYYY-MM-DD HH:mm:ss}</green> <level>{level: <8}</level> <level>{message}</level>',
    level='INFO',
)


def export_month_data(year, month):
    start = datetime(year, month, 1)
    if month == 12:  # Last month of the year
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)

    EnvSnap = leancloud.Object.extend('EnvSnap')
    logger.info('Querying {} data in range of [{}, {})', 'EnvSnap', start, end)

    query = EnvSnap.query

    query.greater_than_or_equal_to('createdAt', start)
    query.less_than('createdAt', end)

    query.add_ascending('createdAt')

    data_count = query.count()

    if data_count:
        logger.info('{} rows of data', data_count)
    else:
        logger.info('No data for {:04d}-{:02d}', year, month)
        return

    # Pagination
    data = []
    query.limit(1000)
    while len(data) < data_count:
        query.skip(len(data))
        new_data = query.find()
        logger.info('Fetched {} rows of data', len(new_data))
        data.extend(new_data)

    foldername = os.path.join('{:04d}'.format(year), '{:02d}'.format(month))
    logger.info('Data will be saved to {}', foldername)

    if not os.path.isdir(foldername):
        os.makedirs(foldername)

    for target in ('temperature', 'pressure', 'humidity'):
        filename = os.path.join(foldername, '{}.csv'.format(target))
        with open(filename, 'w', newline='') as wf:
            writer = csv.writer(wf)
            writer.writerow(['Timestamp', target.capitalize()])  # Header
            for item in data:
                writer.writerow([
                    item.created_at.timestamp(),
                    item.get(target),
                ])
        logger.info('{} data saved to {}', target.capitalize(), filename)


@click.command()
@click.argument('year', type=int, required=True)
@click.argument('month', type=int, required=True)
@click.option('--appid', required=True, envvar='APP_ID')
@click.option('--appkey', required=True, envvar='APP_KEY')
@click.option('--username', required=True, envvar='L_USER')
@click.option('--password', required=True, envvar='L_PAWD')
def main(year, month, appid, appkey, username, password):
    leancloud.init(appid, appkey)
    user = leancloud.User()
    user.login(username, password)
    logger.info('User login OK')

    export_month_data(year, month)
    user.logout()
    logger.info('User logged out')


if __name__ == '__main__':
    main()

