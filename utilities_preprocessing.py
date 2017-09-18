# -*- coding: utf-8 -*- 
# Subcreated on Sunday Sept.15, 2013, with improvements periodically from 2013 to 2017. 
# @author: Colin F. Wilder
# Intellectual Property statement: This code is based on lots of other freely available code on the internet, especially lessons from the Programming Historian by Adam Crymble and William Turkel. The utilities to make bigrams are, I believe, fairly original to me, though not rocket science anyway.  Therefore I release it to thee, benevolent user, under a CC-BY license i.e. Creative Commons Attribution 2.0 Generic license, which is explained at https://creativecommons.org/licenses/by/2.0/.#
# Explanation of algorithms in this module:
# Below, I define a bunch of functions for preprocessing text. At the end, I wrap them all together in one function, called processTextFile, whose function is to open a text file and return simple, stripped, lowercase etc. text
# This could be improved by de-compartmentalizing - have your Main program call the preprocessing utilities individually. 

import re

def stripTags(textWithPointyBrackets):
    # strip out XML tags
    # CWCID part of this comes from The Programming Historian
    inside=0
    cleanedUpText=''
    for char in textWithPointyBrackets:
        if inside<0: inside=0        
        if char == '<':
            inside += 1
        elif (inside > 0 and char == '>'):
            inside -= 1
            cleanedUpText += " "
        elif inside > 0:
            continue
        else:
            cleanedUpText += char
    return cleanedUpText

def removeNumbers(textString):
    # remove numbers
    numberListString='0123456789'
    for i in range(0,10):
        textString = textString.replace(numberListString[i], '')
    return textString
    # NB returns a string
    
def removePunctuation(text):
    # remove punctuation
    # replace with white space because some punct like dashes abut letters on both sides
    # remove punct before turning text into list of words
    # do not replace apostrophes with white space
    text = text.replace('`', '')
    # but replace all other punctuation with white space
    punctuation2 = [ '\'', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '[', '}', ']', '|', '\\', ';', ':', '"', '<', '.', '>', ',', '?', '/', '’' ]
    for punct in punctuation2:
        text = text.replace(punct, ' ')
    return text

def removeExtraWhiteSpace(text):
    # remove any white space longer than a single character
    textList = text.split()
    textString = ' '.join(textList)
    return textString
    # NB returns a string
    
# English stop list
stopList=['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herse\x94', 'him', 'himse\x94', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itse\x94', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'much', 'must', 'my', 'myse\x94', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thick', 'thin', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves']

# Latin stop list
latinStopList=['ab', 'ac', 'ad', 'adhic', 'aliqui', 'aliquis', 'an', 'ante', 'apud', 'at', 'atque', 'aut', 'autem', 'cum', 'cur', 'de', 'deinde', 'dum', 'ego', 'enim', 'ergo', 'es', 'est', 'et', 'etiam', 'etsi', 'ex', 'fio', 'haud', 'hic', 'iam', 'idem', 'igitur', 'ille', 'in', 'infra', 'inter', 'interim', 'ipse', 'is', 'ita', 'magis', 'modo', 'mox', 'nam', 'ne', 'nec', 'necque', 'neque', 'nisi', 'non', 'nos', 'o', 'ob', 'per', 'possum', 'post', 'pro', 'quae', 'quam', 'quare', 'que', 'qui', 'quia', 'quicumque', 'quidem', 'quilibet', 'quis', 'quisnam', 'quisquam', 'quisque', 'quisquis', 'quo', 'quoniam', 'sed', 'si', 'sic', 'sive', 'sub', 'sui', 'sum', 'super', 'suus', 'tam', 'tamen', 'trans', 'tu', 'tum', 'ubi', 've', 'uel', 'uero']

def removeStopWords(textString):
    # remove stop words
    textList = textString.split()
    TextListNew=[]
    for word in textList:
        if word in stopList: # requires stop list, which is given just above
            continue
        else:
            TextListNew.append(word)
            textString = ' '.join(TextListNew)
    return textString
    # NB returns a string

def removeStopWordsFromSpecialList(textString,stopWordList=stopList):
    # remove stop words
    textList = textString.split()
    TextListNew=[]
    for word in textList:
        if word in stopWordList:
            continue
        else:
            TextListNew.append(word)
            textString = ' '.join(TextListNew)
    return textString
    # NB returns a string


def removeSingletons(textString):
    # remove strings in text that are single letters, aside from i and a
    textList = textString.split()
    TextListNew=[]
    for word in textList:
        if len(word)<2 and word.lower() != "i" and word.lower() != "a":
            continue
        else:
            TextListNew.append(word)
    textString = ' '.join(TextListNew)
    return textString
    # NB returns a string

# do some of the above functions
def processTextFile(file):
    # open the file
    TextFile = open(file)
    # turn file into a string
    Text=TextFile.read()
    # make everything lower case
    Text=Text.lower()
    # strip tags
    Text=stripTags(Text)
    # remove punctuation here
    Text=removePunctuation(Text)
    # remove stop words    
    Text=removeStopWords(Text)
    return Text

