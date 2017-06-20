from flask import Flask
from flask import render_template,redirect,request
import os
from DbClass import DbClass
import jinja2



app = Flask(__name__)


@app.route('/')
def homepage():
    db = DbClass()
    huidigeWaardes = db.huidigeWaardeCo()
    huidigeWaardeCO = str(huidigeWaardes[0])

    db = DbClass()
    huidigeWaardes = db.huidigeWaardeCo2()
    huidigeWaardeCO2 = str(huidigeWaardes[0])
    print(huidigeWaardeCO2)

    db = DbClass()
    huidigeWaardes = db.huidigeWaardetemp()
    huidigeWaardeC = str(huidigeWaardes[0])

    db = DbClass()
    huidigeWaardes = db.huidigeWaardeluchtvocht()
    huidigeWaardeP = str(huidigeWaardes[0])



    return render_template('index.html',huidigeWaardeCO=huidigeWaardeCO,huidigeWaardeC=huidigeWaardeC,huidigeWaardeP=huidigeWaardeP,huidigeWaardeCO2=huidigeWaardeCO2)

@app.route('/CO')
def CO():
    db = DbClass()
    waardes = db.listCOtable()
    db = DbClass()
    waardes_graf = db.listCOgraf()
    list_waardes_graf = ['Date', 'CO']
    for waarde in waardes_graf:
        datumtime = str(waarde[0]) + " " + str(waarde[1])
        meetwaarde = [datumtime, int(waarde[2])]
        list_waardes_graf.append(meetwaarde)
    db = DbClass()
    huidigeWaardes = db.huidigeWaardeCo()
    huidigeWaarde = str(huidigeWaardes[0])
    kwaliteit = str(huidigeWaardes[1])
    print(huidigeWaardes)
    print(list_waardes_graf)
    # Db = DbClass()
    # waarden = DbClass.listCO2table(Db)
    # print(waarden)

    return render_template('CO.html',waardes = waardes,huidigeWaarde=huidigeWaarde,kwaliteit=kwaliteit)


@app.route('/CO2')
def CO2():
    db = DbClass()

    waardes = db.listCO2table()
    db = DbClass()
    waardes_graf = db.listCO2graf()
    list_waardes_graf = ['Year', 'Sales']
    for waarde in waardes_graf:
        datumtime = str(waarde[0]) + " " + str(waarde[1])
        meetwaarde = [datumtime,int(waarde[2])]
        list_waardes_graf.append(meetwaarde)
    db = DbClass()
    huidigeWaardes = db.huidigeWaardeCo2()
    huidigeWaarde = str(huidigeWaardes[0])
    verschil = str(huidigeWaardes[1])
    kwaliteit = str(huidigeWaardes[2])
    print(huidigeWaardes)
    return render_template('CO2.html',waardes=waardes,list_waardes_graf=list_waardes_graf,huidigeWaarde=huidigeWaarde,verschil=verschil,kwaliteit=kwaliteit)

@app.route('/temperature')
def temperature():
    db = DbClass()
    waardes = db.listtemptable()
    db = DbClass()
    waardes_graf = db.listtempgraf()
    list_waardes_graf = ['', 'Sales']
    for waarde in waardes_graf:
        datumtime = str(waarde[0]) + " " + str(waarde[1])
        meetwaarde = [datumtime, float(waarde[2]),float(waarde[3])]
        list_waardes_graf.append(meetwaarde)
    db = DbClass()
    huidigeWaardes = db.huidigeWaardetemp()
    huidigeWaardeC = str(huidigeWaardes[0])
    verschilC = str(huidigeWaardes[1])
    huidigeWaardeF= str(huidigeWaardes[2])
    verschilF= str(huidigeWaardes[3])
    print(list_waardes_graf)
    return render_template('temperature.html',waardes=waardes,list_waardes_graf=list_waardes_graf,huidigeWaardeC=huidigeWaardeC,huidigeWaardeF=huidigeWaardeF,verschilC=verschilC,verschilF=verschilF)

@app.route('/humidity')
def humidity():
    db = DbClass()
    waardes = db.listluchtvochttable()
    db = DbClass()
    waardes_graf = db.listluchtvochtgraf()
    list_waardes_graf = ['', 'Sales']
    for waarde in waardes_graf:
        datumtime = str(waarde[0]) + " " + str(waarde[1])
        meetwaarde = [datumtime, float(waarde[2])]
        list_waardes_graf.append(meetwaarde)
    db = DbClass()
    huidigeWaardes = db.huidigeWaardeluchtvocht()
    huidigeWaarde = str(huidigeWaardes[0])
    verschil = str(huidigeWaardes[1])
    kwaliteit = str(huidigeWaardes[2])
    print(list_waardes_graf)
    return render_template('humidity.html',waardes=waardes, list_waardes_graf=list_waardes_graf,
                           huidigeWaarde=huidigeWaarde, verschil=verschil, kwaliteit=kwaliteit)

@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/settings_controleren')
def settings_form():
    dbminuten = DbClass()
    dbrelay = DbClass()
    dbRelay_Gas = DbClass()
    dbRelay_Motor = DbClass()

    relay = request.form["relay"]
    safety_relay = request.form["safety_relay"]
    motorrelay = request.form["motorrelay"]
    minuten = request.form["minuten"]

    dbminuten.update_minuten(minuten)
    dbrelay.update_relay(relay)
    dbRelay_Gas.safety_relay(safety_relay)
    dbRelay_Motor.Motor_relay(motorrelay)
    return render_template('settings.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT",8080))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=True)


