from MyParser import PersonnalParser
proxies = {"http": "http://10.23.201.11:3128",
           "https": "http://10.23.201.11:3128"}

URL="http://www.avito.ma/fr/maroc/informatique_et_multimedia-%C3%A0_vendre"

#Pour le remplissage de la base de données

thread=PersonnalParser()
thread.setURL(URL)
thread.setProxy(proxies)
thread.setDepth(1)
thread.setMaxDepth(5)
thread.start()
