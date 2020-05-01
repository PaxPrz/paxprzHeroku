from flask import Flask, request, render_template, jsonify, flash, redirect
import json
from datetime import datetime
import time

templates="templates"
USERLOGS={}

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

def helpCmd(args):
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

def whoispaxCmd(args):
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


OPERATIONS={
    'help':{
        'usage':'help',
        'arguments':0,
        'description':"Shows list of commands and their descriptions",
        'fn': helpCmd
    },
    'ls':{
        'usage':'ls',
        'arguments':0,
        'description':'Lists files inside current folder'
    },
    'whoispax':{
        'usage':'whoispax',
        'arguments':0,
        'description':'A quick intro of myself',
        'fn':whoispaxCmd
    },
    'clear':{
        'usage':'clear',
        'arguments':0,
        'description':'Clears the terminal'
    }
}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/user', methods=['POST'])
def user():
    global USERLOGS
    try:
        data = json.loads(request.get_data().decode())
        print("Data : ", data, type(data))
        print("headers: ", str(request.headers.get('user_agent','UA')), str(request.remote_addr))
        username = data.get('username','Anonymous')
        if username=='':
            username = 'Anonymous'
        if username not in USERLOGS.keys():
            USERLOGS[username]={'access':[], 'job':[], 'name':[], 'contact':[]}
        USERLOGS[username]['access'].append(str(datetime.now()))
        return jsonify({"msg": welcomeMsg.format(username)})
    except Exception as e:
        writeError(e)

@app.route('/command', methods=['POST'])
def command():
    global OPERATIONS
    try:
        data = json.loads(request.get_data().decode())
        print("Data : ", data)
        command = data.get('command','')
        if command=='':
            return jsonify({"msg": "<span id=\"error\"> Empty Command</span>"})
        cmds = command.strip().split(' ')
        cmd = cmds[0]
        args = cmds[1:]
        try:
            output = OPERATIONS[cmd]['fn'](args)
            return jsonify({"msg": output})
        except KeyError:
            return jsonify({"msg": '<span id="error">'+cmd+'</span> : Command Not found'})
        return jsonify({"msg": '<span id="error"'+cmd+'</span> : Error Processing command'})
    except Exception as e:
        writeError(e)
      
if __name__=="__main__":
    app.run()