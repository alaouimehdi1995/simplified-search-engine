import re
import requests
from threading import Thread
import pymongo

class PersonnalParser(Thread):
    depth = 0
    maxDepth = 0
    text=""
    links=[]
    stopChars = ["'", '"', '-', '—', '+', '*', '=', '.', '/', '(', ')', '[', ']', '{', '}', '|', ',', ';', ':', '¶', '!', '?', '&', '#', '$', '_', '\\']
    stopWords = ["a", "an", "or", "not", "for", "in", "with", "the", "out", "on", "to"]
    def setURL(self,url):
        self.URL=url

    def setProxy(self,proxy):
        self.proxy=proxy

    def setDepth(self,depth):
        self.depth=depth

    def setMaxDepth(self,max):
        self.maxDepth=max

    def setStopChars(self,stopChars):
        TempList=[]
        for c in stopChars:
            if c in ['^','$','?','!','+','*','.','(',')','[',']','{','}','|','\\']:
                c='\\'+c
            TempList.append(c)
        self.stopChars="("+'|'.join(TempList)+")"

    def setStopWords(self,stopwords):
        self.stopWords=stopwords


    def getDictionnary(self):
        dictionnary={}
        List = self.text.split(" ")
        while len(List) > 0:
            word = List.pop(0)
            try:
                dictionnary[word] = dictionnary[word] + 1
            except:
                dictionnary[word] = 1
        return dictionnary





    def parse(self):

        htmlContent = requests.get(self.URL, proxies=self.proxy) # On récupère la page html
        encoding=htmlContent.encoding
        if encoding==None:
            encoding="utf-8"
        htmlContent=htmlContent.content.decode(encoding) # On la décode
        htmlContent= re.sub(r'<script(.)*>[^<]*</script>', r'', htmlContent, flags=re.IGNORECASE | re.MULTILINE) #On supprime le code JS

        links = re.findall('a href="(http[^"]*)"', htmlContent, flags=re.IGNORECASE | re.DOTALL) #On recupère les balises <a href>
        self.links = [re.sub(r'a href="(http[^"]*)"', r'\1', element, re.IGNORECASE) for element in links] #On en retient le lien
        self.setStopChars(self.stopChars)
        self.setStopWords(self.stopWords)


        self.text=re.sub(r'<[^>]*>',r'',htmlContent,flags=re.IGNORECASE | re.MULTILINE) #On supprime les balises
        self.text = re.sub('(?!((19[0-9]{2}|20[0-9]{2})))([0-9]+)', ' ',self.text,flags=re.IGNORECASE | re.MULTILINE)  # On supprime tout les nombres à part les années (dates)
        self.text = re.sub(self.stopChars,' ',self.text,flags=re.IGNORECASE | re.MULTILINE)  # On supprime tout les stopchars
        self.text = re.sub('(\s)+', ' ',self.text)  # On supprime tout les espaces et retours à la ligne par un seul espace
        self.text=self.text.lower() #On met le tout en minuscule
        self.text = re.sub(' ([a-z]{1} )+', ' ', self.text,flags=re.IGNORECASE | re.MULTILINE)  # On supprime tout les stopWords

        TempListe=[]
        for e in self.text.split(' '):
            if e not in self.stopWords:
                TempListe.append(e)
        self.text=' '.join(TempListe)

        #Fin du traitement
    def getText(self):
        return self.text
    def getLinks(self):
        return self.links
    def getURL(self):
        return self.URL

    def run(self):
        self.parse()
        texte = self.getText()
        content=self.getDictionnary()
        try:
            client = pymongo.MongoClient('mongodb://localhost:27017/')  # On se connecte à la BD
            db = client['crawl']
            collection = db['crawl']
            collection.insert_one({'_id': self.URL, 'Content': content})  # On y insère le résultat
            print("Inserted URL >", self.URL)
        except:
            print("",end="")
        links = self.getLinks()  # On obtient les liens
        if self.depth <= self.maxDepth:
            for link in links:  # On crée à chaque lien de la liste un Thread pour traiter son contenu

                T = PersonnalParser()
                T.setProxy(self.proxy)
                T.setURL(link)
                T.setDepth(self.depth + 1)
                T.setMaxDepth(self.maxDepth)
                T.start()

















