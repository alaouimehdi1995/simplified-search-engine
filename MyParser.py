from html.parser import HTMLParser
import re
import requests
from threading import Thread
import pymongo

class MyParser(HTMLParser):

    itsText=False
    itsSpan=False
    itsH1=False
    itsH2=False
    itsH3=False
    itsH4=False
    itsH5=False
    links=[]
    texts=[]
    titles=[]


    def handle_starttag(self, tag, attrs):
        if(tag=='a'):
            for attr in attrs:
                if(attr[1][:4]=="http"):
                    self.links.append(attr[1])
        elif(tag=='p'):
            self.itsText=True
        elif(tag=="span"):
            self.itsSpan=True
        elif(tag=="h1"):
            self.itsH1=True
        elif (tag == "h2"):
            self.itsH2 = True
        elif (tag == "h3"):
            self.itsH3 = True
        elif (tag == "h4"):
            self.itsH4 = True
        elif (tag == "h5"):
            self.itsH5 = True

    def handle_data(self, data):
        if (self.itsSpan):
            #Lorsqu'on trouve une balise span
            self.texts.append(["span", data])
        if(self.itsText):
            #Lorsqu'on trouve une balise texte (p)
            self.texts.append(["p",data])
        if(self.itsH1 or self.itsH2 or self.itsH3 or self.itsH4 or self.itsH5):
            #Lorsqu'on trouve une balise titre (h1..h5)
            self.titles.append(data)

    def handle_endtag(self, tag):
        if(tag=='p'):
            self.itsText=False
        elif(tag=="span"):
            self.itsSpan=False
        elif (tag == "h1"):
            self.itsH1 = False
        elif (tag == "h2"):
            self.itsH2 = False
        elif (tag == "h3"):
            self.itsH3 = False
        elif (tag == "h4"):
            self.itsH4 = False
        elif (tag == "h5"):
            self.itsH5 = False

    def getLinks(self):
        return self.links

    def traitementTexte(self,texts):
        #On concatène tout les paragraphes de la page
        stopWords=["and","or",".",",","et","à","a","(",")","[", "]",":",";","\"","'"]
        stopChars=[".",",","(",")","[", "]",":",";","\"","'"]
        texte=""
        for i in range (0,len(texts)):
            texte+=texts[i][1]+" "
        # On supprime les tabulations et les retours à la ligne
        texte=' '.join(texte.split('\n')) # On supprime les retours à la ligne
        texte = ' '.join(texte.split('\t')) # On supprime les tabulations
        texte = ' '.join(texte.split('\r'))  # On supprime les tabulations
        texte = re.sub('( )+', ' ', texte) # On remplace une série d'espaces par un seul

        liste=[l for l in texte.split(' ') if (l not in stopWords)] #On supprime les stopwords
        texte=' '.join(liste)

        for sc in stopChars: #On supprime les caractères qui ne servent à rien
            texte=''.join(texte.split(sc))

        return texte

    def getText(self):
        texte=self.traitementTexte(self.texts)

        return texte

    def getTitles(self):
        titres=self.traitementTexte(self.titles)
        return titres

class MyThread(Thread):
    depth=0
    maxDepth=0
    URL = None
    proxies = None
    parser= MyParser()

    def setURL(self, URL):
        self.URL = URL

    def setProxy(self, proxies):
        self.proxies = proxies

    def setParser(self,Parser):
        self.parser=Parser

    def setDepth(self,depth):
        self.depth=depth

    def setMaxDepth(self,max):
        self.maxDepth=max

    def run(self):
        try:
            htmlContent = requests.get(self.URL, proxies=self.proxies).content.decode("utf-8")
            print("contenu extrait")
            self.parser.feed(htmlContent)
            texte = self.parser.getText() # On extrait le texte traité
            titles= self.parser.getTitles() # Les titres traités aussi
            print("URL >", self.URL)
            try:
                client = pymongo.MongoClient('mongodb://localhost:27017/') #On se connecte à la BD
                db = client['crawl']
                collection = db['crawl']
                collection.insert_one({'_id': self.URL, 'Text': texte,'Titles':titles}) #On y insère le résultat
            except:
                print("writing error")
            links=self.parser.getLinks() #On obtient les liens
            if self.depth<=self.maxDepth:
                for link in links: #Pour chaque lien

                    #print(">",link) #On l'affiche, on crée un Thread, et on récupère son contenu
                    T=MyThread()
                    T.setProxy(self.proxies)
                    T.setURL(link)
                    T.setParser(self.parser)
                    T.setDepth(self.depth+1)
                    T.setMaxDepth(self.maxDepth)
                    T.start()

        except:
            print("error\n",end="")








