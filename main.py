"""
Simplified Searching Engine, conceived and implemented by: ALAOUI Mehdi 2017
"""
from DBManager import DBManager
from math import pow

"""
This file should be executed when user want to search something and getting the results.
Defined functions below:
    - getScore: function that calculate score of wordList given in parameters into savedWebSite (also given)
Defined variables below:
    - resultsPerPage: number of results that will be shown in one page
    - sentence: a list of words searched by user
    - dbManager: an object that will be the interface with the database
    - databaseContent: a list of websites saved into our database
    - results: a sorted list of results
"""
def getScore(savedWebSite, wordList):
    score = 0
    nb_mots_trouves=0
    nb_titre_trouve=0

    for word in wordList:
        if word in savedWebSite['_id']:
            nb_titre_trouve += 1
        if savedWebSite['title']!= None:
            if word in savedWebSite['title']:
                nb_titre_trouve+=1

        try:
            score += savedWebSite['index'][word]
            nb_mots_trouves+=1
        except:
            pass
    score=score*nb_mots_trouves
    score=score*pow(10,nb_titre_trouve)
    return score


resultsPerPage=15



print("Entrez la phrase à chercher")
sentence=str(input()).lower()
sentence=sentence.split(' ')



dbManager=DBManager()
dbManager.setHost('localhost')
dbManager.setPort(27017)
dbManager.setDBName('crawl')
dbManager.setTableName('crawl')
dbManager.connect()
databaseContent=dbManager.find()


results=[]

for webSite in databaseContent:
    structure={'element':webSite,'score':getScore(webSite,sentence)}
    # Structure of structure:
    # { structure:{ '_id':"http://www.youtube.com", 'index':{'word1':occurence1,...}, 'title':'page title','text':'(content text)' }, 'score':13}
    if structure['score']>0:
        results.append(structure)


results=sorted(results,key=lambda structure: structure['score'],reverse=True)

#Printing results

if len(results)>0:
    i=0
    nb=len(results)
    while i < nb:
        limit=resultsPerPage if i+resultsPerPage < nb else nb-i
        for j in range(limit):
            print(i+j+1,") ",end="")
            if(results[i+j]['element']['title']!=None):
                print(results[i+j]['element']['title'])
            print("\t",results[i+j]['element']['_id']," score:",results[i+j]['score'],"\n")
        print("Page: ",int((i/resultsPerPage)+1),"/",int(1+nb/resultsPerPage))
        i+=limit
        input()
else:
    print("Résultats introuvables pour votre recherche")





