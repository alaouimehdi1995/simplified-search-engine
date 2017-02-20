"""
Simplified Searching Engine, conceived and implemented by: ALAOUI Mehdi 2017
"""
from PersonnalParser import PersonnalParser
from DBManager import DBManager
"""
This file should be executed when you would feed your database.
Defined variables below:
    - proxies: If you use a proxy, enter correspondant parameters, else, switch the setter into no_proxies
    - startURL: It represent the start URL of crawling.
    - maximumCrawlTreeDepth: maximum depth of the crawling tree
    - startThread: It's the Thread that would treat the startURL, after, for each link found, it will start a new Thread
    - dbManager: Object that will be the interface with database(write and read from database)
"""

proxies = {"http": "http://10.23.201.11:3128",
           "https": "http://10.23.201.11:3128"}

no_proxies = {"http": None,
           "https": None}

startURL="http://www.hespress.com/"
maximumCrawlTreeDepth=5


dbManager=DBManager()
dbManager.setHost('localhost')
dbManager.setPort(27017)
dbManager.setDBName('crawl')
dbManager.setTableName('crawl')
dbManager.connect()



startThread=PersonnalParser()
startThread.setURL(startURL)  # Set startURL as the URL that should be treated in the "startThread" thread
startThread.setProxy(no_proxies) # Setting the Proxy
startThread.setDBManager(dbManager)
startThread.setMaxDepth(maximumCrawlTreeDepth) # Setting the maximum depth of the crawling tree
startThread.start() # Starting the process
