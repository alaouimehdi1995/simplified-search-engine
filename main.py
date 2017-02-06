
from MyParser import MyParser
from MyParser import MyThread

proxies = {"http": "http://10.23.201.11:3128",
           "https": "http://10.23.201.11:3128"}

URL="https://fr.wikipedia.org/wiki/Hypertext_Markup_Language"
parser=MyParser()
thread=MyThread()
thread.setURL(URL)
thread.setProxy(proxies)
thread.start()
thread.join()

print("===== Liens ========")
#for link in liens:
    #print("link==>",link)
    #htmlContent2 = requests.get(link, proxies=proxies).content
    #parser.feed(htmlContent2)
    #liens2 = parser.getLinks()
    #for lien in liens2:
    #    print(lien)


