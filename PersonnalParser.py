import re
import requests
from threading import Thread
import pymongo

class PersonnalParser(Thread):
    depth = 1
    maxDepth = 1
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

        htmlContent = requests.get(self.URL, proxies=self.proxy) #Getting the HTML content of the webpage
        encoding=htmlContent.encoding
        if encoding==None:
            encoding="utf-8"
        htmlContent=htmlContent.content.decode(encoding) # Decoding it into it's format (utf-8 by default)
        htmlContent= re.sub(r'<script(.)*>[^<]*</script>', r'', htmlContent, flags=re.IGNORECASE | re.MULTILINE) # Removing JavaScript Code

        links = re.findall('a href="(http[^"]*)"', htmlContent, flags=re.IGNORECASE | re.DOTALL) #Getting the <a href > tags
        self.links = [re.sub(r'a href="(http[^"]*)"', r'\1', element, re.IGNORECASE) for element in links] #Saving the link inside
        self.setStopChars(self.stopChars)
        self.setStopWords(self.stopWords)


        self.text=re.sub(r'<[^>]*>',r'',htmlContent,flags=re.IGNORECASE | re.MULTILINE) #Removing all tags
        self.text = re.sub('(?!((19[0-9]{2}|20[0-9]{2})))([0-9]+)', ' ',self.text,flags=re.IGNORECASE | re.MULTILINE)  # Removing numbers excepting years
        self.text = re.sub(self.stopChars,' ',self.text,flags=re.IGNORECASE | re.MULTILINE)  # Removing stop characters
        self.text = re.sub('(\s)+', ' ',self.text)  # Remplacing multiple spaces by just one
        self.text=self.text.lower()
        self.text = re.sub(' ([a-z]{1} )+', ' ', self.text,flags=re.IGNORECASE | re.MULTILINE)  # Deleting stop words

        TempListe=[]
        for e in self.text.split(' '):
            if e not in self.stopWords:
                TempListe.append(e)
        self.text=' '.join(TempListe)

        #TEnd of treatment
    def getText(self):
        return self.text
    def getLinks(self):
        return self.links
    def getURL(self):
        return self.URL

    def run(self):
        self.parse()
        self.getText()
        content=self.getDictionnary()

        try:
            client = pymongo.MongoClient('mongodb://localhost:27017/')  # Connecting to DB
            db = client['crawl']
            collection = db['crawl']
            collection.insert_one({'_id': self.URL, 'Content': content})  # Writing into DB
            print("Inserted URL >", self.URL)
        except:
            pass
        links = self.getLinks()  # Getting links
        if self.depth <= self.maxDepth: # If we are not exceeding the maximum depth
            for link in links:  # For each link, we create a Thread that will treat it

                T = PersonnalParser()
                T.setProxy(self.proxy)
                T.setURL(link)
                T.setDepth(self.depth + 1)
                T.setMaxDepth(self.maxDepth)
                T.start()

















