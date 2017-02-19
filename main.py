import pymongo

"""
This file should be executed when user want to search something and getting the results.
Defined functions below:
    - getScore: function that calculate score of wordList given in parameters into savedWebSite (also given)
Defined variables below:
    - sentence: a list of words searched by user
    - client,db,collection: variables used to consult the database
    - databaseContent: a list of websites saved into our database
    - results: a sorted list of results
"""
def getScore(savedWebSite, wordList):
    score = 0
    nb_mots_trouves=0
    for word in wordList:
        try:
            score += savedWebSite['Content'][word]
            nb_mots_trouves+=1
        except:
            pass
    score=score*nb_mots_trouves
    return score





print("Entrez la phrase à chercher")
sentence=str(input()).lower()
sentence=sentence.split(' ')



client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['crawl']
collection = db['crawl']
databaseContent=collection.find()


results=[]

for webSite in databaseContent:
    structure={'element':webSite,'score':getScore(webSite,sentence)}
    # Structure of structure:
    # { structure:{ '_id':"http://www.youtube.com", 'Content':{'word1':occurence1,...} }, 'score':13}
    if structure['score']>0:
        results.append(structure)


results=sorted(results,key=lambda structure: structure['score'],reverse=True)

#Printing results
for e in results:
    print(e['element']['_id']," score:",e['score'])





