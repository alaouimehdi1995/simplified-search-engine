from MyParser import PersonnalParser
import pymongo

proxies = {"http": "http://10.23.201.11:3128",
           "https": "http://10.23.201.11:3128"}

URL="https://www.microsoftstore.com/store/msusa/en_US/cat/categoryID.69405400?icid=en_US_Store_UH_devices_Xbox"


"""
#Pour le remplissage de la base de données

thread=PersonnalParser()
thread.setURL(URL)
thread.setProxy(proxies)
thread.setDepth(1)
thread.setMaxDepth(5)
thread.start()

"""

#Pour la recherche dans la base de données
print("Entrez le mot à chercher")
word=str(input()).lower()
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['crawl']
collection = db['crawl']
cursor = collection.find({'Content.'+word: {"$exists": True}},sort=[(str('Content.'+word), pymongo.DESCENDING)])
if cursor.count() > 0:
    print("le mot existe dans la bd:")
    for e in cursor:
        print("> ",e['_id'],", Nombre d'occurences:",e['Content'][word])
else:
    print("Le mot n'existe pas")


"""
Le programme prend en paramètre une URL initiale, il récupère le contenu (texte et liens)
Il filtre le texte des balises, des stopwords et insère le tout dans la base de données MongoDB, et crée pour chaque lien de la page un thread correspondant,
récupère son contenu etc.

La partie recherche consulte la base de données et affiche les résultats selon le nombre d'occurences
Reste à faire: plus de pertinence des données
"""


