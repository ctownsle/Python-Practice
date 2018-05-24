import os
import subprocess
from os import walk
import glob
import json
import numpy as np
import zipfile
import smtplib
import getpass
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

def main():
    directory = raw_input("Please Enter a Directory: \n")
    #print('Hello', jeff)
    #print("directory")
    iterateOverDir(directory)

def iterateOverDir(directory):
    dirlist = glob.glob(directory + '/*')
    for filename in dirlist:
        subprocess.call(['wc', '-l', filename])

def regexCFile():
    directory = '/home/chris/Documents/CSC344/a1/'
    for file in os.listdir(directory):
        #regex C file
        # types are int, char, void, struct
        # check which types we've already checked
        
        if file.endswith('.c'):
            symbolList = []
            typelist = ['int', 'char', 'void', 'struct', 'letter']
            # kill punctuation
            alreadyChecked = []
            punctuation = ['{', ';', '[', "'", "//", ")", "*", "(", ","]
            fl = open(directory + file)
            for line in fl:
                # fix lines with opening parens
                line.replace("(", "( ")
                for punct in punctuation:
                    line = line.replace(punct, " ")
                listoflines = line.split()
                # range function essentially works as a counter
                for i in range(len(listoflines)):
                    if i < len(listoflines) - 1:
                        symbol = listoflines[i + 1]
                        if listoflines[i] in typelist and symbol not in alreadyChecked:
                            alreadyChecked.append(symbol)
                            symbolList.append(symbol.replace('(', ""))
                        if listoflines[i].endswith('(') and listoflines[i] not in alreadyChecked:
                            symbol = listoflines[i].replace('(', "")
                            alreadyChecked.append(word)  
                            if not symbol == "":
                                symbolList.append(symbol)
            return symbolList

def regexClojureFile():
    directory = '/home/chris/Documents/CSC344/a2/'
    for file in os.listdir(directory):

        if file.endswith('.clj'):
            #types are defn, def
            symbolList = []
            typelist = ['defn', 'def']
            alreadyChecked = []
            fl = open(directory + file)
            for line in fl:
                line = line.replace('(', "");
                line = line.replace(')', "")
                listoflines = line.split()
                for i in range(len(listoflines)):
                    if listoflines[i] in typelist and listoflines[i+1] not in alreadyChecked:
                        symbol = listoflines[i+1].replace("*", "")
                        alreadyChecked.append(symbol)
                        symbolList.append(symbol)
            return symbolList
def regexScalaFile():
    directory = '/home/chris/Documents/CSC344/a3/'
    for file in os.listdir(directory):

        if file.endswith('.scala'):
            
            #types are val, var, class, def, object
            typelist = ['val', 'var', 'def', 'class', 'object']
            punctuation = [')', ':', '{', '}', '"', ',', "!",
                        "'", ';', '-', '==' , 'if', '.', '(', '//']
            alreadyChecked = []
            symbolList = []
            fl = open(directory + file)
            for line in fl:
                line = line.replace("(", "( ")
                line = line.replace(".", " ")
                for punct in punctuation:
                    line = line.replace(punct, " ")
                listoflines = line.split()
                for i in range(len(listoflines)):
                    if i < len(listoflines) - 1:
                        if listoflines[i] in typelist and listoflines[i + 1] not in alreadyChecked:
                            if not line.startswith('//'):
                                alreadyChecked.append(listoflines[i+1])
                                symbol = listoflines[i+1]
                                if symbol != "":
                                    symbolList.append(symbol)
                        if listoflines[i].endswith("(") and not listoflines[i] in alreadyChecked:
                            alreadyChecked.append(listoflines[i])
                            symbol = listoflines[i]
                            if symbol != "":
                                symbolList.append(symbol)
            return symbolList

