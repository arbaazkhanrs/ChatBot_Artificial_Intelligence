import time
time.clock = time.time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask import Flask,render_template,request,redirect
from chatterbot import ChatBot, conversation
from chatterbot.trainers import ChatterBotCorpusTrainer
from werkzeug.utils import redirect



cred = credentials.Certificate("kee.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://storemyname-2e105-default-rtdb.firebaseio.com/'})


dbref = db.reference('/')
# dbref.set({'test' : '123'})
flaskobj = Flask(__name__)
chatbotobj = ChatBot('Ron Obvious')
#trainer = ChatterBotCorpusTrainer(chatbotobj)
# trainer.train("chatterbot.corpus.english")

responseop = [({"responder":"bot",
            "message":"Welcome to AI chat"})]

mobileno = ""

@flaskobj.route('/', methods=['GET','POST'])
def homepage():
    global responseop;
    if(request.form):
        btnval = request.form['btn']
        if (btnval == "visitor"):
            return render_template("visitorform.html");
        elif (btnval == "admin"):
            dbref = db.reference("/visitors")
            dbcnt = dbref.get()
            return render_template("visitorstabledisplay.html",web = dbcnt);

    else:
        return render_template("home.html")


# This session is to store information into db 
@flaskobj.route('/regform', methods=['POST'])
def contactformpage():
    global responseop, mobileno;
    if(request.form):
        btnval = request.form['submitbtn']
        umv = 0
        if (btnval == "sub"):
            visitordbref = db.reference("/visitors")
            dbcnt = visitordbref.get()
            username = request.form['Username']
            email = request.form['email']
            mobileno = request.form['mobileno']
            interestedbranch = request.form['Interestedbranch']
            # dbref.set({"name":username,"email":email, "mobileno":mobileno,"Interestedbranch": interestedbranch}) 
          
            conversationcnt = [({"responder":"bot","message":"Welcome to AI chat"})]
            for index, row in enumerate(dbcnt):
                if(index > 0):
                    if(row["mobileno"] == mobileno):
                        umv = 1;
                        conversationcnt = row["conversation"]
                        break;
            if(umv == 0):

                dbcnt.append({"name":username,"email": email,"mobileno":mobileno,"Interestedbranch":interestedbranch,"conversation":responseop})
                visitordbref.set(dbcnt)
        return render_template("Chatbots.html",op=conversationcnt);

    else:
        return render_template("visitorform.html")




@flaskobj.route('/bot', methods=['POST'])
def botpage():
    if(request.form):
        global mobileno;
        indexval = 0;
        conversationcnt = [{}]
        var1 = request.form['UserId_1']
        botresponse = chatbotobj.get_response(var1)
        visitordbref = db.reference("/visitors")
        dbcnt = visitordbref.get()
        for index,row in enumerate(dbcnt):
            if(index > 0):
                if(row["mobileno"] == mobileno):
                    indexval = index;
                    conversationcnt = row["conversation"]
                    break; 
        conversationcnt.append({"id":len(conversationcnt)+1,
                        "responder":"user",
                        "message":var1})
        conversationcnt.append({"id":len(conversationcnt)+1,
                            "responder":"bot",
                            "message":str(botresponse)})
        #indexval is key where the conversation will be stored 
        dbcnt[indexval]["conversation"]=conversationcnt;
        visitordbref.set(dbcnt);

                   
        return render_template("Chatbots.html",op=conversationcnt)
    
    else:
        return render_template("Chatbots.html")



@flaskobj.route('/botback', methods=['POST'])
def botbackpage():
    btnval=""
    if(request.form):
        btnval=request.form['btn']
        if (btnval=="exit"):
            return redirect("/");

    else:
        return render_template("Chatbots.html", az=btnval)
    


@flaskobj.route('/deletedata', methods=['POST'])
def deletepage():
    btnval=""
    if(request.form):
        btnval=request.form['btn']
        if (btnval=="logout"):
            return redirect("/");
        elif(btnval=="del"):
            visitordbref=db.reference("/visitors")
            visitordbref.delete()
            visitordbref.set([{"test":123}])
            dbcnt=visitordbref.get()
            return render_template("visitorstabledisplay.html" , web = dbcnt)

    else:
        return render_template("visitorstabledisplay.html")


@flaskobj.route('/btnsite', methods=['POST'])
def btnsitepage():
    btnval = ""
    username = ""
    if(request.form):
        btnval = request.form['btn']
        visitordbref = db.reference("/visitors")
        dbcnt = visitordbref.get()
        for index,row in enumerate(dbcnt):
                if(index > 0):
                    if(row["mobileno"] == btnval):
                        conversationcnt = row["conversation"]
                        username=row['name']
                        break;
            
        return render_template("admins.html",op = conversationcnt ,az = username);
    else:
        return render_template("Chatbots.html", az = btnval)


    
@flaskobj.route('/clearchat', methods=['POST'])
def clearchat():
    btnval=""
    if(request.form):
        btnval=request.form['btn']
        if (btnval=="exit"):
            return redirect("/");
        elif(btnval=="clear"):
            conversationcnt = db.reference("/conversation")
            conversationcnt.delete()
            conversationcnt.set([{"test":123}])
            dbcnt=conversationcnt.get()
           
            return render_template("admins.html" )

    else:
        return render_template("Chatbots.html")



        



# [==] CodTdo

if __name__ == '__main__':
    flaskobj.run(debug = True, host = '0.0.0.0')   