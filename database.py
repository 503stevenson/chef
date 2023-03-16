from sqlalchemy import create_engine, text
import os

if os.getenv('WHEREAMI') != 'hosted':
    from dotenv import load_dotenv
    load_dotenv()

user=os.getenv('USER')
password=os.getenv('PASSWORD')
host=os.getenv('HOST')

credentials = "mysql+pymysql://" + user + ":" +  password + "@" + host + "/chef?charset=utf8mb4"
engine = create_engine(credentials, connect_args={
    "ssl": {
        "ssl_ca": "/etc/ssl/cert.pem"
    }
})

#METHODS      
def load_all_dishes():
    with engine.connect() as conn:
        result=conn.execute(text('select * from dishes'))

        records = []
        mapping = {0: 'id', 1: 'dishName', 2: 'cookTime', 3: 'country', 4: 'ingredients', 5: 'directions', 6: 'image'} 
        for row in result.all():
            i = 0
            record = {}
            for item in row:
                record[mapping[i]] = item
                i+= 1
            records.append(record)
    return records

def load_dishes_by_country(country):
    query = 'select * from dishes where country=\'' + country + '\''
    with engine.connect() as conn:
        result = conn.execute(text(query))

        records = []
        mapping = {0: 'id', 1: 'dishName', 2: 'cookTime', 3: 'country', 4: 'ingredients', 5: 'directions', 6: 'image'} 
        for row in result.all():
            i = 0
            record = {}
            for item in row:
                record[mapping[i]] = item
                i+= 1
            records.append(record)
    return records

def load_dishes_by_ingredient(ingredient):
    query = 'select * from dishes where ingredients like \'%' + ingredient + '%\''
    with engine.connect() as conn:
        result = conn.execute(text(query))

        records = []
        mapping = {0: 'id', 1: 'dishName', 2: 'cookTime', 3: 'country', 4: 'ingredients', 5: 'directions', 6: 'image'} 
        for row in result.all():
            i = 0
            record = {}
            for item in row:
                record[mapping[i]] = item
                i+= 1
            records.append(record)
    return records

def load_dishes_by_country_and_ingredient(country, ingredient):
    query = 'select * from dishes where ingredients like \'%' + ingredient + '%\'' + 'and country like \'%' + country + '%\''
    with engine.connect() as conn:
        result = conn.execute(text(query))

        records = []
        mapping = {0: 'id', 1: 'dishName', 2: 'cookTime', 3: 'country', 4: 'ingredients', 5: 'directions', 6: 'image'} 
        for row in result.all():
            i = 0
            record = {}
            for item in row:
                record[mapping[i]] = item
                i+= 1
            records.append(record)
    return records

def add_dish(dish):
    with engine.connect() as conn:
        dishName=dish['name']
        cookTime=dish['time']
        country=dish['country']
        ingredients=dish['ingredients']
        directions=dish['directions']
        image=dish['image']
        values = '\'' + dishName + '\', \'' + cookTime + '\', \'' + country + '\', \'' + ingredients + '\', \'' + directions + '\', \'' + image + '\''
        query = text("INSERT INTO dishes(dishName, cookTime, country, ingredients, directions, image) VALUES(" + values + ")")

        conn.execute(query)
    
load_dishes_by_country_and_ingredient('Canada', 'love')