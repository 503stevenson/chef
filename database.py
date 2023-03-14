from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
host=os.getenv("HOST")
db=os.getenv("DATABASE")
user=os.getenv("USER")
password=os.getenv("PASSWORD")

credentials = "mysql+pymysql://" + user + ":" + password + "@" + host + "/" + db + "?charset=utf8mb4"
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