def regexPrologFile():
    directory = '/home/chris/Documents/CSC344/a4/'
    for file in os.listdir(directory):

        if file.endswith('.pl'):
            #want names of rules and vars generated in rules
            #looking for '=' and 'is'
            alreadyChecked = []
            symbolList = []
            punctuation = ['(', '%']
            assignments = ["=", "is"]
            fl = open(directory + file)
            for line in fl:
                line = line.rstrip()
                if not line.startswith("%"):
                    if line.endswith(":-"):
                        line = line.replace('(', "( ")
                        for punct in punctuation:
                            line = line.replace(punct, " ")
                        listoflines = line.split()
                        if listoflines[0] not in alreadyChecked:
                            alreadyChecked.append(listoflines[0])
                            symbol = listoflines[0]
                            if symbol != "":
                                symbolList.append(symbol)
                    else:
                        listoflines = line.split()
                        if len(listoflines) > 1:
                            if listoflines[1] in assignments:
                                if listoflines[0] not in alreadyChecked and not listoflines[0].startswith("%"):
                                    alreadyChecked.append(listoflines[0])
                                    symbol = listoflines[0]
                                    if symbol != "":
                                        symbolList.append(symbol)
            return symbolList

def regexPythonFile():
    directory = '/home/chris/Documents/CSC344/a5/'
    for file in os.listdir(directory):

        if file.endswith('.py'):
            #def  then check for = 
            alreadyChecked = []
            symbolList = []
            punctuation = ['(', ')', ':', '[', ","]
            declares = ["def", "for"]
            assignment = ["="]
            fl = open(directory + file)
            for line in fl:
                line = line.rstrip()
                line = line.replace("(", " (")
                for punct in punctuation:
                    line = line.replace(punct, " ")
                if not line.startswith("#"): 
                    listoflines = line.split()
                    if len(listoflines) > 1:
                        if listoflines[0] in declares and not listoflines[1] in alreadyChecked:
                            alreadyChecked.append(listoflines[1])
                            symbol = listoflines[1]
                            if symbol != "":
                                symbolList.append(symbol)
                        elif listoflines[1] in assignment and not listoflines[0] in alreadyChecked:
                            alreadyChecked.append(listoflines[0])
                            symbol = listoflines[0]
                            if symbol != "":
                                symbolList.append(symbol)

            return symbolList



def createCFile():
    path = '/home/chris/Documents/CSC344/a1/ChristopherTownsleyassign_1.c'
    symlist = regexCFile()
    command_stdout = subprocess.check_output(['wc', '-l', path])
    data = {}
    data['symbols'] = symlist
    data['filename'] = 'ChristopherTownsleyassign_1.c'
    splitstring = command_stdout.rstrip("\n").split(" ")
    mynum = splitstring[0]
    data['filesize'] = mynum
    with open('/home/chris/Documents/CSC344/csymbols.json', 'w') as outfile:
        json.dump(data, outfile)

def createClojureFile():
    path = '/home/chris/Documents/CSC344/a2/core.clj'
    symlist = regexClojureFile()
    command_stdout = subprocess.check_output(['wc', '-l', path])
    data = {}
    data['symbols'] = symlist
    data['filename'] = 'core.clj'
    splitstring = command_stdout.rstrip("\n").split(" ")
    mynum = splitstring[0]
    data['filesize'] = mynum
    with open('/home/chris/Documents/CSC344/cljsymbols.json', 'w') as outfile:
        json.dump(data, outfile)
def createScalaFile():
    path = '/home/chris/Documents/CSC344/a3/Main.scala'
    symlist = regexScalaFile()
    command_stdout = subprocess.check_output(['wc', '-l', path])
    data = {}
    data['symbols'] = symlist
    data['filename'] = 'Main.scala'
    splitstring = command_stdout.rstrip("\n").split(" ")
    mynum = splitstring[0]
    data['filesize'] = mynum
    with open('/home/chris/Documents/CSC344/scalasymbols.json', 'w') as outfile:
        json.dump(data, outfile)

def createPrologFile():
    path = '/home/chris/Documents/CSC344/a4/mejeff.pl'
    symlist = regexPrologFile()
    command_stdout = subprocess.check_output(['wc', '-l', path])
    data = {}
    data['symbols'] = symlist
    data['filename'] = 'mejeff.pl'
    splitstring = command_stdout.rstrip("\n").split(" ")
    mynum = splitstring[0]
    data['filesize'] = mynum
    with open('/home/chris/Documents/CSC344/prologsymbols.json', 'w') as outfile:
        json.dump(data, outfile)
