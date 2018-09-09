# Adwords_api
Some keynotes and script for running queries aainst the adwords api.  
  
# Instructions for setting up VM
1. Spin up fresh VM on google cloud: https://console.cloud.google.com/compute/instances  
  
2. Get pip, using python 2 in this case:
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py  
python get-pip.py  
  
3. Get googleads tar file from:  
https://github.com/googleads/google-ads-python  
wget <url from github>  
  
4. Unpack tar file into convenient folder (e.g. in /home/googleads), then install it.  
tar -xvf googleads-14.0.0.tar.gz 
cd googleads-14.0.0  
sudo python setup.py install  

5. Get another copy of the googleads yaml.  
wget https://raw.githubusercontent.com/googleads/googleads-python-lib/master/googleads.yaml  
And put it in a convenient folder again. Easiest is in same folder as you will run your jupyter notebooks from, but can also hardcode URL into scripts.  

# Create Adwords api credentials
https://developers.google.com/adwords/api/docs/guides/first-api-call

https://console.developers.google.com/apis/credentials

1. While logged in with your manager account credentials, open the Google API Console Credentials page.  
2. From the project drop-down, choose Create a new project, enter a name for the project, and click Create.  
3. Select Create credentials and choose OAuth client ID.  
4. You may be prompted to set a product name on the Consent screen; if so, click Configure Consent Screen, supply the requested information, and click Save to return to the Credentials screen.  
5. Under Application type, choose Other for this tutorial. Enter a name in the space provided.  
6. For the AdWords API, Other is the option to choose for an installed application flow. Before you build your app, you'll want to read up on the difference between installed and web applications, and choose the appropriate type for the app you're building.  
7. Click Create. The OAuth2 client ID and client secret appear. Copy and save these items. You will add them to your configuration file in the next step.  

wget https://raw.githubusercontent.com/googleads/googleads-python-lib/master/examples/adwords/authentication/generate_refresh_token.py
python generate_refresh_token.py --client_id <insert client_id> --client_secret <insert client_secret>
Go to webpage and copy paste code into terminal. You will receive an access and refresh token

nano googleads.yaml 

```
  #############################################################################
  # Required Fields                                                           #
  #############################################################################
  developer_token: xxxxx     
  #############################################################################
  # Optional Fields                                                           #
  #############################################################################
  # client_customer_id: INSERT_CLIENT_CUSTOMER_ID_HERE
  # user_agent: INSERT_USER_AGENT_HERE
  # partial_failure: True
  # validate_only: True
  #############################################################################
  # OAuth2 Configuration                                                      #
  # Below you may provide credentials for either the installed application or #
  # service account flows. Remove or comment the lines for the flow you're    #
  # not using.                                                                #
  #############################################################################
  # The following values configure the client for the installed application
  # flow.
  client_id: xxxxx
  client_secret: xxxxx
  refresh_token: xxxxx
```

pip3 install jupyter

https://towardsdatascience.com/running-jupyter-notebook-in-google-cloud-platform-in-15-min-61e16da34d52
jupyter notebook --generate-config
nano ~/.jupyter/jupyter_notebook_config.py

add to top
c = get_config()
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8000

Run jupyter:
jupyter-notebook --no-browser --port=8000
go to
http://35.237.143.72:8000/notebooks/


https://developers.google.com/adwords/api/docs/samples/python/reporting

Example code for report:

"""This example downloads a criteria performance report with AWQL.
To get report fields, run get_report_fields.py.
The LoadFromStorage method is pulling credentials and properties from a
"googleads.yaml" file. By default, it looks for this file in your home
directory. For more information, see the "Caching authentication information"
section of our README.
"""

import sys
from googleads import adwords

def main(client):
  # Initialize appropriate service.
  report_downloader = client.GetReportDownloader(version='v201806')

  # Create report query.
  report_query = (adwords.ReportQueryBuilder()
                  .Select('CampaignId', 'AdGroupId', 'Id', 'Criteria',
                          'CriteriaType', 'FinalUrls', 'Impressions', 'Clicks',
                          'Cost')
                  .From('CRITERIA_PERFORMANCE_REPORT')
                  .Where('Status').In('ENABLED', 'PAUSED')
                  .During('LAST_7_DAYS')
                  .Build())

  # You can provide a file object to write the output to. For this
  # demonstration we use sys.stdout to write the report to the screen.
  report_downloader.DownloadReportWithAwql(
      report_query, 'CSV', sys.stdout, skip_report_header=False,
      skip_column_header=False, skip_report_summary=False,
      include_zero_impressions=True)


if __name__ == '__main__':
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage("/home/mauricerichard91/googleads.yaml")
  adwords_client.SetClientCustomerId('429-283-9693')
  main(adwords_client)

Client ID's
429-283-9693
340-724-7913
122-015-2837
229-732-1788


data point to get:
https://developers.google.com/adwords/api/docs/reference/v201806/AdGroupAdService.UrlData
https://developers.google.com/adwords/api/docs/samples/python/basic-operations#get-the-ad-groups-of-a-campaign

sudo pip install pandas
