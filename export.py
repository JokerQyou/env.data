# coding: utf-8
import csv
import os
import sys

import requests

'''
Usage: python export.py 00:00_20170101 00:00_20170201
'''


def export(start, end):
    for target in ('temperature', 'pressure', 'humidity'):
        data = requests.get(
            'http://127.0.0.1:6666/render', params={
                'format': 'json',
                'target': 'stats.gauges.nodemcu.{}'.format(target),
                'from': start,
                'until': end,
            }
        ).json()

        foldername = start.split('_')[-1][:6]

        if not os.path.isdir(foldername):
            os.makedirs(foldername)

        filename = os.path.join(foldername, '{}.csv'.format(target))
        with open(filename, 'w', newline='') as wf:
            writer = csv.writer(wf)
            writer.writerow(['Timestamp', target.capitalize()])  # Header
            for v, t in data[0]['datapoints']:
                writer.writerow([t, v])
        print('Target {} from {} to {} exported, saved as "{}"'.format(
            target, start, end, filename
        ))


if __name__ == '__main__':
    export(*sys.argv[1:])
