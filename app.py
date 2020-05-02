from flask import Flask, request, render_template, jsonify, flash, redirect
import json
from datetime import datetime
import time
import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import re

templates="templates"

welcomeMsg = '''<span class="red">{0}@PaxPrz:</span>:<span class="blue">~</span>$ whoispax 
Hello {0}, Welcome to my virtual system <span class="success">PraKsha</span> v1.0.

This system was designed so you could know me well. It's like a personal site. Let me introduce myself I am Prakash Prajapati. I am a security researcher cum programmer. 

Navigate the system with commands you can play. Start with 'help' command. I hope you have good time learning about me.
'''

welcomeMsg2='''
hello welcome
'''

def writeError(e):
    print(e)

app = Flask(__name__, template_folder=templates)
app.config['SECRET_KEY']='mynameisprakashprajapati'

USERS={}
WHOISPAX={
    "Name":"Prakash Prajapati",
    "Gender":"Male",
    "Academics":"Bachelors in Computer Engineering",
    "Interest":"Cybersecurity, AI, Blockchain",
    "Hobbies":"Playing Football & PC games"
}

PROJECTS={
    'ChatBot':{
        'quick':'C Project',
        'detail':'I did this project when I was in fresher in engineering. This is a C program that searches for pattern of words in user\'s input and generate output based on that input. It could detect question patterns and generate a random answers by creating suitable answer pattern.'
    },
    'Library Management System':{
        'quick':'C++ Project',
        'detail':'This program manages library books. List books based on authors or publication. Entry books. Search for books. The program users Standard Template Library and file handling.'
    },
    'Secret Notice':{
        'quick':'Java & Android Project',
        'detail':'Program encrypts messages using caesar cipher algorithm and converts the encrypted text to QR code. User with valid password can only decipher message from QR code. Swimg framework in java was implemented for GUI. Used zxing library to generate QR for desktop application.'
    },
    'Travel Partner':{
        'quick':'Android Project',
        'detail':'Android app with complete package for tourists visiting Nepal in 2020. Provides speech detection and translation from various languages to nepali and vice versa using Yandex API; Currency conversion using Fixer API; and google map searches for nearest hotels.'
    },
    'Image Processing Toolkit':{
        'quick':'Python project',
        'detail':'Basic image processing functions like grayscaling, power-law, brightness, contrast, filters, etc implemented in python. Tkinter was used for GUI.'
    },
    'Asteroid Smash':{
        'quick':'Android game in Unity',
        'detail': '2D android game developed as minor project. The game implements reinforcement learning using ML-Agents to train enemy ship.'
    },
    'DrSewa':{
        'quick':'Django Application with Hyperledger',
        'detail':'Doctors and patients informations are stored in blockchain network implemented using hyperledger composer. Only consulted (Allowed) doctors can view all reports of patients. Patient can set an appointment with doctor and doctor can set an appointment time; and consult with video conference implemented using WebRTC.'
    },
    'Hastakshar':{
        'quick':'Academic Major Project',
        'detail':'Offline signature verification system using CNN (Keras &amp; Tensorflow). The trained weights metadata are then stored in blockchain network implemented using Hyperledger Composer. System was developed in Django with web interfaces. Only allowed users can verify signature of a signee while the signee gets notified of those actions. I tested with many CNN architecture, mostly created by myself. Training was done in Nvidia-1050Ti using Tensorflow-gui. Many steps of image pre-processing were carried out including grayscaling, noisereduction, resizing, etc using numpy and opencv library.'
    },
    'Firefly Responsive Web':{
        'quick':'HTML & CSS Project',
        'detail':'Design project at Leapfrog using HTML and CSS2. Live demo at <a href="https://paxprz.github.io/firefly-responsive-web" target="_blank">here</a>.'
    },
    'FaceFilter':{
        'quick':'Javascript Project',
        'detail':'Implementation of Haar Cascade technique developed by Voila & Jones to detect human face in image. Then user can select face(s) and add available filters to it. Live demo at <a href="https://paxprz.github.io/Haar-Face-Detector/" target="_blank">here</a>.'
    },
    'RansomTest':{
        'quick':'Light Version of Ransomware',
        'detail':'Program developed in python that mimics the action of ransomware and encrypts the images present in working directory using AES. 4096 bit RSA key was used for public key encryption. Crypto.Cipher.AES and rsa modules were implemented.'
    },
    'Eminence':{
        'quick':'Python Hacking automation tool',
        'detail':'Eminence project was developed in python to test a few vulnerabilities available in Metasploitable 3. It consist of scanning tool, information gathering, dictionary attack and command injection to gain access to metasploitable 3 enviornment.'
    },
    'ToHarrods':{
        'quick':'Flask App',
        'detail':'Application developed for client. Worked with big database set. Can\'t share much detail of the work'
    }
}

