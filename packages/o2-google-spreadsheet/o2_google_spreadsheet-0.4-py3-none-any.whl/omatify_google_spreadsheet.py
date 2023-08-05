#!/usr/bin/env python
# coding: utf-8

# In[2]:


from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import requests
import json
import pandas as pd
import re
import os

load_dotenv(find_dotenv())


# In[3]:


api_key = os.getenv("DOCPARSER_API_KEY")
parser_id = os.getenv("PARSER_ID")


# In[ ]:
