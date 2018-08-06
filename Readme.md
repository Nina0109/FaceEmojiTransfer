This is a small application based on flask.
Please install python3.5 and necessary packages in requirements.txt.
You can use some images in testcase to test the application.

To test the application on local server. Please run:
> cd classproject/flask  
> set FLASK_APP=app.py (use export instead on linux)  
> flask run

To test on remote server. Please run:
> cd classproject/flask  
> python app.py

The system takes a face image as input and will generate several other expression for the same person.
Thes interace is as follow.

<img src="https://raw.githubusercontent.com/Nina0109/FaceEmojiTransfer/master/webdemo.png" alt="alt text" align="middle" height="500">

Some generated examples:
<div>Original Input &nbsp&nbsp&nbsp&nbsp&nbsp Happy &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp Angry &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp Sad
  <img src="https://raw.githubusercontent.com/Nina0109/FaceEmojiTransfer/master/static/gallery/origin1.jpg" alt="alt text" align="middle" width="100">
  <img src="https://raw.githubusercontent.com/Nina0109/FaceEmojiTransfer/master/static/gallery/happy1.jpg" alt="alt text" align="middle" width="100">
  <img src="https://raw.githubusercontent.com/Nina0109/FaceEmojiTransfer/master/static/gallery/angry1.jpg" alt="alt text" align="middle" width="100">
  <img src="https://raw.githubusercontent.com/Nina0109/FaceEmojiTransfer/master/static/gallery/sad1.jpg" alt="alt text" align="middle" width="100">
</div>
