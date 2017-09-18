# CTP: Catalog Title Processor
# September 2017

# gibs me dat
import os, csv
import pandas as pd
from utilities_preprocessing import *
from utilities_output_files import *
from glob import glob
from cltk.stem.latin.j_v import JVReplacer
from cltk.stem.lemma import LemmaReplacer
from cltk.tokenize.word import WordTokenizer
from cltk.lemmatize.latin.backoff import TrainLemmatizer

# global variables
customDictionary={} # a dictionary into which we will read the custom dictionary csv file for use during execution
customLemmatizer = TrainLemmatizer(customDictionary)
lemmatizer = LemmaReplacer('latin')
word_tokenizer = WordTokenizer('latin')
failsList=[] # here will be recorded tokens which the two dictionaries have failed to recognize for that line
jv=JVReplacer()
lemmatizedTextList=[] # holds the versions of the title as we lemmatize them
lengthOfDataFile=0 # number of rows in data file
preprocessedTitle="" # a temp string where we store the ongoing preprocessing work on a title

# import custom dictionary csv as python dictionary
cwd=os.getcwd()
customDictionaryPath=os.path.join(cwd,'customDictionary.csv')
with open(customDictionaryPath,'r') as f:
	reader=csv.DictReader(f)
	for row in reader:
		if row['lemma']=="":
			continue # in case a token has been added to custom dictionary but no lemma has yet been provided it
		customDictionary[row['token']]=row['lemma']

# make a hole in the output
print()

# find the current data file index and increment it
# make new output base path
bp=newOutputBasePath()
print("basePath: \t\t" + bp)
ci=currentIndex()

#construct new output folder based on index
newOutputFolder=makeNewOutputFolder(ci,bp)
print("new output folder: \t" + newOutputFolder)

# construct data folder path
dataFolder=os.path.join(bp,"data") # make data folder path; this is where data file(s) are to live
print("data folder: \t\t" + dataFolder)

# look in data folder
g=glob(dataFolder + "/*")
print(g)

