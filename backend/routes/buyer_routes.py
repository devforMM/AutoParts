from Database.models import Buyer,Store
from Server.server_utils import get_current_buyer
from Database.Bridge import get_session
from fastapi import Request,HTTPException,APIRouter,Depends,Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from Database.models import Buyer,Store,Purchase,Part,Sale
from Server.server_utils import verifiy_password,create_token,hash_password
templates=Jinja2Templates(directory="../front-end/buyer")

buyer_router=APIRouter(tags=["buyer"],prefix="/buyer")


####################################### templates #############################################################
@buyer_router.get("/login")
def login_template(request:Request):
    try:
        return templates.TemplateResponse(
            request=request,
            name="LoginTemplate.html",
        )

    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)


@buyer_router.get("/register")
def register_template(request:Request):
    try:
         return templates.TemplateResponse(
            name="RegisterTemplate.html",
            request=request
        )

    except Exception as e:
        raise HTTPException(detail=f"Server Error : {e}",status_code=400)

@buyer_router.get("/dashboard")
def dashboard_template(request:Request,buyer=Depends(get_current_buyer),database:Session=Depends(get_session)):
    try:
        stores=database.query(Store).all()
        return templates.TemplateResponse(
            name="DashboardTemplate.html",
            request=request,
            context={
                "buyer":buyer,
                "len_purchases":len(buyer.purchases),
                "len_stores":len(stores)
            }
        )


    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)




@buyer_router.get("/purchases")
def purchases_template(request:Request,buyer=Depends(get_current_buyer),database:Session=Depends(get_session)):
    try:
        
        return templates.TemplateResponse(
            request=request,
            name="StoresTemplate.html",
            context={
                "purchases":buyer.purchases,

            }
        )

    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)
        




@buyer_router.get("/stores")
def stores_template(request:Request,buyer=Depends(get_current_buyer),database:Session=Depends(get_session)):
    try:
        stores=database.query(Store).all()
        return templates.TemplateResponse(
            request=request,
            name="StoresTemplate.html",
            context={
                "stores":stores
            }
        )

    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)
        





@buyer_router.get("/store_details")
def store_template(request:Request,store_id:int,buyer=Depends(get_current_buyer),database:Session=Depends(get_session)):
    try:
        store=database.query(Store).filter(Store.id==store_id).first()
        return templates.TemplateResponse(
            request=request,
            name="StoreDetailsTemplate.html",
            context={
                "store":store,
                "parts":store.parts
            }
        )


    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)




#########################################################################################################################################

@buyer_router.post("/register")
def  register(request:Request,first_name=Form(...),last_name=Form(...),
              email=Form(...),password=Form(...),adress=Form(...),phone_number=Form(...),
              database:Session=Depends(get_session)

):
    try:
        new_buyer=Buyer(first_name=first_name,last_name=last_name,adress=adress,phone_number=phone_number,email=email,password=hash_password(password))
        database.add(new_buyer)
        database.commit()
        return templates.TemplateResponse(request=request,name="LoginTemplate.html")
    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)




@buyer_router.post("/login")
def login(request:Request,email=Form(...),password=Form(...),database:Session=Depends(get_session),):
    try:
        buyer=database.query(Buyer).filter(Buyer.email==email).first()
        if buyer:
            if verifiy_password(password,buyer.password):
                token=create_token({"id":buyer.id,"email":buyer.email})
                reponse=RedirectResponse(
                    url="/buyer/dashboard",
                    status_code=303
                )
                reponse.set_cookie(
                    key="access_token",
                    value=token,
                    httponly=False
                )
                return reponse
            else:
                return templates.TemplateResponse(
                    request=request,
                    name="LoginTemplate.html",
                    context={
                        "message":"Invalid Password"
                    }
                )
        else:
            return templates.TemplateResponse(
                name="LoginTemplate.html",
                request=request,
                context={
                    "message":"Email Invalid"
                }
            )



    except Exception as e:
        return templates.TemplateResponse(
            name="LoginTemplate.html",
            request=request,
            context={
                "error_message":f"Error Message: {e}"
            }
        )

from datetime import datetime


@buyer_router.post("/purchase")
def purchase_part(request:Request,store_id:int,parts_ids:list[int]=Form(...),quantities:list[int]=Form(...),database:Session=Depends(get_session),buyer=Depends(get_current_buyer)):
    try:
        total_cost=0
        total=0
        parts=[]
        parts_infos=[]

        store=database.query(Store).filter(Store.id==store_id).first()
        for id,q in zip(parts_ids,quantities):
            if q>0:
                p=database.query(Part).filter(Part.id==id).first()
                parts.append(p)
                total+=p.selling_price*q
                total_cost+=p.cost_price*q
                p.quantity-=q
                parts_infos.append(
                    {"name":p.name,"reference":p.reference,"selling_price":p.brand,
                     "store":p.store.name}
                )
       
        new_purchase=Purchase(
            date=datetime.today().strftime("%Y-%m-%d"),
            parts=parts_infos,
            buyer_id=buyer.id,
            store_id=store.id, 
            total=total, 
        )
        database.add(new_purchase)
        new_sale=Sale(
            date=datetime.today().strftime("%Y-%m-%d"),
            buyer_id=buyer.id,
            seller_id=store.seller_id,
            parts=parts_infos,
            cost=total_cost,
            profit=total-total_cost,
            total=total,
            store_id=store.id

        )
        database.add(new_sale)
        database.commit()
        return templates.TemplateResponse(
            name="PurchasesTemplate.html",
            request=request,
            context={
                "purchases":buyer.purchases,
                "parts":store.parts,
                "store":store,
            }
        )


    except Exception as e:
        return templates.TemplateResponse(
            name="StoreDetailsTemplate.html",
            request=request,
            context={
                "error_message":f"Error occured {e}",
                "store":store,
                "parts":store.parts
                
            }
        )

@buyer_router.get("/logout")
def logout(request:Request,buyer=Depends(get_current_buyer)):
    return templates.TemplateResponse(
        name="LoginTemplate.html",
        request=request
    )
