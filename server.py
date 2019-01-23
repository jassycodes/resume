from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/resume')
def resume():
	return render_template('resume.html')

@app.route('/resumev1-2')
def resumev1_2():
	return render_template('resumev1-2.html')

@app.route('/resumev2')
def resumev2():
	return render_template('resumev2.html')

@app.route('/blog')
def blog():
	return render_template('blog.html')

@app.route('/blogv2')
def blogv2():
	return render_template('blogv2.html')

@app.route('/sentiment_post')
def sentiment():
	return "sentiment Post"
	#make a request to get data from reddit:
	#run sentiment analysis using previous code that we wrot
	#pass in sentiment and current post to our html
	#html output ->  post + sentiment output


if __name__ == '__main__':
   app.run()