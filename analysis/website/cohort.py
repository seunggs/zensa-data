from matplotlib import pyplot as plt
import numpy as np
import argparse
import csv

# USAGE:
#   python cohort.py -csv [csv filename; i.e. cohort-data-from-2017-05-01-to-2017-11-08.csv]
# AVAILABLE OPTIONS:
#   -csv (required)

parser = argparse.ArgumentParser(description='Analysize data by cohort')
parser.add_argument('-csv', '--csv', help='CSV filename to use to create the charts', required=True)
args = vars(parser.parse_args())

with open(args['csv']) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    rows = np.array([row for (i, row) in enumerate(readCSV)])

heading = rows[0]
cols = rows[1:].T
date = cols[0]
colsLessDate = cols[1:]
colsLessDateInFloat = colsLessDate.astype(np.float)  # change all the values to float with 2 decimal places
date_name = [i[5:] for i in date] # abbreviated cohort date name

for i, col in enumerate(colsLessDateInFloat):
    plt.figure(figsize=(16, 9), dpi=80)
    plt.bar(date_name, colsLessDateInFloat[i])
    plt.title(heading[i+1])
    plt.ylabel(heading[i+1])
    plt.xlabel('cohort')
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.savefig('cohort_analysis_' + heading[i+1] + '.svg')
    # plt.show()
