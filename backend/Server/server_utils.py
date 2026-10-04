from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,Request
from datetime import datetime,timedelta,timezone
from Database.Bridge import get_session
from Database.models import Seller,Buyer,Supplier
SECRET_KEY="SECRET_KEY"
CRYPT_SCHEMES="bcrypt"
ALGO="HS256"
context=CryptContext(schemes=[CRYPT_SCHEMES],deprecated="auto")



def hash_password(password):
    return context.hash(password)


def verifiy_password(password,hashed_password):
    return context.verify(password,hashed_password)


def expire_time():
    return datetime.now(timezone.utc)+timedelta(minutes=300)


def create_token(data:dict):
    try:
        data_copy=data.copy()
        data_copy["exp"]=expire_time()
        return jwt.encode(data_copy,key=SECRET_KEY,algorithm=ALGO)
    except Exception as e:
        HTTPException(status_code=401,detail=f"error creating token : {e}")

def get_current_buyer(request:Request,database=Depends(get_session)):
    try:
        token=request.cookies.get("access_token")
        buyer_data=jwt.decode(token,key=SECRET_KEY,algorithms=ALGO)
        if buyer_data:
            buyer=database.query(Buyer).filter(buyer_data["id"]==Buyer.id).first()
            if buyer:
                return buyer
        else:
                raise HTTPException(detail="forbiden you are not a buyer ",status_code=403)
        raise HTTPException(status_code=401, detail="invalid token  ")
    except Exception as e :
        raise HTTPException(status_code=400,detail=f" Token null: {e}")





def get_current_seller(request:Request,database=Depends(get_session)):
    try:
        token=request.cookies.get("access_token")
        seller_Data=jwt.decode(token,key=SECRET_KEY,algorithms=ALGO)
        if seller_Data:
            seller=database.query(Seller).filter(seller_Data["id"]==Seller.id).first()
            if seller:
              return seller
            else:
                raise HTTPException(status_code=403,detail="frobiden you are not a seller ")
        raise HTTPException(status_code=401, detail="invalid token  ")
    except Exception as e :
        raise HTTPException(status_code=400,detail=f" server error: {e}")



def get_current_supplier(request:Request,database:Session=Depends(get_session)):
    try:
       
       token=request.cookies.get("access_token")
       supplier_data=jwt.decode(token,SECRET_KEY,algorithms=ALGO)
       if supplier_data:
           supplier=database.query(Supplier).filter(Supplier.id==supplier_data["id"]).first()
           if supplier:
               return supplier
           else:
               raise HTTPException(status_code=404,detail="Supplier Not found")
       else:
           raise HTTPException(status_code=400,detail="Token invalid")
           
    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)



    

    

