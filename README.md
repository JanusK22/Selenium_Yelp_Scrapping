# Selenium_Yelp_Scrapping
Webscraping of Shops with Selenium in Yelp


There is 3 modes in depends of the cpu :

One : to scrappe one to one
Multi : Here you have to define the number of thread
Fast : That will scrape with the max possible number of thearth

## Parameter :

 
There are store in a Yaml file (Config) 

###Exemple###

*method* : "fast" # The mode for scrapping

*base* : "https://www.yelp.fr/" # the website base (betweeen yelp.de , yelp.com ...)

*city* : "Paris" # The city

*thread* : 3 # Number of thread if method is multi

*shops* : "cafe" # The type of shop you want to scrappe

