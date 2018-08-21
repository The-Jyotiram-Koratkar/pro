
# coding: utf-8

# Each page has 50 job postings, which means that the total number of jobs can be calcuated as follows:

# In order to work with this data at a later point in time, we could save it as a csv file. A better was to do this is to save the dataframe as a pickle object using cPickle library. By doing this we can store and retrieve the data as a Python object (i.e., Pandas dataframe). 

# In[1]:


import bs4
import urllib2
import pandas as pd
import math
import time
from pandas import DataFrame
from collections import OrderedDict
import cPickle
########################################################################
base_url = 'https://www.naukri.com/it-telecom-data-science-machine-learning-jobs'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
req = urllib2.Request(base_url, headers=hdr)
try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

source = page.read()

##################################################################################

soup = bs4.BeautifulSoup(source, "lxml")


# In[2]:


# Together into one function
labels = ['Salary', 'Industry', 'Functional Area', 'Role Category', 'Design Role']
edu_labels = ['UG', 'PG', 'Doctorate']
naukri_df = pd.DataFrame()
num_pages = int(3)


# In[3]:


for page in range(1,num_pages+1):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    page_url = base_url+str(page)
    
    req2=urllib2.Request(page_url,headers=hdr)
    try:
        source_base2=urllib2.urlopen(req2)
    except urllib2.HTTPError, err:
        print err.fp.read()
    
    
    source = source_base2.read()
    soup = bs4.BeautifulSoup(source,"lxml")
    all_links = [link.get('href') for link in soup.findAll('a') if 'job-listings' in  str(link.get('href'))]
    for url in all_links:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        req1=urllib2.Request(url,headers=hdr)
        try:
            
            source_base=urllib2.urlopen(req1)
        except urllib2.HTTPError, er:
            print er.fp.read()
        jd_source = source_base.read()
        jd_soup = bs4.BeautifulSoup(jd_source,"lxml")
        try:
            jd_text = jd_soup.find("ul",{"itemprop":"description"}).getText().strip()
            location = jd_soup.find("div",{"class":"loc"}).getText().strip()
            experience = jd_soup.find("span",{"itemprop":"experienceRequirements"}).getText().strip()
            
            role_info = [content.getText().split(':')[-1].strip() for content in jd_soup.find("div",{"class":"jDisc mt20"}).contents if len(str(content).replace(' ',''))!=0]
            role_info_dict = {label: role_info for label, role_info in zip(labels, role_info)}
            
            key_skills = '|'.join(jd_soup.find("div",{"class":"ksTags"}).getText().split('  '))[1:]

            edu_info = [content.getText().split(':') for content in jd_soup.find("div",{"itemprop":"educationRequirements"}).contents if len(str(content).replace(' ',''))!=0]
            edu_info_dict = {label.strip(): edu_info.strip() for label, edu_info in edu_info}
            for l in edu_labels:
                if l not in edu_info_dict.keys():
                    edu_info_dict[l] = ''

            company_name = jd_soup.find("div",{"itemprop":"hiringOrganization"}).contents[1].p.getText().strip()
        
        except AttributeError:
            continue
        df_dict = OrderedDict({'Location':location, 'Link':url,'Job Description':jd_text,'Experience':experience,'Skills':key_skills,'Company Name':company_name})
        df_dict.update(role_info_dict)
        df_dict.update(edu_info_dict)
        naukri_df = naukri_df.append(df_dict,ignore_index=True)
        time.sleep(1)
    print page


# In[4]:


#naukri_df.count()


# In[5]:

'''
import sqlalchemy
database_username = 'root'
database_password = 'vishi'
database_ip       = 'localhost'
database_name     = 'jobs'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))
naukri_df.to_sql(con=database_connection, name='test', if_exists='replace')
'''

# In[6]:


#naukri_df.columns


# In[7]:


#dff=pd.read_sql_table('dataScience',con=database_connection,schema=None)


# In[8]:


#dff


# In[ ]:


# import cPickle
# column_names = ['Location', 'Link', 'Job Description', 'Experience','Salary', 'Industry', 'Functional Area', 'Role Category', 
#                 'Design Role', 'Skills', 'Company Name',
#                 'UG','PG','Doctorate']

# naukri_df = naukri_df.reindex(columns=column_names)        
# with open('naukri_dataframe.pkl', 'wb') as f:
#     cPickle.dump(naukri_df, f)


# In[ ]:


# with open('naukri_dataframe.pkl', 'r') as f:
#     naukri_df = cPickle.load(f)

