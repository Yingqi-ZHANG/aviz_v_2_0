
# coding: utf-8

# In[1]:

from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter


# In[4]:

def convert(path):
    file = open(path,'rb')
    doc = Rtf15Reader.read(file)
    text = PlaintextWriter.write(doc).getvalue()
    file.close()
    return text


# In[ ]:

#test
#t=convert("Cour de Cassation, Chambre criminelle, du 1 décemb.RTF")
#print(t)

