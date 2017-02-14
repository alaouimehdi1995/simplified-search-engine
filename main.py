from MyParser import MyThread

proxies = {"http": "http://10.23.201.11:3128",
           "https": "http://10.23.201.11:3128"}

URL="https://github.com/"


thread=MyThread()
thread.setURL(URL)
thread.setProxy(None)
thread.setDepth(1)
thread.setMaxDepth(5)
thread.start()


"""
Le programme prend en paramètre une URL initiale, il récupère le contenu (texte et liens)
Il filtre le texte des balises, des stopwords et insère le tout dans la base de données MongoDB, et crée pour chaque lien de la page un thread correspondant,
récupère son contenu etc.

Reste à faire: Ajout d'une fonction qui prend en paramètre un texte et nous rend un dictionnaire (clé=le mot, valeur=nombre d'occurences du mot)


"""


