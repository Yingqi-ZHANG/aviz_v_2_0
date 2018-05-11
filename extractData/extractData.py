
# coding: utf-8

# In[2]:

import extractDataString
import pdfToString
import rtfToString
import re
import getFileFromZotero
import pandas as pd
import sys


# In[26]:

#connecter avec MongoDB
import pymongo

avizDB = pymongo.MongoClient(host='localhost',port=27017)

#name of database
db = avizDB.canton

#define the collection
collection = db['metaData']


# In[3]:

#filePathRoot="H:/application/zoteroFichier/export/test/"
filePathRoot = sys.argv[1]
print(sys.argv)


# In[4]:

docFile = pd.DataFrame()
docFile = getFileFromZotero.getDocFileList(filePathRoot)


# In[37]:

for index,doc in docFile.iterrows():
    fileName = doc['attFilePath']
    fileType = fileName.split('.')[-1]
    
    #transformer les fichiers de type different en string
    if(('rtf' == fileType) or ('RTF' == fileType)):
        textString = rtfToString.convert(fileName)
    elif(('pdf' == fileTyoe) or ('PDF' == fileType)):
        textString
        
    #verifier le type de document et obtenir les metadonnées    
    docType = extractDataString.checktype(textString)
    textJson = extractDataString.extractDataByType(docType,textString)
       
    #enregister les données dans mongoDB
    textJson['docName'] = doc['docName']
    textJson['docUrl'] = doc['docUrl']
    textJson['_id'] = doc['docUrl']
    textJson['attFilePath'] = doc['attFilePath']
    textJson['path'] = doc['path']
    textJson['pathKey'] = list(filter(lambda x: x and x.strip(), doc['path'].split('/')))
            
    collection.replace_one({'_id':doc['docUrl']},textJson,upsert=True)    
    print(index)
    for item in textJson:
        if list == type(textJson[item]):
            print(item," : ")
            for i in textJson[item]:    
                print(i)
        else:
            print(item,': ', textJson[item]) 
     


# In[19]:




# In[ ]:




# In[ ]:




# In[3]:




# In[ ]:



