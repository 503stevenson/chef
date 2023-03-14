from flask import Flask, render_template
from database import load_all_dishes

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/create")
def create():
    return render_template('create.html')

@app.route("/explore")
def explore():
    dishes = load_all_dishes()
    return render_template('explore.html', dishes=dishes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)