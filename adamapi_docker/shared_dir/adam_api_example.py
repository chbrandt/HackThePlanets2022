#!/usr/bin/env python
# coding: utf-8

# # Adam API usage example
# https://docs.neanias.eu/projects/c2-dataexploration/en/latest/
# 

# In[1]:


get_ipython().system(' which python')


# In[4]:


get_ipython().system(' ls /app/')


# In[6]:


get_ipython().system(' cat /app/adam_api_key.txt')


# In[2]:


import adamapi


# In[3]:


from adamapi import Auth


# In[9]:


a = Auth()
a.setKey("qCKuUM8PMIx9llcCq8-yD-A1u01TZNN4CHT82Oo4o38")
a.setAdamCore("https://explorer-space.adamplatform.eu")
a.authorize()


# In[10]:


auth_data


# In[11]:


from adamapi import Datasets
datasets = Datasets(a)
items = datasets.getDatasets()
print( "Available datasets:")
for key in items: 
    print( key )


# In[16]:


datasetId = "58592:MRO_CTX"


# In[25]:


metadata = datasets.getDatasets(datasetId)
metadata


# ## Count all products

# In[48]:


min_start_date = '2006-03-24'
max_end_date = '2020-08-30'


# In[ ]:


from adamapi import Search


# In[83]:


def downloadMetadata(auth, start_date, end_date):
    search = Search(auth)
    maxRec = 200
    search_result = search.getProducts(
        datasetId,
        maxRecords=maxRec,
        startIndex=0,
        outputAttributes=['productId'],
        startDate=start_date,
        endDate=end_date
    )
    print(f"Total products: {len(search_result['content'])}")
    return search_result["content"]
#for product in search_result["content"][0:10]:
#    print(product["productId"])


# In[89]:


files_metadata = []


# In[90]:


from dateutil.relativedelta import relativedelta
start_date = date(2015, 7, 1)
end_date = date(2016, 1, 1)
while start_date < end_date:
    next_date = start_date + relativedelta(days=1)
    print(f"Download data from {start_date} - {next_date}")    
    files_metadata = files_metadata + downloadMetadata(a, start_date, next_date)
    start_date = next_date


# In[91]:


len(files_metadata)


# In[93]:


get_ipython().system(' pwd')


# In[94]:


import pickle
pickle.dump(files_metadata, open('/shared_dir/files_metadata.pickle', 'wb'))


# In[22]:


first_product = search_result["content"][0]["productId"]
first_product


# In[23]:


from adamapi import GetData
data=GetData(a)
product = first_product
data.getData(datasetId, productId = product, outputFname=f"/shared_dir/{first_product}")


# In[ ]:




