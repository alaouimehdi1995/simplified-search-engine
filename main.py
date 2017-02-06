
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

"""
Le programme prend en paramètre une URL initiale, il récupère le contenu (texte et liens)
Il filtre le texte dans un tableau, et crée pour chaque lien de la page un thread correspondant,
récupère son contenu etc.

Il reste à filtrer l'unicité des liens et la gestion des bases de données (stockage)

"""


