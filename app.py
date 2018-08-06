import flask
import logging
import os
import datetime
import werkzeug
import tornado.wsgi
import tornado.httpserver
from shutil import copyfile

from interface import *
from findface import *

import cv2
import time

from flask import Flask
app = Flask(__name__)

UPLOAD_FOLDER = './static/uploaded_images/'
PROCESSED_FOLDER = './static/processed_images/'
BLACKTEMPLATE_FOLDER = './static/blacktemplate/'
DATABASE_FOLDER = './database/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['DATABASE_FOLDER'] = DATABASE_FOLDER
app.config['BLACKTEMPLATE_FOLDER'] = BLACKTEMPLATE_FOLDER
app.count = 0
app.timestamp = int(time.time())
app.timestamp = "-"+str(app.timestamp)


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if flask.request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return flask.redirect(flask.url_for('index'))

    # show the form, it wasn't submitted
    return flask.render_template('gallery.html')

@app.route('/')
def index():
    # return 'Hello, World!'
    fullpath = os.path.join(app.config['BLACKTEMPLATE_FOLDER'],'write.jpg')
    qrcodepath = os.path.join(app.config['BLACKTEMPLATE_FOLDER'],'qr.png')
    return flask.render_template('index.html', inputimagesrc=fullpath,imagesrc=fullpath,qrcode=qrcodepath)

@app.route('/favicon.ico')
def favicon():
	return flask.send_from_directory(os.path.join(app.root_path, 'static'),
		'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/uploads')
def uploaded_file():
    return flask.send_from_directory(app.config['UPLOAD_FOLDER'],"test.jpg")

@app.route('/downloads/<filename>')
def download_file(filename):
    return flask.send_from_directory(app.config['PROCESSED_FOLDER'],
                               filename)

@app.route('/indifference', methods=['GET'])
def get_indifference_img():
	print("indifference")
	outfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'indifference'+str(app.count) + app.timestamp+ '.jpg')
	inputfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'origin'+str(app.count)+app.timestamp+'.jpg')
	# inputfullpath = os.path.join(app.config['UPLOAD_FOLDER'],'test.jpg')

	print("Get indifference img in: ",outfullpath)
	print("Get reference img in: ",inputfullpath)

	qrcodepath = os.path.join(app.config['BLACKTEMPLATE_FOLDER'],'qr.png')
	return flask.render_template(
		'index.html', inputimagesrc=inputfullpath,imagesrc=outfullpath,qrcode=qrcodepath)

@app.route('/angry', methods=['GET'])
def get_angry_img():
	print("angry")
	outfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'angry'+str(app.count)+app.timestamp+'.jpg')
	inputfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'origin'+str(app.count)+app.timestamp+'.jpg')
	# inputfullpath = os.path.join(app.config['UPLOAD_FOLDER'],'test.jpg')

	print("Get angry img in: ",outfullpath)
	print("Get angry img in: ",inputfullpath)

	qrcodepath = os.path.join(app.config['BLACKTEMPLATE_FOLDER'],'qr.png')
	return flask.render_template(
		'index.html', imagesrc=outfullpath,inputimagesrc=inputfullpath,qrcode=qrcodepath)

@app.route('/sad', methods=['GET'])
def get_sad_img():
	print("sad")
	outfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'sad'+str(app.count)+app.timestamp+'.jpg')
	inputfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'origin'+str(app.count)+app.timestamp+'.jpg')
	# inputfullpath = os.path.join(app.config['UPLOAD_FOLDER'],'test.jpg')

	print("Get sad img in: ",outfullpath)
	print("Get sad img in: ",inputfullpath)

	qrcodepath = os.path.join(app.config['BLACKTEMPLATE_FOLDER'],'qr.png')
	return flask.render_template(
		'index.html', imagesrc=outfullpath,inputimagesrc=inputfullpath,qrcode=qrcodepath)

@app.route('/happy', methods=['GET'])
def get_happy_img():
	print("happy")
	outfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'happy'+str(app.count)+app.timestamp+'.jpg')
	inputfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'origin'+str(app.count)+app.timestamp+'.jpg')
	# inputfullpath = os.path.join(app.config['UPLOAD_FOLDER'],'test.jpg')

	print("Get happy img in: ",outfullpath)
	print("Get hapy img in: ",inputfullpath)

	qrcodepath = os.path.join(app.config['BLACKTEMPLATE_FOLDER'],'qr.png')
	return flask.render_template(
		'index.html', imagesrc=outfullpath, inputimagesrc=inputfullpath,qrcode=qrcodepath)

@app.route('/classify_upload', methods=['POST'])
def classify_upload():
	imagefile = flask.request.files['imagefile']
	filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
		werkzeug.secure_filename(imagefile.filename)
	# filename1 = os.path.join(UPLOAD_FOLDER, filename_)
	app.count += 1
	filename0 = os.path.join(UPLOAD_FOLDER, 'test_unp'+str(app.count)+app.timestamp+'.jpg')
	filename1 = os.path.join(UPLOAD_FOLDER, 'test'+str(app.count)+app.timestamp+'.jpg')
	filename2 = os.path.join(DATABASE_FOLDER, werkzeug.secure_filename(imagefile.filename))

	imagefile.save(filename0)
	print("Original img file saved to: ",filename0)
	# copyfile(filename1, filename2)
	# print("Original img file saved to database: ",filename2)
	crop_face(filename0,filename1)


	# inputfullpath = os.path.join(app.config['UPLOAD_FOLDER'],'test.jpg')
	inputfullpath = os.path.join(app.config['PROCESSED_FOLDER'],'origin'+str(app.count)+app.timestamp+'.jpg')
	blackfullpath = os.path.join(app.config['BLACKTEMPLATE_FOLDER'],'write.jpg')

	lists=app.gan.GanImage(filename1)
	save_image(denorm(lists[0].data.cpu()), PROCESSED_FOLDER + "origin"+str(app.count)+app.timestamp+".jpg", nrow=1, padding=0)
	save_image(denorm(lists[1].data.cpu()), PROCESSED_FOLDER + "angry"+str(app.count)+app.timestamp+".jpg", nrow=1, padding=0)
	save_image(denorm(lists[2].data.cpu()), PROCESSED_FOLDER + "happy"+str(app.count)+app.timestamp+".jpg", nrow=1, padding=0)
	save_image(denorm(lists[3].data.cpu()), PROCESSED_FOLDER + "indifference"+str(app.count)+app.timestamp+".jpg", nrow=1, padding=0)
	save_image(denorm(lists[4].data.cpu()), PROCESSED_FOLDER + "sad"+str(app.count)+app.timestamp+".jpg", nrow=1, padding=0)

	qrcodepath = os.path.join(app.config['BLACKTEMPLATE_FOLDER'],'qr.png')
	return flask.render_template('index.html',inputimagesrc=inputfullpath,imagesrc=blackfullpath,qrcode=qrcodepath)
		# return flask.redirect(flask.url_for('classify_upload'))



def start_from_terminal(app):
	parser = argparse.ArgumentParser()
	config = parser.parse_args()
	app.gan=Gan(config)
	print
	print("Model loaded.")
	print("-"*30)
	print
	print

	start_tornado(app, 10020)

def start_tornado(app, port=5000):
	http_server = tornado.httpserver.HTTPServer(tornado.wsgi.WSGIContainer(app))
	http_server.listen(port)
	print("Tornado server starting on port {}".format(port))
	tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    start_from_terminal(app)
    # app.run(host='202.120.39.24',port=10090,debug=True)


