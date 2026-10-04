from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DB_URL = "postgresql+psycopg://postgres:qwerty@127.0.0.1:5432/Autoparts"
engine=create_engine(url=DB_URL)
local_session=sessionmaker(bind=engine,autoflush=False)
Base=declarative_base()
