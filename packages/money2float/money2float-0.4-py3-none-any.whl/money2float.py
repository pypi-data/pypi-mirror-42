#!/usr/bin/env python
# coding: utf-8

# In[4]:


from decimal import *
import re


# In[9]:


def money(text, places=2):
    text = f"{text}"
    try:
        text = text.replace(",", "")
    except:
        pass
    try:
        text = text.replace("$", "")
    except:
        pass
    try:
        response = float(round(Decimal(text), places))
    except:
        text = re.sub("[^\d\.]", "", text)
        try:
            response = float(round(Decimal(text), places))
        except:
            response = 0
    return response


# In[ ]:
