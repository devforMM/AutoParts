from Database.Database import local_session

def get_session():
    db=local_session()
    try:
        yield db
    finally:
        db.close()