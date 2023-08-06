#!/usr/bin/env python
# coding: utf-8

# In[14]:


import re

from datetime import date, timedelta
from pathlib import Path

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


# In[9]:


def split_text(text, symbol):
    lines = text.split(symbol)
    lines = [line.split() for line in lines if line]
    return lines


# In[11]:


def find_objects(lines, object_type):
    return_lines = []
    for line in lines:
        return_line = []
        for word in line:
            if object_type == "dates":
                try:
                    if len(word) > 5:
                        raw_date = parse(word, dayfirst=True)
                        formatted_date = raw_date.strftime(format="%Y-%m-%d")
                        elapsed_years = relativedelta(raw_date, date.today()).years
                        if elapsed_years > -10:
                            return_line.append(formatted_date)
                except:
                    pass
            elif object_type == "numbers":
                r1 = re.match(r"[\$0-9\.,]+", word)
                try:
                    return_line.append(r1.group(0))
                except:
                    pass
        return_lines.append(return_line)
    return return_lines


# In[ ]:
