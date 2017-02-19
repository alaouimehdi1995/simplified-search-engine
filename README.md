# Simplified Searching Engine
##that crawls, scrapps, indexes data and stores it into a database##
The program is written in Python Language, uses regex to parse HTML, and MultiThreading to go faster. The database part is assured by MongoDB
The Project contains 3 files:
###PersonnalParser.py:###
  - Contains PersonnalParser class, that gets HTML content, parses it, stores it and starts new PersonnalParser Thread for each link in the page content.

###fill_database.py:###
  - Contains the general settings like start URL, proxy settings and depth search. The first crawl Thread starts here.

###main.py###
  - Contains the code that gets the user search, gets the database content and sorts the results by relevance.
