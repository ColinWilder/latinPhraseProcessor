# What the heck is this? 
This code lemmatizes Latin phrases stored in CSV form. It has a custom dictionary also stored in CSV form that you can add to. Work in progress!

# Current status (9/18/2017)
I am just uploading a first more or less working batch of this code right now. Still have a few features to add and kinks to work out. Wanted to share the basics though. 

# Path structure
Starting in your working directory, you need the following: A file called customDictionary.csv. See sample provided. This can be as long or short as you wish. My plan here is to make the code add to this file with every run so that the user can improve and extend it. Not there yet! Within the working directory, also make a folder called ctp_output (see sample provided). CTP is short for Catalog Title Processor, the original, narrower name of this code project. 

# Other dependencies
Code uses the Classical Language Toolkit (CLTK), which is great though not quite perfect. 

# History
This code began life as a project for doing text analysis on the (mostly) Latin titles of books in historical library catalogs. The idea is to tokenize and lemmatize them using both custom and standard dictionaries. I first presented work related to it at Digitizing Enlightenment 2: The Revenge at Radboud University, Nijmegen (Netherlands), in June 2017, organized by Alicia Montoya, support from whom for travel and attendance I remain grateful. 

# (Planned) future research applications
My goal is to use this code in a more finished form to distantly read historical library catalogs in order to discover large-scale patterns in collecting and holding. I particularly look at collections from 17th-18th centure western Germany, around Frankfurt, Marburg, and Hanau. Gott mit uns! or, Git mit uns?!

# (Planned) future code changes
I would like to make the Latin stop word list an external file, e.g. something like stopWords.txt, for easy editing. The mainprogram would then import this into list form dynamically during execution. 

# Intellectual property (IP) and thanks
Many thanks to Kyle Johnson of CLTK, Patrick Burns of Disiecta Membra, and countless others. I have come to usually suppose in situations like this that most of the code is probably not my own, not really. Mistakes are definitely my own though!
