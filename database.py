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
        for row in result.all():
            records.append(dict(row))
    return records