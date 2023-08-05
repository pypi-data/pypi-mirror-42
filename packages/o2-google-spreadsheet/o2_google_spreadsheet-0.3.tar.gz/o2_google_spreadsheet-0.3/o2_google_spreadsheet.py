#!/usr/bin/env python
# coding: utf-8

# In[11]:


import json
import numpy as np
import pandas as pd
import re

import gspread

from pathlib import Path
from money2float import money
from oauth2client.service_account import ServiceAccountCredentials


# In[12]:


def get_online_data(google_sheets):
    secret_filename = Path.cwd() / "mba-optim2-d1e893718415.json"

    # use creds to create a client to interact with the Google Drive API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(secret_filename, scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open(google_sheets).worksheet("Data")

    # Extract and print all of the values
    all_data = sheet.get_all_records()
    return pd.DataFrame(all_data)


# In[18]:


def convert_columns(df):
    columns = {
        "First": "first_name",
        "Last": "last_name",
        "Cloudstaff": "cloudstaff_id",
        "Bill": "billable_client",
        "Account": "client_name",
        "Status": "status",
        "Direct cost": "direct_cost",
        "Service fee payable": "service_fee_payable",
        "Total Cost": "total_cost",
        "Service fee billable": "service_fee_billable",
    }

    new_columns = [
        "full_name",
        "cloudstaff_id",
        "billable_client",
        "client_name",
        "status",
        "direct_cost",
        "service_fee_payable",
        "total_cost",
        "service_fee_billable",
    ]

    df2 = df.rename(columns=columns)
    df2["full_name"] = (
        df2["first_name"].astype(str) + " " + df2["last_name"].astype(str)
    )
    df2 = df2[new_columns]
    data = df2
    data["direct_cost"] = df2["direct_cost"].apply(lambda x: money(f"{x}"))
    data["service_fee_payable"] = df2["service_fee_payable"].apply(
        lambda x: money(f"{x}")
    )
    data["total_cost"] = df2["total_cost"].apply(lambda x: money(f"{x}"))
    data["service_fee_billable"] = df2["service_fee_billable"].apply(
        lambda x: money(f"{x}")
    )
    data = data[data["direct_cost"] > 0]
    data = data.replace(r"^\s*$", np.nan, regex=True)
    data["billable_client"] = data["billable_client"].fillna(data["client_name"])
    return data


# In[ ]:
