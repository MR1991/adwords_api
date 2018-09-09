
# coding: utf-8

# In[191]:


#!/usr/bin/env python

# Author: Maurice Richard
# Version: 1.0
# Date: 20180906

# This script uses the ReportDownloader from the Adwords Api to collect the 
# TrackingUrlTemplate on Campaign level and on Keyword level. 

# Ouput is 2 CSV files, comma separated and with quotations. 
# The Campaign csv shows all campaigns that have a TrackingUrlTemplate.
# The Keywords csv shows all keywords that have an incorrect TrackingUrlTemplate
# A parameter is missing when it is not mentioned on a row.

# Script does not check for the correct order or multiple occurances of a parameter.
# Error handling to be added, e.g. to check per call whether the api returns data

import io
import pandas as pd

from googleads import adwords


### Settings -----------------------------------------------------------------------------

googleads_yaml      = "/home/mauricerichard91/googleads.yaml"
api_version         = 'v201806'
client_customer_ids = ('429-283-9693', '340-724-7913', '122-015-2837', '229-732-1788')
valid_template  = ('{lpurl}?utm_campaign={campaignid}_{adgroupid}_{creative}'                             '_{targetid}_{device}_{matchtype}') 
valid_parameters    = ('lpurl', 'campaignid', 'adgroupid', 'creative', 'targetid',
                       'device', 'matchtype')

### Queries -------------------------------------------------------------------------------

keyword_query = ('''select CustomerDescriptiveName, Criteria, TrackingUrlTemplate
                    from KEYWORDS_PERFORMANCE_REPORT''')

campaign_query = ('''select CustomerDescriptiveName, CampaignName, TrackingUrlTemplate
                     from CAMPAIGN_PERFORMANCE_REPORT''')

### Functions to get reports --------------------------------------------------------------

def get_report_one_client(adwords_client, api_version, query, client_customer_id):
    """Retrieves report for a specific customer client"""
    
    adwords_client.SetClientCustomerId(client_customer_id)
    report_downloader = adwords_client.GetReportDownloader(version = api_version)
    
    # Define output as a string
    output = io.BytesIO()

    # Write query result to output file
    report_downloader.DownloadReportWithAwql(
        query, 
        'CSV',
        output,
        client_customer_id  = client_customer_id,
        skip_report_header  = True, 
        skip_column_header  = False,
        skip_report_summary = True, 
        include_zero_impressions = True)

    output.seek(0)
    df = pd.read_csv(output)
    df.columns = [c.replace(' ', '_') for c in df.columns] # swap space by _ for easy code
    
    return(df)        

def get_report_all_clients(adwords_client, api_version, query, client_customer_ids):
    """Retrieves report for multiple customer clients."""

    ls = [get_report_one_client(adwords_client, api_version, query, 
                                client_customer_id = c)  for c in client_customer_ids]
    df = pd.concat(ls)
            
    return(df)


### Main ----------------------------------------------------------------------------------

# Loads settings for api client object and get data
adwords_client = adwords.AdWordsClient.LoadFromStorage(googleads_yaml)

df_campaigns = get_report_all_clients(adwords_client, api_version, campaign_query, 
                                      client_customer_ids)
df_keywords  = get_report_all_clients(adwords_client, api_version, keyword_query,  
                                      client_customer_ids)

# Selects campaigns where the tracking template is not empty, i.e. ' --'
df_campaigns_wrong = df_campaigns[df_campaigns.Tracking_template != ' --'].copy()

# On keyword level all records are selected that do not exactly match the required template
# then regex is used to check whether a parameter occurs at least once.
df_keywords_wrong  = df_keywords[df_keywords.Tracking_template != valid_template].copy()

for p in valid_parameters:
    df_keywords_wrong['{'+p+'}'] = df_keywords_wrong.Tracking_template                                                     .str.extract(r'(\{'+p+'\})')
    
# Write results to csv's 
today = pd.Timestamp('today')
df_keywords_wrong.to_csv('{:%Y%m%d}_keywords_wrong_trackingurl.csv'.format(today), 
                         index = False, quoting  = 1)
df_campaigns_wrong.to_csv('{:%Y%m%d}_campaigns_wrong_trackingurl.csv'.format(today), 
                         index = False, quoting  = 1)

