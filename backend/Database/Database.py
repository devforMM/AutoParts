from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv



load_dotenv()


database_name=os.getenv("DataBase_name")
database_user=os.getenv("DataBase_user")
database_password=os.getenv("DataBase_password")
database_testname=os.getenv("DataBase_test")


base=declarative_base()

db_url = f"postgresql+psycopg://{database_user}:{database_password}@127.0.0.1:5432/{database_name}"


db_url_test=f"postgresql+psycopg://{database_user}:{database_password}@127.0.0.1:5432/{database_testname}"



engine=create_engine(url=db_url)
session_maker=sessionmaker(bind=engine,autoflush=False)



test_engine=create_engine(url=db_url_test)
test_session_maker=sessionmaker(bind=test_engine,autoflush=False)




