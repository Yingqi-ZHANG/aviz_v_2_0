
# coding: utf-8

# In[1]:

from xml.dom.minidom import parse
import xml.dom.minidom
import pandas as pd
import numpy as np


# In[2]:

#filePathRoot="H:/application/zoteroFichier/export/test/"


# In[ ]:

#DOMTree = xml.dom.minidom.parse("H:/application/zoteroFichier/export/test/test.rdf")
#allNodes = DOMTree.documentElement


# In[8]:

#table = getDocFileList(filePathRoot)


# In[9]:

#table


# In[3]:

def getDocFileList(filePathRoot):
    rdfFile = list(filter(lambda x: x and x.strip(), filePathRoot.split('/')))[-1]+'.rdf'
    DOMTree = xml.dom.minidom.parse(filePathRoot+rdfFile)
    allNodes = DOMTree.documentElement
    zCollection = pd.DataFrame()
    bibDoc = pd.DataFrame()
    zAttachement = pd.DataFrame()
    bibDoc = pd.DataFrame()
    zCollection,colDoc = getColEtColdoc(allNodes)
    zAttachement = getAtt(allNodes,filePathRoot)
    bibDoc = getDoc(allNodes)
    bibDoc = bibDoc.merge(zAttachement,on='attLink')[['docName','docUrl','attFilePath']]
    colDoc = colDoc.merge(zCollection,on='colId')[['docUrl','path']]
    bibDoc = bibDoc.merge(colDoc,on='docUrl')
    return bibDoc


# In[4]:

def collectionPath(rootId,zCollection):
    root = zCollection[(zCollection['colId']==rootId)]
    subcolIds = root['subcolId']
    for subcolId in subcolIds:
        colName = zCollection[zCollection['colId']==subcolId]['name']
        zCollection.loc[zCollection['colId']==subcolId,'path']= root['path']+colName+'/'
        if (zCollection[zCollection['colId']==subcolId]['subcolId'].notnull().values.any()):
            zCollection = collectionPath(subcolId,zCollection)
    return zCollection


    


# In[5]:

def getColEtColdoc(xmlDomElement): 
    zCollectionsXMl = xmlDomElement.getElementsByTagName("z:Collection")
    zCollection = pd.DataFrame()
    colDoc = pd.DataFrame()
    for collection in zCollectionsXMl:
        colName = collection.getElementsByTagName('dc:title')[0].childNodes[0].nodeValue
        #print(colName)
        colId = collection.attributes.item(0).value
        subcols = collection.getElementsByTagName('dcterms:hasPart')
        for subcol in subcols:
            subcolId = subcol.attributes.item(0).value
            if subcolId.startswith('#collection'):
                colInfo = pd.DataFrame()
                colInfo['name']=[colName]
                colInfo['colId']=[colId]
                colInfo['subcolId']=[subcolId]
                colInfo['path']=['']
                zCollection = zCollection.append(colInfo)
            else :
                colDocInfo = pd.DataFrame()
                colDocInfo['colId'] = [colId]
                colDocInfo['docUrl']=[subcolId]
                colDoc = colDoc.append(colDocInfo)
                colInfo = pd.DataFrame()
                colInfo['name']=[colName]
                colInfo['colId']=[colId]
                colInfo['path']=['']
                zCollection = zCollection.append(colInfo)
    zCollection = zCollection.drop_duplicates()
    colDoc = colDoc.drop_duplicates()
    rootId = (set(zCollection['colId'].unique())-set(zCollection['subcolId'].unique())).pop()
    zCollection.loc[zCollection['colId']==rootId,'path'] = zCollection[zCollection['colId']==rootId]['name']+'/'
    zCollection = collectionPath(rootId,zCollection)
    return zCollection, colDoc


# In[6]:

def getAtt(xmlDomElement,filePathRoot):
    zAttachementsXML= xmlDomElement.getElementsByTagName('z:Attachment')
    zAttachement = pd.DataFrame()
    for att in zAttachementsXML:
        attLink = att.attributes.item(0).value
        attFilePath = att.getElementsByTagName("filepath")[0].attributes.item(0).value
        attInfo = pd.DataFrame()
        attInfo['attLink']=[attLink]
        attInfo['attFilePath']=[filePathRoot+attFilePath]
        zAttachement = zAttachement.append(attInfo)
    return zAttachement


# In[7]:

def getDoc(xmlDomElement):
    bibDocsXML= xmlDomElement.getElementsByTagName("bib:Document")
    bibDoc = pd.DataFrame()
    for doc in bibDocsXML:
        docName = list(filter(lambda x:x.nodeName == "dc:title",doc.childNodes))[0].childNodes[0].nodeValue
        docUrl = doc.getElementsByTagName("dc:identifier")[0].getElementsByTagName("rdf:value")[0].childNodes[0].nodeValue
        docLink = doc.getElementsByTagName("link:link")[0].attributes.item(0).value
        docInfo = pd.DataFrame()
        docInfo['docName']=[docName]
        docInfo['docUrl']=[docUrl]
        docInfo['attLink']=[docLink]
        bibDoc=bibDoc.append(docInfo)
    return bibDoc


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