PROGRAMMING={
    'Python':'&#9733;&nbsp;&#9733;&nbsp;&#9733;&nbsp;&#9733;&nbsp;&#9734;&nbsp;',
    'Javascript':'&#9733;&nbsp;&#9733;&nbsp;&#9733;&nbsp;&#9734;&nbsp;&#9734;&nbsp;',
    'C':'&#9733;&nbsp;&#9733;&nbsp;&#9733;&nbsp;&#9734;&nbsp;&#9734;&nbsp;',
    'C++':'&#9733;&nbsp;&#9733;&nbsp;&#9733;&nbsp;&#9734;&nbsp;&#9734;&nbsp;',
    'Java':'&#9733;&nbsp;&#9733;&nbsp;&#9734;&nbsp;&#9734;&nbsp;&#9734;&nbsp;',
    'PHP':'&#9733;&nbsp;&#9734;&nbsp;&#9734;&nbsp;&#9734;&nbsp;&#9734;&nbsp;'
}

gmail_email = os.environ['GMAIL_EMAIL']
gmail_pass = os.environ['GMAIL_PASS']
cv_filename = 'paxcv.pdf'

def sendCVEmail(name, email):
    global gmail_email, gmail_pass, cv_filename
    text = '''Hello {0}. I have attached my CV hereby. If you consider me good for any position please contact me or email me.'''
    msg = MIMEMultipart()
    msg['From'] = gmail_email
    msg['To'] = gmail_pass
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "PaxPrz CV"
    msg.attach(MIMEText(text.format(name)))
    try:
        with open(cv_filename, 'rb') as f:
            part = MIMEApplication(f.read(), Name=basename(cv_filename))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(cv_filename)
        msg.attach(part)
    except Exception as e:
        writeError(e)
        return '<span class="error">CV file not found. Try later</span>'
    try:
        smtp = smtplib.SMTP('smtp.gmail.com:587')
        smtp.ehlo()
        smtp.starttls()
        smtp.login(gmail_email, gmail_pass)
        smtp.sendmail(gmail_email, email, msg.as_string())
        smtp.quit()
    except Exception as e:
        writeError(e)
        return '<span class="error">SMTP server error. Please Try later</span>'
    return '<span class="success">Success</span>: Please check your email'

def createUser(username):
    global USERS
    USERS[username]={'access':[], 'job':[], 'email':[], 'name':[], 'contact':[], 'github':False, 'linkedin':False, 'stackoverflow':False}

def helpCmd(user, args):
    global OPERATIONS
    output = '''<table class="noBorders">
    <thead>
        <tr>
            <td> Command &nbsp;&nbsp;</td>
            <td> Description </td>
        </tr>
    </thead>
    <tbody>
    '''
    KEYS_TO_WATCH = OPERATIONS.keys()
    if args:
        KEYS_TO_WATCH = [x for x in KEYS_TO_WATCH if x in args]
    for key in KEYS_TO_WATCH:
        output+='''     <tr>
            <td>'''+key+'''</td>
            <td>'''+OPERATIONS[key]['description']+'''</td>
        </tr>'''
    output+='''</tbody>
    </table>
    '''
    return output

def whoispaxCmd(user, args):
    global WHOISPAX
    output = '''<table class="noBorders">
    <tbody>
    '''
    for key in WHOISPAX.keys():
        output+='''<tr>
        <td>'''+key+'''</td>
        <td>'''+WHOISPAX[key]+'''</td>
        </tr>'''
    output += '''</tbody>
    </table>'''
    return output

def workCmd(user, args):
    output = '''Currently working as <span class="success">Security Analyst</span> @ Cynical Technology'''
    return output

def projectsCmd(user, args):
    global PROJECTS 
    output = ''
    if not args:
        output = '''<table class="noBorders">
        <thead>
            <tr>
                <td> Project &nbsp;&nbsp;</td>
                <td> Quick Info </td>
            </tr>
        </thead>
        <tbody>
        '''
        for key in PROJECTS.keys():
            output+='''     <tr>
            <td>'''+key+'''</td>
            <td>'''+PROJECTS[key]['quick']+'''</td>
            </tr>'''
        output+='''</tbody>
        </table>
        <span>For Project Details, use piece of project title. Usage: projects [titl...]</span>
        '''
    else:
        title = ' '.join(args)
        print(title)
        projects = [key for key in PROJECTS.keys() if title.lower() in key.lower()]
        print(projects)
        if projects:
            for p in projects:
                output+='''<table class=noBorders>
                <thead>
                    <tr>
                        <td colspan='2'>'''+p+'''</td>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Quick Info</td>
                        <td>'''+PROJECTS[p]['quick']+'''</td>
                    </tr>
                    <tr>
                        <td>Description</td>
                        <td>'''+PROJECTS[p]['detail']+'''</td>
                    </tr>
                </tbody>
            </table>
            '''
        else:
            output="<span>No Project Found</span>"
    return output

def programmingCmd(user, args):
    global PROGRAMMING
    output = '''<table class="noBorders">
        <thead>
            <tr>
                <td> Language &nbsp;&nbsp;</td>
                <td> Skill Rating </td>
            </tr>
        </thead>
        <tbody>
        '''
    for language in PROGRAMMING:
        output+='''     <tr>
        <td>'''+language+'''</td>
        <td>'''+PROGRAMMING[language]+'''</td>
        </tr>
        '''
    output+='''</tbody>
        </table>'''
    return output

def looksCmd(user, args):
    output = '''I look somewhat like this XD <br>
    <span class="small-text">
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■□□□■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□■□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□■■■□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□■■■■■■■□□□□□□□□□□□■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□■■■■■■■■■□□□□□□□■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■□□□□□□□□□□■■□□□□□□■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■■■□□□□□■■■■■■■□□□□□□□■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□■□■□□□□□■■■■■□■□□□□□□□□□■■■□■■■□□■■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□■□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□■■■□■■■□□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□□□□□□□□□■□□□□□□□□□■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■□□□□□□□□■■■□□□□□■■■■■■□□□■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□□□■■■■■■■■■■■■■■■■□□□■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■□□□□□□■■■■■■■■■■■■■■□□□■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■□□□□□□□■■□□□□□■■■□□□□□■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■□□□□□□□■■■■■■■■□□□□□■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■□□□□□□□□■■■□□□□□□□■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■□□□□□□□□□□□□□□□□■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■□□□□□□□□□□□□□□□■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■□□□□□□□□□□□□□■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■□□□□□□□□□■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■□□□□□□□□□■■□□■■■■■□□□■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■□□□□□□□□□□□□□□■■□□□□□■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□□□■■■■■■■■■■□□■■■□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□□□■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□□□□■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■□□□■■■■■■■■■■■■■■■■■■■□□□□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□□□■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■□□□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□□□■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■□□□</p>
<p style="margin:0px; margin-bottom:-5px">□□□□■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■□</p>
<p style="margin:0px; margin-bottom:-5px">□□■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□</p>
<p style="margin:0px; margin-bottom:-5px">□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■□□■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■</p>
<p style="margin:0px; margin-bottom:-5px">■■■■■■■■■■■■■■■■■■■■■■□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□□</p>
</span><br>'''
    return output

def githubCmd(user, args):
    global USERS
    if user not in USERS.keys():
        createUser(user)
    USERS[user]['github']=True
    output = '''Redirecting to <a href="https://github.com/paxprz/" target="_blank" id="github">github</a> ...
    <script>document.getElementById('github').click()</script>'''
    return output

def linkedinCmd(user, args):
    global USERS
    if user not in USERS.keys():
        createUser(user)
    USERS[user]['linkedin']=True
    output = '''Redirecting to <a href="https://www.linkedin.com/in/paxprz" target="_blank" id="linkedin">LinkedIn</a> ...
    <script>document.getElementById('linkedin').click()</script>'''
    return output

def stackoverflowCmd(user, args):
    global USERS
    if user not in USERS.keys():
        createUser(user)
    USERS[user]['stackoverflow']=True
    output = '''Redirecting to <a href="https://stackoverflow.com/users/5611227/pax" target="_blank" id="stackoverflow">StackOverFlow</a> ...
    <script>document.getElementById('stackoverflow').click()</script>'''
    return output

def getcvCmd(user, args):
    global USERS
    if user not in USERS.keys():
        createUser(user)
    if not args:
        return '''<span>CV will be sent through email<br>
        Usage: getcv <i>email@address</i> ["<i>Full Name</i>"] [<i>ContactNo.</i>]'''
    email = args[0]
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if(re.search(regex,email)):
        if str.isdecimal(args[-1]):
            contact = args[-1]
            name = ' '.join(args[1:-1]).strip(' ').strip('"').strip(' ')
        else:
            contact = ''
            name = ' '.join(args[1:]).strip(' ').strip('"').strip(' ')
        if name=='':
            name = 'Sir/Madam'
        else:
            USERS[user]['name'].append(name)
        if contact!='':
            USERS[user]['contact'].append(contact)
        USERS[user]['email'].append(email)
        if 'yopmail' in email.lower():
            return '<span class="error">Temporary Email Not supported</span>'
        return sendCVEmail(name, email)
    else:
        return '<span class="error">Invalid Email Address</span>'

OPERATIONS={
    'help':{
        'usage':'help',
        'arguments':0,
        'description':"Shows list of commands and their descriptions",
        'fn': helpCmd
    },
    'clear':{
        'usage':'clear',
        'arguments':0,
        'description':'Clears the terminal'
    },
    # 'ls':{
    #     'usage':'ls',
    #     'arguments':0,
    #     'description':'Lists files inside current folder'
    # },
    'whoispax':{
        'usage':'whoispax',
        'arguments':0,
        'description':'A quick intro of myself',
        'fn':whoispaxCmd
    },
    'work':{
        'usage':'work',
        'arguments':0,
        'description':'Where do I work?',
        'fn':workCmd
    },
    'projects':{
        'usage':'projects',
        'arguments':0,
        'description':'Displays Projects I have done.',
        'fn':projectsCmd
    },
    'programming':{
        'usage':'programming',
        'arguments':0,
        'description':'Shows my programming skills',
        'fn':programmingCmd
    },
    'looks':{
        'usage':'looks',
        'arguments':0,
        'description':'Portraits my face',
        'fn':looksCmd
    },
    'github':{
        'usage':'github',
        'arguments':0,
        'description':'Opens my github profile',
        'fn':githubCmd
    },
    'linkedin':{
        'usage':'linkedin',
        'arguments':0,
        'description':'Opens my linkedin profile',
        'fn':linkedinCmd
    },
    'stackoverflow':{
        'usage':'stackoverflow',
        'arguments':0,
        'description':'Opens my stackoverflow profile',
        'fn':stackoverflowCmd
    },
    'getcv':{
        'usage':'getcv',
        'arguments':0,
        'description':'Request for my CV',
        'fn':getcvCmd
    }
}

def InputSanitizor(data):
    return data.replace('<','&lt;').replace('>','&gt;')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/user', methods=['POST'])
def user():
    global USERS
    try:
        data = json.loads(request.get_data().decode())
        print("Data : ", data, type(data))
        print("headers: ", str(request.headers.get('user_agent','UA')), str(request.remote_addr))
        username = InputSanitizor(data.get('username','Anonymous'))
        if username=='':
            username = 'Anonymous'
        if username not in USERS.keys():
            createUser(username)
        USERS[username]['access'].append((str(datetime.now()),str(request.headers.get('user_agent','UA')), str(request.remote_addr)))
        return jsonify({"msg": welcomeMsg.format(username)})
    except Exception as e:
        writeError(e)

@app.route('/command', methods=['POST'])
def command():
    global OPERATIONS
    try:
        data = json.loads(request.get_data().decode())
        print("Data : ", data)
        user = InputSanitizor(data.get('username','Anonymous'))
        command = InputSanitizor(data.get('command',''))
        if command=='':
            return jsonify({"msg": "<span id=\"error\"> Empty Command</span>"})
        cmds = command.strip().split(' ')
        cmd = cmds[0]
        args = cmds[1:]
        try:
            output = OPERATIONS[cmd]['fn'](user, args)
            return jsonify({"msg": output})
        except KeyError:
            return jsonify({"msg": '<span id="error">'+cmd+'</span> : Command Not found'})
        return jsonify({"msg": '<span id="error"'+cmd+'</span> : Error Processing command'})
    except Exception as e:
        writeError(e)

MASTER_USERNAME=os.environ.get('MASTER_USERNAME','admin')
MASTER_PASSWORD=os.environ.get('MASTER_PASSWORD','password')

@app.route('/users', methods=['GET','POST'])
def getUsers():
    global USERS
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username','')
        password = request.form.get('password','')
        if username==MASTER_USERNAME and password==MASTER_PASSWORD:
            return jsonify(USERS)
        return render_template('login.html')

@app.route('/save', methods=['GET'])
def saveUsers():
    global USERS
    with open('users.json','w') as f:
        json.dump(USERS, f, indent=4)
    return "<h1>Save Complete</h1>"
      
if __name__=="__main__":
    if os.path.isfile('users.json'):
        with open('users.json','r') as f:
            USERS = json.load(f)
    app.run()