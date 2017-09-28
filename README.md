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
I would like to make the Latin stop word list an external file, e.g. something like stopWords.txt, for easy editing. The main program would then import this into list form dynamically during execution. 
Detect language first. That will tell you which stop words to use and which lemmatizer to apply.
Replace small syntactical and spelling errors such as a¨
Look for proper names first. If found, mark them in some special way so that they do not get lemmatized.
Look for all Roman numberals in upper case through say about CCC (300). Do this before going to lower case and lemmatizing.

Lemmatize in German, French, and English first before tokenizing and lemmatizing in Latin. You should do Latin last because it requires the U-V and I-J change, which messes with the other languages. Tokenization seems to remove the n on the end of some words, making it hard to recognize many German words.

For Latin, I think it would be very valuable to be able to use Whitaker's Words as a reference. Frankly I get far more correct hits with it than I do with the CLTK lemmatizer.

For German, it would be great to be able automatically to decompose compound words into elements, e.g. reichstagabschied into reich tag abschied.

I wonder whether a stemming program could re-discover the proper head forms of names, for instance turning Egidio into Egidius. If so, you could then feed the head word candidates to a list of proper names.

I sense that it would be good to store words as Python objects (instances of the class word or something). I imagine that NLTK does something like this. Alternatively maybe each line (here each title) being processed could be stored as a line object (instance of the class line or something).


# Intellectual property (IP) and thanks
Many thanks to Kyle Johnson of CLTK, Patrick Burns of Disiecta Membra, and countless others. I have come to usually suppose in situations like this that most of the code is probably not my own, not really. Mistakes are definitely my own though!
