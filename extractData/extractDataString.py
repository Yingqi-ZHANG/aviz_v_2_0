
# coding: utf-8

# In[1]:

import re


# In[2]:

CNSPattern = 'Commission Nationale des Sanctions'
ACPRPattern = '(AUTORITÉ) DE CONTR(Ô|O)LE PRUDENTIEL ?e?t? ?d?e? ?r?é?s?o?l?u?t?i?o?n? ?(?: \n)* ?Commission des Sanctions'
CCASSPattern = 'Cours de cassation' 


# In[3]:

def checktype(text):
    #regCheckCNS = re.search(CNSPattern,text,re.I)
    #regCheckACPR = re.search(ACPRPattern,text,re.I)
    if(not(re.search(CNSPattern,text,re.I) is None)):
        return 'CNS'
    elif(not(re.search(ACPRPattern,text,re.I) is None)):
        return 'ACPR'
    elif(not(re.search(CCASSPattern,text,re.I is None))):
        return 'CCASS'


# In[8]:

def metaDataCNS(textType,text):
    numdossier = re.search(' Dossier n(?:°|o) (\d\d\d\d-\d\d)',text,re.I)
    dateaudiencecns = re.search(' Audience du (\d* \S* \d*)',text,re.I)
    datedecisioncns = re.search(' D(?:e|é)cision rendue le (\d* \S* \d*)',text,re.I)
    president = re.search('en la présence de (.*) en sa qualité de président',text,re.I)
    cns = re.search('CNS\S,? (.*);',text,re.I)
    textecns = re.search('vu le (code .*)notamment ses (.*) et ([A-Z]\.\d+-\d+ ?);',text,re.I)
    resume = re.search(' ni adjonction ?\S? ?\n?([\S\f \n]*)Fait à',text,re.I)
    myjson = {"FileNumber" : numdossier,
        "AudienceDate" : dateaudiencecns,
        "DecisionDate" : datedecisioncns,
        "President" : president,
        "Commission" : cns,
        "Text" : textecns,
        "Minutes" : resume }
    for item in myjson:
        if myjson[item] != None:
            myjson[item] = myjson[item].group(1)
        else:
            myjson[item] =""
    return myjson
    
def metaDataACPR(textType,text):
    misencause = re.search('(?:Décision.*)*(?:\n)*(?:Le Conseil.*)*(?:\n)*(?:.*a formé*.*)*(?:\n)*(.*)(?:\n)*(?:-|_)*(.*)(?:\n)*(.*)(?:\n)*procédures?',text,re.I)
    procnumber = re.search('procédures? n(?:o|°)s? (\d\d\d\d-\d\d ?e?t? ?\d?\d?\d?(?:\d-)?\d?\d? ?b?i?s?)',text,re.I)
    dateaudienceacpr = re.search('(?:audition|audience) du (.*\d\d\d\d)(?: |\n)* *.*rendu',text,re.I)
    datedecisionacpr = re.search('(?:audition|audience).*(?:\n)*.*rendue? le (.*\d\d\d\d)(?:\n)*',text,re.I)
    quantum = re.search('procédures? n(?:o|°)s? \d\d\d\d-\d\d(?: et \d\d\d\d-\d\d)?(?:bis)? *(?:\n)*(.*)(?:\n)*(.*)(?:\n)*(.*)(?:\n)*(.*)(?:audience|audition)',text,re.I)
    presidentacpr = re.search(' de (.*), Président',text,re.I)
    commission = re.search(', Président, e?t? ?d?e? ?(.*)',text,re.I)
    grief = re.search('notification des? griefs du (\d+ \S+ \d+)',text,re.I)
    collegerep = re.search('\d+ par lesquels (.*), représentant du collège',text,re.I)
    rapporteur = re.search('\d+,? de (.*), rapporteur',text,re.I)
    texteacpr = re.search('vu le(?: )*(Code .*)',text,re.I)
    myjson = {"Questioned" : misencause,
        "FileNumber" : procnumber,
        "AudienceDate" : dateaudienceacpr,
        "DecisionDate" : datedecisionacpr,
        "Quantum" : quantum,
        "President" : presidentacpr,
        "Commission" : commission,
        "GriefNotificationDate" : grief,
        "CollegeRepresentant" : collegerep,
        "Reporter" : rapporteur,
        "Text" : texteacpr}
    for item in myjson:
        if myjson[item] != None:
            myjson[item] = myjson[item].group(1)
        else:
            myjson[item] =""
                
    return myjson


# In[25]:

def metaDataCCASS(textType,text):
    nomCour=re.search('cour de cassation(?: |\n)*(chambre criminelle|chambre civile)',text,re.I)
    dateDecision=re.search('audience publique du (.*)(?:\n)',text,re.I)
    numPourvoi=re.search('N° de pourvoi: (\d\d-\d\d\d\d\d)\n',text,re.I)
    publication=re.search('(?:\n)*(Non publié au bulletin|Inédit|publié au bulletin)(?:\n)*',text,re.I)
    solution=re.search('(?:\n)+(Rejet|Cassation|Cassation Partielle)(?:\n)+',text,re.I)
    if solution != None:
        president=re.search(solution.group(1)+'(?:\n)*(?:président :)?(.*)(?: \(président\))?(?:, président)(?:\n)+',text,re.I)
    else:
        president = re.search('(?:\n)*(?:président :)?(.*)(?: \(président\))?(?:, président)(?:\n)+',text,re.I)
    decisionAttquee=re.search('Décision attaquée ?:(.*)(?:\n)+',text,re.I)
    tirages=re.search('Titrages et résumés : (.*)(?:\n)+',text,re.I)
    if tirages != None:
        resumee=re.search(tirages.group(1)+'(?:\n)+(.*)(?:\n)+',text,re.I)
    else:
        resumee=None
    precedent=re.search('(?:\n)+Précédents jurisprudentiels : (.*)(?:\n)+',text,re.I)
    ecli=re.search('(?:\n)+(ECLI:(?:\w)+:(?:\w)+:(?:\d){4}:(?:\w|\d|.){0,25})(?:\n)+',text,re.I)
    myjson={
        "Nom de la cour":nomCour,
        "Date de la décision":dateDecision,
        "Numéro de pourvoi":numPourvoi,
        "Publication":publication,
        "Solution":solution,
        "Président":president,
        "Décision attaquée":decisionAttquee,
        "Tirages":tirages,
        "Résumée":resumee,
        "Précédents jurisprudentiels":precedent,
        "ECLI" :ecli
    }
    for item in myjson:
        if myjson[item] != None:
            myjson[item] = myjson[item].group(1)
        else:
            myjson[item] =""
    if myjson['Tirages'] != "":
        myjson['Tirages'] = myjson['Tirages'].split(" - ")
     
    return myjson
    


# In[ ]:




# In[26]:

def extractDataByType(textType,text):
    if('CNS' == textType):
        myjson=metaDataCNS(textType,text)   
        
    if('ACPR' == textType):
        myjson=metaDataACPR(textType,text)
        
    if('CCASS' == textType):
        myjson=metaDataCCASS(textType,text)
        
    myjson['DocumentType']=textType
    return myjson
        



# In[ ]:



