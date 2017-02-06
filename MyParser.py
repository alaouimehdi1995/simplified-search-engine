from html.parser import HTMLParser
import re
import requests
from threading import Thread
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

    def getText(self):
        #On regroupe les span juxtaposés, et les textes (p) justaposés
        i=0
        while(i<len(self.texts)):
            j=i+1
            while(j<len(self.texts) and self.texts[i][0]==self.texts[j][0]):
                self.texts[i][1]+=self.texts[j][1]
                del self.texts[j]
            i+=1
        # On supprime les tabulations et les retours à la ligne
        for element in self.texts:
            element[1]=' '.join(element[1].split('\n')) # On supprime les retours à la ligne
            element[1] = ' '.join(element[1].split('\t')) # On supprime les tabulations
            element[1] = ' '.join(element[1].split('\r'))  # On supprime les tabulations
            element[1] = re.sub('( )+', ' ', element[1])
        return self.texts

    def getTitles(self):
        newTitles=[]
        for element in self.titles:
            e =' '.join(element.split('\n')) # On supprime les retours à la ligne
            e = ' '.join(e.split('\t')) # On supprime les tabulations
            e = ' '.join(e.split('\r'))  # On supprime les tabulations
            e = re.sub('( )+', ' ', e)
            if(e!="" and e!=" "):
                newTitles.append(e)
        self.titles=newTitles
        return self.titles

class MyThread(Thread):
    URL = None
    proxies = None
    parser= MyParser()

    def setURL(self, URL):
        self.URL = URL

    def setProxy(self, proxies):
        self.proxies = proxies

    def setParser(self,Parser):
        self.parser=Parser
    def run(self):
        try:
            htmlContent = requests.get(self.URL, proxies=self.proxies).content.decode("utf-8")
            self.parser.feed(htmlContent)
            links=self.parser.getLinks() #On obtient les liens
            for link in links: #Pour chaque lien

                print(">",link) #On l'affiche, on crée un Thread, et on récupère son contenu
                T=MyThread()
                T.setProxy(self.proxies)
                T.setURL(link)
                T.setParser(self.parser)
                T.start()

        except:
            print("",end="")