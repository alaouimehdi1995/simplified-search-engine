from PersonnalParser import PersonnalParser
"""
This file should be executed when you would feed your database.
Defined variables below:
    - proxies: If you use a proxy, enter correspondant parameters, else, switch it to None (proxies= None)
    - startURL: It represent the start URL of crawling.
    - maximumCrawlTreeDepth: maximum depth of the crawling tree
    - startThread: It's the Thread that would treat the startURL, after, for each link found, it will start a new Thread
"""

proxies = {"http": "http://10.23.201.11:3128",
           "https": "http://10.23.201.11:3128"}

startURL="http://www.avito.ma/fr/maroc/informatique_et_multimedia-%C3%A0_vendre"

maximumCrawlTreeDepth=5

startThread=PersonnalParser()
startThread.setURL(startURL)  # Set startURL as the URL that should be treated in the "startThread" thread
startThread.setProxy(proxies) # Setting the Proxy
startThread.setMaxDepth(maximumCrawlTreeDepth) # Setting the maximum depth of the crawling tree
startThread.start() # Starting the process
