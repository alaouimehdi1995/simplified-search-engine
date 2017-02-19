<h1>Simplified Searching Engine</h1>
<h2>that crawls, scrapps, indexes data and stores it into a database</h2>
The program is written in Python Language, uses regex to parse HTML, and MultiThreading to go faster.
The database part is assured by MongoDB
The Project contains 3 files:
<h4><a href="https://github.com/alaouimehdi1995/SimplifiedSearchingEngine/blob/master/PersonnalParser.py">PersonnalParser.py:</a></h4>
  - Contains PersonnalParser class, that gets HTML content, parses it, stores it and starts new PersonnalParser Thread for each link in the page content.

<h4><a href="https://github.com/alaouimehdi1995/SimplifiedSearchingEngine/blob/master/fill_database.py">fill_database.py:</a></h4>
  - Contains the general settings like start URL, proxy settings and depth search. The first crawl Thread starts here.

<h4><a href="https://github.com/alaouimehdi1995/SimplifiedSearchingEngine/blob/master/main.py">main.py</a></h4>
  - Contains the code that gets the user search, gets the database content and sorts the results by relevance.
