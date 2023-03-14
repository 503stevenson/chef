from sqlalchemy import create_engine, text

credentials = "mysql+pymysql://jdas3sptw9rruv3swudv:pscale_pw_WabFoSBA7eTz9RHNEuIa0cammWk6mVruKNGYoc4Cso3@us-east.connect.psdb.cloud/chef?charset=utf8mb4"
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

def add_dish(dish):
    with engine.connect() as conn:
        dishName=dish['name']
        cookTime=dish['time']
        country=dish['country']
        ingredients=dish['ingredients']
        directions=dish['directions']
        image=dish['image']
        values = '\'' + dishName + '\', \'' + cookTime + '\', \'' + country + '\', \'' + ingredients + '\', \'' + directions + '\''
        query = text("INSERT INTO dishes(dishName, cookTime, country, ingredients, directions) VALUES(" + values + ")")

        conn.execute(query)
    
print(load_all_dishes())