from urllib.request import urlopen, HTTPError, urlretrieve
from urllib.error import URLError
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
import time

def rasparXML(itemFinal,pasta):
    item = itemFinal.find_all('td')    
    for issue in item:
        try:
            linkissue = issue.find('a')['href']
            print('Acessando a edição: ' + linkissue +'\n')
            req = urlopen(linkissue)
            bs = BeautifulSoup(req.read(), 'lxml')
            tabelaGeral = bs.find(class_='content')
            linkArtigos = tabelaGeral.find_all('a',href=re.compile(r'script=sci_arttext'))
            for artigo in linkArtigos:
                link = artigo['href']
                req = urlopen(link)
                bs = BeautifulSoup(req.read(), 'lxml')
                li = bs.find_all('li')
                listaId = []
                for i in li:
                    try:
                        idArtigo = i.find('a',href=re.compile(r'/pdf/[a-z]*/'))
                        idArtigo = idArtigo['href']
                        listaId.append(idArtigo)
                    except:
                        pass                
                idFinal = listaId[0].replace('/pdf/', '')
                idFinal = idFinal.replace('.pdf','')
                idFinal = idFinal.replace('/','_')
                fullName = idFinal+'.xml'
                for t in li:
                    try:
                        xmlLink = t.find('a',href=re.compile(r'/php/articleXML.php'))
                        xml = f'{xmlLink["href"]}.xml'
                        path = os.path.join(pasta, fullName)
                        if not os.path.exists(path):
                            urlretrieve(xml, path)
                    except:
                        pass
        except:
            pass
