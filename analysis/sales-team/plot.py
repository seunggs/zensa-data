from matplotlib import pyplot as plt
from matplotlib.dates import date2num
import numpy as np
import argparse
import csv
from datetime import datetime
import math
import os

# USAGE:
#   python plot.py -folder 2014-04-01_2017-11-13
# AVAILABLE OPTIONS:
#   -folder (required)
# EXAMPLE:
#   python plot.py -folder 2014-04-01_2017-11-13
#   python plot.py -folder 2014-04-01_2017-12-19

cwd = os.getcwd()
parser = argparse.ArgumentParser(description='Analyze sales team data')
parser.add_argument('-folder', '--folder', help='Folder name', required=True)
args = vars(parser.parse_args())

# CONSTANTS
showPlt = False

def get_csv_data(filename):
    with open(cwd + '/' + args['folder'] + '/' + filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        raw_data = np.array([tuple(row) for (i, row) in enumerate(readCSV)])
        heading = raw_data[0]
        data = raw_data[1:]
        data[data=='']='0'
        data_dict = [dict(zip(heading, row)) for row in data]
    return (heading, data_dict)

def get_col(colName, rows):
    return np.array([cols[colName] for cols in rows])

def convert_to_datetime(dates):
    return np.array([datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').date() for date in dates]).astype('str')

def setupPlt():
    plt.figure(figsize=(20, 9), dpi=80)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.xticks(rotation='vertical')

def savePlt(filename):
    if showPlt:
        plt.show()
    plt.savefig(cwd + '/' + args['folder'] + '/charts/' + filename + '.svg')


# annual-retention-monthly-trend.csv
#
filename = 'annual-retention-monthly-trend.csv'
(heading, data) = get_csv_data(filename)
retention_rate = get_col('retention_rate', data)
date = get_col('date', data)

setupPlt()
plt.bar(date, retention_rate)
plt.title(filename)
plt.ylabel('retention_rate')
plt.xlabel('monthly_cohort')
savePlt(filename)

# initial-purchase-cycle-by-monthly-cohort.csv
#
filename = 'initial-purchase-cycle-by-monthly-cohort.csv'
(heading, data) = get_csv_data(filename)
date = get_col('date', data)
purchase_cycle = get_col('initial_purchase_cycle_in_days', data).astype(float)
# purchase_value = get_col('initial_purchase_value', data).astype(float)
x = np.arange(len(date))

setupPlt()
plt.xticks(x, date)
plt.bar(x + 0.00, purchase_cycle, color='#EE3224', width=0.25, label='purchase_cycle')
# plt.bar(x + 0.25, purchase_value, color='#FFC222', width=0.25, label='purchase_value')
plt.legend(loc='upper left')
plt.title(filename)
plt.ylabel('initial_purchase_cycle_in_days')
plt.xlabel('purchase_date')
savePlt(filename)

# repeat-purchase-cycle-by-monthly-cohort.csv
#
filename = 'repeat-purchase-cycle-by-monthly-cohort.csv'
(heading, data) = get_csv_data(filename)
date = get_col('date', data)
purchase_cycle = get_col('avg_purchase_cycle', data).astype(float)
# purchase_value = get_col('avg_purchase_size', data).astype(float)
x = np.arange(len(date))

setupPlt()
plt.xticks(x, date)
plt.bar(x + 0.00, purchase_cycle, color='#EE3224', width=0.25, label='purchase_cycle')
# plt.bar(x + 0.25, purchase_value, color='#FFC222', width=0.25, label='purchase_value')
plt.legend(loc='upper left')
plt.title(filename)
plt.ylabel('initial_purchase_cycle_in_days')
plt.xlabel('purchase_date')
savePlt(filename)

# new-deals-weekly-cohort-trend.csv
#
filename = 'new-deals-weekly-cohort-trend.csv'
(heading, data) = get_csv_data(filename)
date = get_col('date', data)
purchase_value = get_col('decimal_value', data).astype(float)
num_new_clients = get_col('contact_count', data).astype(float)
x = np.arange(len(date))

setupPlt()
plt.xticks(x, date)
plt.plot(x, purchase_value, color='#EE3224', label='purchase_value')
plt.legend(loc='upper left')
plt.title(filename)
plt.ylabel('purchase_value')
plt.xlabel('purchase_date')
savePlt(filename)

# number of new orders
setupPlt()
plt.xticks(x, date)
plt.plot(x, num_new_clients, color='#EE3224', label='num_new_clients')
plt.legend(loc='upper left')
plt.title(filename)
plt.ylabel('num_new_clients')
plt.xlabel('purchase_date')
savePlt(filename)

# repeat-deals-weekly-cohort-trend.csv
#
filename = 'repeat-deals-weekly-cohort-trend.csv'
(heading, data) = get_csv_data(filename)
date = get_col('date', data)
purchase_value = get_col('decimal_value', data).astype(float)
num_repeat_clients = get_col('contact_count', data).astype(float)
x = np.arange(len(date))

setupPlt()
plt.xticks(x, date)
plt.plot(x, purchase_value, color='#EE3224', label='purchase_value')
plt.legend(loc='upper left')
plt.title(filename)
plt.ylabel('purchase_value')
plt.xlabel('purchase_date')
savePlt(filename)

# number of repeat orders
setupPlt()
plt.xticks(x, date)
plt.plot(x, num_repeat_clients, color='#EE3224', label='num_repeat_clients')
plt.legend(loc='upper left')
plt.title(filename)
plt.ylabel('num_repeat_clients')
plt.xlabel('purchase_date')
savePlt(filename)

# initial-purchase-cycle-by-deal-size-distribution.csv
#
filename = 'initial-purchase-cycle-by-deal-size-distribution.csv'
(heading, data) = get_csv_data(filename)
bucket_labels = get_col('bucket', data)
avg_initial_purchase_cycle_in_days = get_col('avg_initial_purchase_cycle_in_days', data).astype(float)
x = np.arange(len(bucket_labels))

setupPlt()
plt.xticks(x, bucket_labels)
plt.bar(x, avg_initial_purchase_cycle_in_days, color='#EE3224', label='avg_initial_purchase_cycle_in_days')
plt.legend(loc='upper left')
plt.title(filename)
plt.ylabel('avg_initial_purchase_cycle_in_days')
plt.xlabel('bucket')
savePlt(filename)

# avg-deal-size-by-contact-distribution.csv
#
filename = 'avg-deal-size-by-contact-distribution.csv'
(heading, data) = get_csv_data(filename)
bucket_labels = get_col('avg deal size bucket', data)
frequency = get_col('frequency', data).astype(int)
x = np.arange(len(bucket_labels))

setupPlt()
plt.xticks(x, bucket_labels)
plt.bar(x, frequency, color='#EE3224', label='frequency')
plt.legend(loc='upper left')
plt.title(filename)
plt.ylabel('frequency')
plt.xlabel('avg deal size bucket')
savePlt(filename)
