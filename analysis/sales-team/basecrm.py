from matplotlib import pyplot as plt
import numpy as np
import argparse
import csv

# USAGE:
#   python basecrm.py -csv_deals [deals csv from Base CRM] -csv_contacts [contacts csv from Base CRM]
# AVAILABLE OPTIONS:
#   -csv_deals (required)
#   -csv_contacts (required)
# EXAMPLE:
#   python basecrm.py -csv_deals deals.csv -csv_contacts contacts.csv

parser = argparse.ArgumentParser(description='Analysize data by cohort')
parser.add_argument('-csv_deals', '--csv_deals', help='deals csv from Base CRM', required=True)
parser.add_argument('-csv_contacts', '--csv_contacts', help='contacts csv from Base CRM', required=True)
args = vars(parser.parse_args())

with open(args['csv_contacts']) as csv_contacts_file:
    read_csv_contacts = csv.reader(csv_contacts_file, delimiter=',')
    all_contacts_raw = np.array([row for row in read_csv_contacts])
    all_contacts_headings = all_contacts_raw[0]
    contacts_index_dict = dict(zip(all_contacts_headings, range(0,len(all_contacts_headings))))
    all_contacts = np.array([x for x in all_contacts_raw[1:] if len(x) == len(all_contacts_headings)]) # get rid of empty rows
    all_contact_ids = all_contacts[:, contacts_index_dict['id']]

with open(args['csv_deals']) as csv_deals_file:
    read_csv_deals = csv.reader(csv_deals_file, delimiter=',')
    all_deals_raw = np.array([row for row in read_csv_deals])
    all_deals_headings = all_deals_raw[0]
    deals_index_dict = dict(zip(all_deals_headings, range(0,len(all_deals_headings))))
    # print(deals_index_dict)
    all_deals = np.array([x for x in all_deals_raw[1:] if len(x) == len(all_deals_headings)]) # get rid of empty rows
    won_deals = np.array([cols for cols in all_deals if cols[deals_index_dict['stage_name']] == 'Won'])
    # print(len(all_deals))
    # print(len(won_deals))

def get_deals(contact_id):
    # get all deals per contact, but sort it based on when it was won
    deals = np.array([deal for deal in all_deals if deal[deals_index_dict['company_id']] == contact_id])
    print(deals.shape)
    return deals[deals[:, deals_index_dict['last_stage_change_at']].argsort()]

# Group all the deals by contact
deals_by_contact = np.array([get_deals(contactId) for contactId in all_contact_ids])
print(deals_by_contact[0])
