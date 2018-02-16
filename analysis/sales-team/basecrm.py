from matplotlib import pyplot as plt
import numpy as np
import argparse
import csv
import datetime
import math
from termcolor import colored

# USAGE:
#   python basecrm.py -csv_deals [deals csv from Base CRM] -csv_contacts [contacts csv from Base CRM]
# AVAILABLE OPTIONS:
#   -csv_deals (required)
#   -csv_contacts (required)
# EXAMPLE:
#   python basecrm.py -csv_deals deals.csv -csv_contacts contacts.csv

# remove_empty_rows :: np_array -> np_array
def remove_empty_rows(rows):
    return np.array([row for row in rows if len(row) != 0])

# remove_invalid_deals :: list -> np_array -> np_array
def remove_invalid_deals(all_keys, rows):
    company_id_index = all_keys.index('company_id')
    return np.array([row for row in rows if row[company_id_index] != ''])

# Change the date format 2014-10-16T17:13:38Z to 2014-10-16
# normalize_date_format :: list -> np_array -> np_array
def normalize_date_format(date_indices, rows):
    return np.array([[col.split('T')[0] if i in date_indices else col for (i, col) in enumerate(row)] for row in rows])

# keep_cols :: list -> list -> array of tuples
def keep_cols(keys_to_keep, all_keys, rows):
    key_indices_to_keep = [all_keys.index(key) for key in keys_to_keep]
    shortened_rows = rows[:, key_indices_to_keep]
    return [tuple(row) for row in shortened_rows]

# get_deals_by_contact_id :: str -> np_array -> np_array
def get_deals_by_contact_id(contact_id, all_deals):
    return np.array([deal for deal in all_deals if deal['company_id'] == contact_id])

# group_deals_by_contact :: np_array -> np_array -> np_array
def group_deals_by_contact(all_contact_ids, all_deals):
    return remove_empty_rows(np.array([get_deals_by_contact_id(contactId, all_deals) for contactId in all_contact_ids]))

# sort_by_key :: str -> structured np_array -> structured np_array
def sort_by_key(key, np_arr):
    return np.sort(np_arr, order = key)

# filter_by_key :: str -> func -> structured np_array -> structured np_array
def filter_by_key(key, predicate, np_arr):
    return XXX

# diff_np_datetime :: datetime64[D] -> datetime64[D] -> int
def diff_np_datetime_days(date1, date2):
    return (date2 - date1).astype('timedelta64[D]') / np.timedelta64(1, 'D')

def find_nearest_index(value, np_arr):
    return (np.abs(np_arr - value)).argmin()

def get_breakpoint_indices(breakpoints, rows):
    return [find_nearest_index(breakpoint, rows['added_on']) for breakpoint in breakpoints]

# Divide the data by time cohort
# Provide flattened list
# create_cohorts :: int -> np_array -> np_array
def create_cohorts(days, rows):
    # Sort the list by
    rows_sorted = sort_by_key('added_on', rows)

    # Create time breakpoints
    first_added_on_date = rows_sorted[0]['added_on']
    last_added_on_date = rows_sorted[len(rows_sorted) - 1]['added_on']
    diff_days = diff_np_datetime_days(first_added_on_date, last_added_on_date)
    num_breakpoints = math.ceil(diff_days / days)
    breakpoints = [first_added_on_date + np.timedelta64((days * (i + 1)), 'D') for i in range(num_breakpoints)]
    breakpoints_indices = get_breakpoint_indices(breakpoints, rows_sorted)

    # Use the breakpoints to split the data into cohorts
    return np.array(np.split(rows_sorted, breakpoints_indices))

# average_cohort :: np_array -> np_array
def average_cohort(keys, cohort):
    [deals for deals in cohort]



