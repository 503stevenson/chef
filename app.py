from flask import Flask, flash, redirect, render_template, jsonify, request
from database import load_all_dishes, add_dish

#variables
formStepOne = False
Ingredientdata = False
error = False

#app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/create")
def create():
    global error
    if error:
        error = False
        return render_template('create.html', error=True)
    else:
        return render_template('create.html', error=False)

@app.route("/create/ingredients", methods=['post'])
def postIngredients():
    global formStepOne
    global Ingredientdata
    formStepOne = True
    Ingredientdata = request.form.to_dict()
    return render_template('formTwo.html')

@app.route("/create/details", methods=['post'])
def postDish():
    global Ingredientdata
    global formStepOne
    global error
    newDish = request.form.to_dict()

    if Ingredientdata != False and Ingredientdata != None and formStepOne:
        newDish['ingredients'] = Ingredientdata['ingredients']
        newDish['directions'] = Ingredientdata['directions']
        Ingredientdata = False
        formStepOne = False
        add_dish(newDish)
        return jsonify(newDish)
    Ingredientdata = False
    formStepOne = False
    error = True
    return redirect("/create")

@app.route("/explore")
def explore():
    dishes = load_all_dishes()
    return render_template('explore.html', dishes=dishes)

#json page to view dishes
@app.route("/api/dishes")
def list_dishes():
    dishes = load_all_dishes()
    return jsonify(dishes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)