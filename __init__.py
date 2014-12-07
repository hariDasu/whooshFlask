from flask import Flask,request
from flask import request,render_template
from flask_bootstrap import Bootstrap
from infoSeek.infoScores import InfoSeeker
from evaluate.evaluate import doEvaluate
from spellCheck.correct import doyoumean


def createApp():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app=createApp();
@app.route("/index")
def index():
    return render_template('index.html');


@app.route("/")
def boots():
    return render_template('whoosh.html');


@app.route("/seekInfo")
def initSeeker():
    retModel=request.args.get("retModel")
    qExpansion=request.args.get("qExpansion")
    uQuery=request.args.get("uQuery")
    print (retModel, qExpansion, uQuery)
    is1=InfoSeeker()
    is1.initSeeker(retrMethod=retModel)
    return is1.initQuery(userQueryString=uQuery, expModel=qExpansion)


@app.route("/expType")
def expResults():
    qExpansion=request.args.get("exp")
    print (retModel, qExpansion, uQuery)
    is1=InfoSeeker()
    is1.initSeeker(retrMethod=retModel)
    return is1.initQuery(userQueryString=uQuery, expModel=qExpansion)

@app.route("/seekTopic")
def evaluate():
    nVal=request.args.get("nVal")
    intVal=int(nVal)
    topic=request.args.get("topic");
    intTopic=int(topic)
    values = doEvaluate(intTopic,intVal)
    return values


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