def main():
    parser = argparse.ArgumentParser(description='Analyze data by cohort')
    parser.add_argument('-csv_deals', '--csv_deals', help='deals csv from Base CRM', required=True)
    parser.add_argument('-csv_contacts', '--csv_contacts', help='contacts csv from Base CRM', required=True)
    args = vars(parser.parse_args())

    with open(args['csv_contacts']) as csv_contacts_file:
        read_csv_contacts = csv.reader(csv_contacts_file, delimiter=',')
        all_contacts_raw = np.array([row for row in read_csv_contacts])
        all_contacts_raw_cleaned = remove_empty_rows(all_contacts_raw)
        all_contacts_headings = all_contacts_raw_cleaned[0]
        all_contacts_rows = all_contacts_raw_cleaned[1:]

    # Create a structured np_array
    all_contacts_dtype = [
        ('id', 'i4'),
    ]
    all_contacts_unstructured = keep_cols([key for (key, dtype) in all_contacts_dtype], list(all_contacts_headings), all_contacts_rows)
    all_contacts = np.array(all_contacts_unstructured, dtype=all_contacts_dtype)
    all_contact_ids = np.array(all_contacts['id'])

    with open(args['csv_deals']) as csv_deals_file:
        read_csv_deals = csv.reader(csv_deals_file, delimiter=',')
        all_deals_raw = np.array([row for row in read_csv_deals])
        all_deals_headings = all_deals_raw[0]
        all_keys = list(all_deals_headings)
        all_deals_raw_cleaned = remove_invalid_deals(all_keys, remove_empty_rows(all_deals_raw))
        all_deals_rows = all_deals_raw_cleaned[1:]
        last_stage_change_at_index = all_keys.index('last_stage_change_at')
        all_deals_rows_date_normalized = normalize_date_format([last_stage_change_at_index], all_deals_rows)

    # Create a structured np_array
    all_deals_dtype = [
        ('name', '<U255'),
        ('stage_name', '<U255'),
        ('owner', '<U255'),
        ('company_id', 'i4'),
        ('added_on', 'datetime64[D]'),
        ('currency', '<U255'),
        ('decimal_value', 'f4'),
        ('last_stage_change_at', 'datetime64[D]'),
    ]
    keys_to_keep = [key for (key, dtype) in all_deals_dtype]
    all_deals_unstructured = keep_cols(keys_to_keep, all_keys, all_deals_rows_date_normalized)
    all_deals_structured = np.array(all_deals_unstructured, dtype=all_deals_dtype)
    all_deals = all_deals_structured[all_deals_structured['owner'] != 'Hussein Lalani'] # filter out Hussein's deals
    won_deals = all_deals[all_deals['stage_name'] == 'Won']

    # Group all the deals by contact
    deals_by_contact = group_deals_by_contact(all_contact_ids, all_deals)
    won_deals_by_contact = group_deals_by_contact(all_contact_ids, won_deals)
    won_deals_by_contact_sorted = np.array([sort_by_key('last_stage_change_at', buyer) for buyer in won_deals_by_contact]) # deals inside each contact sorted by last_stage_change_at

    new_deals = np.array([contact[0] for contact in won_deals_by_contact_sorted])
    repeat_deals_by_contact = remove_empty_rows(np.array([contact[1:] for contact in won_deals_by_contact_sorted]).ravel())
    repeat_deals = np.array([deals for contact in repeat_deals_by_contact.tolist() for deals in contact])

    # Create cohorts
    new_deals_cohorts = create_cohorts(7, new_deals)
    new_deals_cohorts_averaged = [cohort for cohort in new_deals_cohorts]
    repeat_deals_cohorts = create_cohorts(7, repeat_deals)
    repeat_deals_cohorts_averaged = [ for cohort in repeat_deals_cohorts]

    ### ACTUAL ANALYSIS

    # Percentage of repeat clients
    repeat_client_ratio = len(repeat_deals_by_contact) / len(won_deals_by_contact)
    print colored('What percentage of buyers is repeat buyers?' + repeat_client_ratio, 'green')

    # Set up plt
    plt.figure(figsize=(16, 9), dpi=80)
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)

    # Sales trends - new
    plt.bar(date_name, new_deals_cohorts_averaged)
    plt.title(heading[i+1])
    plt.ylabel(heading[i+1])
    plt.xlabel('cohort')
    plt.savefig('cohort_analysis_' + heading[i+1] + '.svg')
    # plt.show()

    #


    # Per salesperson metrics
    won_deals_by_aly = won_deals[won_deals['owner'] == 'Aly Lalani']
    won_deals_by_nabil = won_deals[won_deals['owner'] == 'Nabil Khan']
    won_deals_by_nicole = won_deals[won_deals['owner'] == 'Nicole Sprauer']




if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
