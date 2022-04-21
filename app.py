from flask import Flask, render_template,redirect,url_for,request

app = Flask(__name__)
@app.route("/")
def welcome() :
    data = [
        ("01-02-2021",3309),
        ("02-02-2021",2609),
        ("03-02-2021",2409),
        ("04-02-2021",6009),
        ("05-02-2021",7309),
        ("06-02-2021",8309),
        ("07-02-2021",6043),
    ]
    
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("index.html", labels=labels, values=values)
@app.route("/<coin>")
def coin(coin) :
    data = [
        ("01-02-2021",3309),
        ("02-02-2021",2609),
        ("03-02-2021",2409),
        ("04-02-2021",6009),
        ("05-02-2021",7309),
        ("06-02-2021",8309),
        ("07-02-2021",6043),
    ]
    
    labels = [row[0] for row in data]
    values = [row[1] for row in data]
    return render_template("{}.html".format(coin), labels=labels, values=values)

    
if __name__== '__main__' :
    app.run(debug=True)
    