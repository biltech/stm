#!/usr/bin/env python

import smtplib

WEBMASTER = "contact.resp@gmail.com"   # webmaster e-mail
SMTP_SERVER = "localhost" # your SMTP server

from email.mime.text import MIMEText

def sendMail(to, subject, text):
	user = 'contact.resp@gmail.com'
	pwd = 'USER900P'
	msg = MIMEText(text)
	msg['From']=''
	msg['To'] = to
	msg['Subject'] = subject
	try:
		smtpServer = smtplib.SMTP('smtp.gmail.com', 587)
		smtpServer.ehlo()
		smtpServer.starttls()
		smtpServer.ehlo()
		smtpServer.login(user,pwd)
		smtpServer.sendmail(user, to, msg.as_string())
		smtpServer.close()
		print "mail sent."
	except smtplib.SMTPException as e:
		print "failed", e

def email(req, name, email, comment, subject=None):

    # make sure the user provided all the parameters
    s_err = """\
<html lang="en">
<head>
  <title>StemSeeker</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  <style type="text/css">
	.navbar{
		margin-top: 20px;
  	}
  </style>
</head>
<body>

<div class="container">
    <nav role="navigation" class="navbar navbar-inverse">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <button type="button" data-target="#navbarCollapse" data-toggle="collapse" class="navbar-toggle">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a href="/index.html" class="navbar-brand"><h4>StemSeeker</h4></a>
        </div>
        <!-- Collection of nav links, forms, and other content for toggling -->
        <div id="navbarCollapse" class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
                <li ><a href="/index.html"><h4>Home</h4></a></li>
                <li ><a href="/blog.html"><h4>Blog</h4></a></li>
				<li class="active"><a href="/comments.html"><h4>Comments</h4></a></li>
            </ul>
        </div>
    </nav>
</div>
  
<div class="container">
        <!-- <label> Add comments : </label> -->

        <div class="well">
            <h3 class="lead">
                Submission failed!  Please fill in all the required parameters(*) and submit again.
            </h3>
        </div>
    </div>

</body>
</html>"""

    if not (name and email and comment):
        return s_err 

    # message to webmaster
    msg = """\
From: %s
Subject: feedback
To: %s

I have the following comment:

%s

Thank You,

%s

""" % (email, WEBMASTER, comment, name)

    # message to visitor
    reply = """\
From: %s
Subject: feedback
To: %s

Dear %s, Thank you for your feedback.

""" % (WEBMASTER, email, name)

    ## send to Webmaster
    sendMail('testpostemail111@gmail.com', subject, msg)

    ## send to visitor
    sendMail(email, 'feedback', reply)    

    # provide feedback to the user
    s = """\
<html lang="en">
<head>
  <title>StemSeeker</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  <style type="text/css">
	.navbar{
		margin-top: 20px;
  	}
  </style>
</head>
<body>

<div class="container">
    <nav role="navigation" class="navbar navbar-inverse">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <button type="button" data-target="#navbarCollapse" data-toggle="collapse" class="navbar-toggle">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a href="/index.html" class="navbar-brand"><h4>StemSeeker</h4></a>
        </div>
        <!-- Collection of nav links, forms, and other content for toggling -->
        <div id="navbarCollapse" class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
                <li ><a href="/index.html"><h4>Home</h4></a></li>
                <li ><a href="/blog.html"><h4>Blog</h4></a></li>
				<li class="active"><a href="/comments.html"><h4>Comments</h4></a></li>
            </ul>
        </div>
    </nav>
</div>
  
<div class="container">
        <!-- <label> Add comments : </label> -->

        <div class="well">
            <h3 class="lead">
                Dear %s,<br> thank you for your feedback.
            </h3>
        </div>

        <div class="contact-form">
        </div>
    </div>

</body>
</html>""" % name

    return s
