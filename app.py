import boto3
import os
from flask import Flask, redirect, render_template, jsonify, request
from database import load_all_dishes, add_dish, load_dishes_by_country, load_dishes_by_ingredient, load_dishes_by_country_and_ingredient
from werkzeug.utils import secure_filename

#variables
formStepOne = False
Ingredientdata = False
error = False

#aws
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

#AWS Image Handler
def handleImage(image):
    if image:
        filename = secure_filename(image.filename)
        try:
            s3.upload_fileobj(
                image,
                os.getenv("AWS_BUCKET_NAME"),
                filename,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": image.content_type
                }
            )

        except Exception as e:
            # This is a catch all exception, edit this part to fit your needs.
            print("Something Happened: ", e)
            return e
    

        # after upload file to s3 bucket, return filename of the uploaded file
        return image.filename
    
#app
app = Flask(__name__)

#Routes
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
    filename = handleImage(request.files['file'])
    print(filename)
    newDish = request.form.to_dict()
    newDish['image'] = filename

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
    for dish in dishes:
        dish['url'] = "https://503stevensonchef.s3.us-east-2.amazonaws.com/" + dish['image']
    return render_template('explore.html', dishes=dishes)

@app.route("/dishes", methods=['POST'])
def showDishes():
    parameters = request.form.to_dict()
    
    if parameters['country'] != "" and parameters['ingredient'] != "":
        dishes = load_dishes_by_country_and_ingredient(parameters['country'], parameters['ingredient'])
    elif parameters['country'] != "":
        dishes = load_dishes_by_country(parameters['country'])
    elif parameters['ingredient'] != "":
        dishes = load_dishes_by_ingredient(parameters['ingredient'])
    else:
        dishes = load_all_dishes()
    for dish in dishes:
        dish['url'] = "https://503stevensonchef.s3.us-east-2.amazonaws.com/" + dish['image']
    return render_template('explore.html', dishes=dishes)
    
#json page to view dishes
@app.route("/api/dishes")
def list_dishes():
    dishes = load_all_dishes()
    return jsonify(dishes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)