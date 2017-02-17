import pymongo


def getScore(element, wordList):
    score = 0
    nb_mots_trouves=0
    for word in wordList:
        try:
            score += element['Content'][word]
            nb_mots_trouves+=1
        except:
            print("", end="")
    score=score*nb_mots_trouves
    return score




#Pour la recherche dans la base de données
print("Entrez la phrase à chercher")
sentence=str(input()).lower()
sentence=sentence.split(' ')

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['crawl']
collection = db['crawl']

# Structure: {structure:{notre structure},score:13}
cursor=collection.find()
results=[]
for e in cursor:
    structure={'element':e,'score':getScore(e,sentence)}
    if structure['score']>0:
        results.append(structure)
results=sorted(results,key=lambda structure: structure['score'],reverse=True)
for e in results:
    print(e['element']['_id']," score:",e['score'])


"""
Le programme prend en paramètre une URL initiale, il récupère le contenu (texte et liens)
Il filtre le texte des balises, des stopwords et insère le tout dans la base de données MongoDB, et crée pour chaque lien de la page un thread correspondant,
récupère son contenu etc.

La partie recherche consulte la base de données et affiche les résultats selon le nombre d'occurences
Reste à faire: plus de pertinence des données
"""


