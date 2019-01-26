from flask import Flask
from flask import render_template
import requests
import os
import re
import html

app = Flask(__name__)

@app.route('/sentiment_post')
def sentiment():
	#return "sentiment Post"
	#make a request to get data from reddit:
	#run sentiment analysis using previous code that we wrote
	#pass in sentiment and current post to our html
	#html output ->  post + sentiment output

	#### START -- Class: SentimentAnalyzer ######
	class SentimentToAnalyze():
			def __init__(self, text):
				self.text = text
				self.positiveWords = set()#0 #int
				self.negativeWords = set() #0 #int
				self.positivetxt = os.path.realpath("data/positive-words.txt") #get address of positive-words.txt
				self.negativetxt = os.path.realpath("data/negativewords.txt") #get address of negative-words.txt

			#a function that analyzes a sentiment of a text and returns a string: "positive", "negative" or "neutral"
			def analyzeSentiment(self): 
				tweetStripped = self.text.strip() #remove whitespaces 
				#print("Analyzing. . . . . \n " + ' " ' + tweetStripped + ' " ' + "\n") #check -> SentimentText: value 
				tweetWords = tweetStripped.split() 
				self.positiveWords = self.createSetOfWords(tweetWords, self.positivetxt) #list of positive words
				self.negativeWords = self.createSetOfWords(tweetWords, self.negativetxt) #list of negative words

				if len(self.positiveWords) > len(self.negativeWords):
					return "positive"
				elif len(self.positiveWords) < len(self.negativeWords):
					return "negative"
				else:
					return "neutral"

			def createSetOfWords(self, strList, txtFile):
				setOfWords = set()
				regex = re.compile('[^a-zA-Z]')

				for wordTweet in strList: #a function that creates a set (no duplicates) of words
					textAllAlpha = regex.sub('', wordTweet).strip() #strip the words to only have letters (no special characters)

					with open(txtFile, "r") as txtLines: #open the file that contains strings you're comparing each word in the strList to
						for everyWord in txtLines:
							if textAllAlpha.lower() == everyWord.strip() and textAllAlpha.lower() != "":
								setOfWords.add(everyWord.strip()) #add to the set of words in the current srting

				return setOfWords

			#changes the source of positive words for comparison.
			#newPositivetxt - a parameter; should be a variable containing the path to the new positive words txt source
			def changePositiveDictSource(self, newPositivetxt):
				self.positivetxt = newPositivetxt

			#changes the source of negative words for comparison.
			#newNegativetxt - a parameter; should be a variable containing the path to the new negative words txt source
			def changePositiveDictSource(self, newNegativetxt):
				self.negativetxt = newNegativetxt

	#### END -- Class: SentimentToAnalyze ######
	########################################

	TAG_RE = re.compile(r'<[^>]+>')
	#remove html tags
	def rm_htmltags(text):
		return TAG_RE.sub('', text)

	response = requests.get('https://hacker-news.firebaseio.com//v0/maxitem.json?print=pretty') #get the response of URL
	latest_ID = response.json() #store the id of the latest item in a variable, latest_ID
	latest_ID_response = requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(latest_ID) +'.json?print=pretty') #get the response of latest ID URL
	#store all the info associated to the latest ID in the variable, latest_ID_info
	latest_ID_info = latest_ID_response.json() #data type: dictionary

	item_counter = 1
	#max_item = int(input("How many top comments do you want to analyze? ")) #get the number of top comments you want to analyze
	max_item = 10
	current_ID = latest_ID #initialize the current_ID to the value of the latest_ID
	
	comment_sentiment_dict = {}
	comment_sentiment_pair_list = []

	if max_item == 1:
		print("THE LATEST COMMENT: \n")
	elif max_item > 1:
		print("THE " + str(max_item) + " LATEST COMMENTS: \n")
	else:
		print("Okay, nothing to analyze.")


	def printResult():
		for c in comment_sentiment_pair_list:
			print(c)

	while item_counter <= max_item: #while we haven't gotten the desired number of top comments we want, go through the latest items from newest to oldest
		#print("Current ID: " + str(current_ID)) #print current_ID
		current_ID_response = requests.get('https://hacker-news.firebaseio.com/v0/item/' + str(current_ID) +'.json?print=pretty') #get the response of current_ID
		current_ID_info = current_ID_response.json() #store all the info associated to the current ID in the variable, current_ID_info
		comment_sentiment_dict = {}
		if current_ID_info['type'] == 'comment':
			comment = rm_htmltags(html.unescape(current_ID_info['text'])) #store the value of the key 'comment' to the variable, comment
			commentToAnalyze = SentimentToAnalyze(comment) #create an object of the class, SentimentToAnalyze and store it in a variable, commentSentiment
			commentSentiment = commentToAnalyze.analyzeSentiment()
			item_counter += 1 #increase item_counter
			comment_sentiment_dict["ID"] = current_ID
			comment_sentiment_dict["COMMENT"] = comment
			comment_sentiment_dict["SENTIMENT"] = commentSentiment
			comment_sentiment_pair_list.append(comment_sentiment_dict)
		


		#print(item_counter)
		current_ID -=1 #get the ID of the next older item
		#print(current_ID)

	return str(comment_sentiment_pair_list) #comment_sentiment_pair_list

if __name__ == '__main__':
   app.run()