import random
import os

from flask import (
	Flask,
	request, session,
	url_for, render_template,	redirect)
#Create a Flask application object
app = Flask(__name__)
# session variables are stored client-side(on the user's browser).
# the content of these variables is encryted, so users can't actually
# read their contents. they could edit the sesson data, but because it 
# would not be "signed" with the secret key below, the server would
# reject is as invalid.
# You need to set a secret key(random text) and keep it secret!
app.secret_key = "15"
# The path to the directory containig our images
#We will store a list of image file names ina asession variable
IMAGE_DIR = app.static_folder

##################
# Helper funtions#
##################

def init_game():
	#initializa a new deck(a list of filenames)
	image_name = os.listdir(IMAGE_DIR)
	#Shuffle the deck
	random.shuffle(image_name)
	#store it in the user's session
	# 'session' is a special global object that Flask provides
	# which exposes the basic session management funtionality
	session['images'] = image_name
	
def select_from_deck():
	try:
		
		image_name = session['images'].pop()
	except IndexError:
		image_name = None
	return image_name

#################
# View funtions #
#################
@app.route('/')
def index():
	init_game()
	return render_template("index.html")

@app.route('/draw')
def draw_card():
	if 'images'not in session:
		abort(400)
	image_name = select_from_deck()
	if image_name is None:
		return render_template("gameover.html")
	return render_template("showcard.html", image_name = image_name)
if __name__ == '__main__':
	app.run(debug=True)