# open and process file(s) inside the data folder
for f in g:
	print("found in data folder: \t"+str(f))
	# read file into a pandas data frame
	currentDF=pd.read_csv(f, na_values=['nan'], keep_default_na=False) # the nan thing is an annoying CLTK data thingy # don't worry # just keep this as is
	# some tests that can be eliminated later on
	lengthOfDataFile = len(currentDF['fails'])
	# make copy of the data frame; we will write new changes to the copy
	nextDF=currentDF
	
	for i in range(0,lengthOfDataFile):
		print("\nworking on new title now...")
		##############################
		# preprocess any titles that have not yet been preprocessed
		print("preprocessing...")
		preprocessedTitle=currentDF['preprocessed title'][i]
		# if any cell is blank, then preprocess the corresponding cell in the first column
		# the purpose of this is in case (1) this is the first run of a new data set or (2) new data has been added.
		# case 1: title has already been preprocessed
		if currentDF['preprocessed title'][i] == "":
			# assume that user will not manually edit preprocessed titles
			preprocessedTitle=currentDF["original title"][i]
			# to do: deal with special characters such as æ and o¨ # probably change them to dipthongs e.g. ae and oe
			# remove punctuation
			preprocessedTitle=removePunctuation(preprocessedTitle)
			# remove numbers
			preprocessedTitle=removeNumbers(preprocessedTitle)
			# change preprocessedTitle to lower case
			preprocessedTitle=preprocessedTitle.lower()
			# change js and vs
			preprocessedTitle=jv.replace(preprocessedTitle)
			# remove stopwords
			preprocessedTitle=removeStopWordsFromSpecialList(preprocessedTitle, stopWordList=latinStopList)
			# remove extra white space because material forces determine that whiteness will disappear
			preprocessedTitle=removeExtraWhiteSpace(preprocessedTitle)
			print("preprocessed form of title:\t" + preprocessedTitle)
			
			# write the temporary string to the 'preprocessed title' column cell that was empty
			nextDF['preprocessed title'][i]=preprocessedTitle

		##############################
		# tokenization and lemmatization
		print("tokenizing and lemmatizing...")
		
		print("first running through custom dictionary...")
		# if the custom dictionary succeeds in recognizing the token, then write the lemma into the corresponding tuple. 
		# if the custom dictionary fails, write the lemma value as "None". 
		# It would be better to be able to choose a different default message than "None", as the CLTK default lemmatizer can do
		tokens=preprocessedTitle.split() # split preprocessed title into list form
		lemmatizedTextList=customLemmatizer.lemmatize(tokens) # run the custom dictionary on it and write each token into a tuple in lemmatizedTextList
		print("resulting list of token-lemma pairs:\t"+str(lemmatizedTextList))

		# look for other tokens in CLTK standard lemmatizer (also tokenize and clean up, etc.)
		for j in range(0,len(lemmatizedTextList)):
			lemmatizedTextList[j]=(str(lemmatizedTextList[j][0]),str(lemmatizedTextList[j][1]))
			if str(lemmatizedTextList[j][1])=="None":
				token=str(lemmatizedTextList[j][0])
				lemma=token
				print("searching for " + lemma + " in CLTK standard dictionary")
				
				# tokenize text; though tokens themselves are not the goal this separates enclitics etc. 
				lemma=str(word_tokenizer.tokenize(lemma))

				# tokenizer leaves dashes on enclitics might want to run removePunctuation again here
				lemma=removePunctuation(lemma)

				# similarly re-run removeStopWordsFromSpecialList here to remove new arrivals like que or ne produced from separating enclitics
				lemma=removeStopWordsFromSpecialList(lemma, stopWordList=latinStopList)

				# and again removeSingletons
				lemma=removeSingletons(lemma)

				# now feed the tokenized text into the lemmatizer
				lemma=lemmatizer.lemmatize(lemma)
				
				# make sure lemma is a string, not a list or egads an empty list
				if lemma==[]:
					lemma=""
				else:
					lemma=lemma[0]
				
				# replace tuple (with weird CLTK objects) with other tuple (with strings)
				lemmatizedTextList[j]=(token,lemma)
				print(lemmatizedTextList[j])
				
				# to do: write fails to failsList using append
		
		# write lemmatizedTextList to the third column, so that we retain all the success and failure information for a possible next run of the system after perhaps improving the custom dictionary. 
		nextDF['lemmatized text list'][i]=lemmatizedTextList
		print("new column #3 of data file:\t" + str(nextDF['lemmatized text list'][i]))
		
		# fashion a simple string version of lemmatizedTextList and write it to the fourth column
		bestCurrentLemmatizedForm="" # a temp string for storing the best current form containing lemmas where possible and fialing that the original tokens
		for tuple in lemmatizedTextList:
			if tuple[1]=="None":
				bestCurrentLemmatizedForm+=tuple[0]+" "
			elif tuple[1]=="":
				continue			
			else:
				bestCurrentLemmatizedForm+=tuple[1]+" "
		nextDF['best current lemmatized form'][i]=bestCurrentLemmatizedForm
		print("new column #4 of data file:\t" + bestCurrentLemmatizedForm)
		
		
		"""
		# write failsList to the cell in the fifth column in a prettyprint string form. it is not important to save the failsList structure because if/when we next run the system, we need to look for fails in column four not column five anyway so as to maintain the integrity and sequence of tokens/lemmas in the titles.
		# add the items in failsList to the custom dictionary. 
		"""
	
	# print failsList to output for review
	print("\nfails:\t"+str(failsList))
	
	# write the data file to a new csv file. 
	nextDF.to_csv(os.path.join(newOutputFolder,'testData3.csv'),index=False)
	# This is the last action to take after the loading and full processing of each file in the data folder. 
	# After all data files have been processed, the for loop stops. 

# add a space for the sake of clarity of output to screen
print()

