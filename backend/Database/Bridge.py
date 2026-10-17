from Database.Database import session_maker,test_session_maker

def get_session():
    db=session_maker()
    try:
        yield db
    finally:
        db.close()
        
    
def test_get_session():
    test_db=test_session_maker()
    try:
        yield test_db
    finally:
        test_db.close()