def createPythonFile():
    path = '/home/chris/Documents/CSC344/a5/micro.py'
    symlist = regexPythonFile()
    command_stdout = subprocess.check_output(['wc', '-l', path])
    data = {}
    data['symbols'] = symlist
    data['filename'] = 'micro.py'
    splitstring = command_stdout.rstrip("\n").split(" ")
    mynum = splitstring[0]
    data['filesize'] = mynum
    with open('/home/chris/Documents/CSC344/pythonsymbols.json', 'w') as outfile:
        json.dump(data, outfile)

def createHtmlFile():
    html_str = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<style>
    td.symbol_cell {
        max-width: 500px;
        word-wrap: break-word;
    }

    table.a {
    table-layout: fixed;
    width: 180px;
    grid-auto-rows: 500px;
    
}
</style>
</head>
<body>
    <h1> CSC344 Assignment5 </h1>
<script type="text/javascript">
    window.onload = function main(){

const cobj = getJson('./csymbols.json');
const cljobj = getJson('./cljsymbols.json');
const scaobj = getJson('./scalasymbols.json');
const probj = getJson('./prologsymbols.json');
const pyobj = getJson('./pythonsymbols.json');

insertRow(cobj, 1);
insertRow(cljobj, 2);
insertRow(scaobj, 3);
insertRow(probj, 4);
insertRow(pyobj, 5);
    
}

function getJson(url) {
var request = new XMLHttpRequest();
request.overrideMimeType('application/json');
request.open("GET", url, false);
request.send(null)
return JSON.parse(request.responseText);
}

function insertRow(json, index) {
    const table = document.getElementById('myTable');

    const row = table.insertRow(index);

    const col1 = row.insertCell(0);
    const col2 = row.insertCell(1);
    const col3 = row.insertCell(2);

    col3.className = 'symbol_cell';
// var link = json.filename.link("<div style=\"height:100%;width:=100%""./a" + index + "/" + json.filename)
    var link = json.filename.link("./a" + index + "/" + json.filename)
    col1.innerHTML = link;
    col2.innerHTML = json.filesize;
    col3.innerHTML = json.symbols;
}
    </script>
    <p><a href="csymbols.json" download> csymbols.json </a></p>
    <p><a href="cljsymbols.json" download> clojuresymbols.json </a></p>
    <p><a href="scalasymbols.json" download> scalasymbols.json </a></p>
    <p><a href="prologsymbols.json" download> prologsymbols.json </a></p>
    <p><a href="pythonsymbols.json" download> pythonsymbols.json </a></p>
    <table id="myTable" rules="all">
        <tbody>
        <tr>
            <th>Filename</th>
            <th>Filesize</th>
            <th>Symbols</th>
        </tr>
        </tbody>
    </table>
</body>
</html>
    """

    html_file = open("/home/chris/Documents/CSC344/index.html", "w")
    html_file.write(html_str)
    html_file.close()

def createZipFile():
    zipf = zipfile.ZipFile('CSC344.jeff', 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('.././'):
        for file in files:
            if not file.endswith('.jeff'):
                zipf.write(os.path.join(root, file))
    zipf.close()

def sendMail():

    emailer = "ctownsle@oswego.edu"
    to = raw_input("Enter your email address: ")
    print("Email Address: " + emailer + '\n' + to)
    password = getpass.getpass()

    message = MIMEMultipart()
    message["From"] = emailer
    message["To"] = to
    message["Subject"] = "Assignment 5 Submission"
    part = MIMEBase('application', 'zip')
    part.set_payload(open("CSC344.jeff", 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 
                    'attachment; filename="CSC344.jeff"')
    message.attach(part)

    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpObj.ehlo(); smtpObj.starttls(); smtpObj.ehlo();
    smtpObj.login(emailer, password)
    smtpObj.sendmail(emailer, to, message.as_string())
    smtpObj.close()
    print("Successfully sent email")


createCFile()
createClojureFile()
createScalaFile()
createPrologFile()
createPythonFile()
createHtmlFile()
createZipFile()
sendMail()