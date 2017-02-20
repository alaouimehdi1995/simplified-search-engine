<h1>Simplified Searching Engine</h1>
<h2>that crawls, scraps, indexes data and stores it into a database</h2>
The program is written in Python Language, uses regex to parse HTML, and MultiThreading to go faster.
The database part is assured by MongoDB
The Project contains 3 files:

<h4>PersonnalParser.py:</h4>
  - Contains PersonnalParser class, that gets HTML content, parses it, stores it and starts new PersonnalParser Thread for each link in the page content.
  
<h4>DBManager.py</h4>
  - Contains DBManager class, which assure the connexion with DB and inserting and/or finding operations.
  
<h4>fill_database.py:</h4>
  - Contains the general settings like start URL, proxy settings and depth search. The first crawl Thread starts here.

<h4>main.py</h4>
  - Contains the code that gets the user search, gets the database content and sorts the results by relevance.
