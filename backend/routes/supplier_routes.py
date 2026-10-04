from Database.Bridge import get_session
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter,Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from Server.server_utils import get_current_supplier
from Database.models import SupplyRequest,Stock
from fastapi import Form
import traceback

from Server.server_utils import hash_password,verifiy_password,create_token
templates=Jinja2Templates(directory="../front-end/supplier")
supplier_router=APIRouter(tags=["supplier"],prefix="/supplier")





@supplier_router.get("/login")
def login_template(request:Request):
    try:
        return templates.TemplateResponse(
            name="LoginTemplate.html",
            request=request
        )
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Server Error: {e}")



@supplier_router.get("/register")
def register_template(request:Request):
    try:
        return templates.TemplateResponse(
            request=request,
            name="RegisterTemplate.html"
        )

    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Server Error: {e}")




@supplier_router.get("/dashboard")
def dashboard(request:Request,supplier=Depends(get_current_supplier)):
    try:
        return templates.TemplateResponse(
            name="DashboardTemplate.html",
            request=request,
            context={
                "supplier":supplier,
                "stock_length":len(supplier.stocks),
                "requests_length":len(supplier.requests)
            }
        )


    except Exception as e:
        raise HTTPException(detail=f"Server Error : {e}",status_code=400)



@supplier_router.get("/requests")
def requests_template(request:Request,supplier=Depends(get_current_supplier)):
    try:
        supply_requests=supplier.requests
        return templates.TemplateResponse(
            name="SupplyRequestsTemplate.html",
            request=request,
            context={
                "requests":supply_requests
            }
        )


    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Server Error: {e}")




@supplier_router.get("/stocks")
def stocks_template(request:Request,supplier=Depends(get_current_supplier)):
    try:
        all_stocks=supplier.stocks
        return templates.TemplateResponse(
            request=request,
            name="StocksTemplate.html",
            context={
                "stocks":all_stocks
            }
        )


    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Server  Error: {e}")






@supplier_router.get("/requests")
def get_requests(request:Request,supplier=Depends(get_current_supplier)):
    try:
        supply_requests=supplier.requests
        return templates.TemplateResponse(
            name="SupplyRequestsTemplate.html",
            request=request,
            context={
                "requests":supply_requests
            }

        )


    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)





@supplier_router.get("/add_stock")
def stock_template(request:Request,supplier=Depends(get_current_supplier)):
    try:
        return templates.TemplateResponse(
            name="AddStockTemplate.html",
            request=request,
        )
    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)


######################################################## templates ##############################################

from Database.models import Supplier,Stock,SupplyRequest

@supplier_router.post("/register")
def register(
             request:Request,first_name=Form(...),last_name=Form(...),email=Form(...),password=Form(...),
             database:Session=Depends(get_session)
             ):
    try:
        new_supplier=Supplier(
            first_name=first_name,last_name=last_name,email=email,
            password=hash_password(password)
        )
        database.add(new_supplier)
        database.commit()

        return templates.TemplateResponse(
            name="LoginTemplate.html",
            request=request,
            context={
                "message":"Register_succesfully"
            }
        )

    
    except Exception as e:
        database.rollback()
        traceback.print_exc()
        return templates.TemplateResponse(
            request=request,
            name="RegisterTemplate.html",
            context={
                "error_message":f"Error {e} occured while registration"
            }
        )

@supplier_router.post("/login")
def login(request:Request,email=Form(...),password=Form(...),database:Session=Depends(get_session)):
    try:
        supplier=database.query(Supplier).filter(Supplier.email==email).first()
        if supplier:
            if verifiy_password(password,supplier.password):
                token=create_token({"id":supplier.id,"email":supplier.email})
                reponse=RedirectResponse(
                    url="/supplier/dashboard",
                    status_code=303,  
                )
                reponse.set_cookie(
                    key="access_token",value=token
                )
                return reponse 
            else:
                return templates.TemplateResponse(
                    name="LoginTemplate.html",
                    request=request,
                    context={
                        "message":"Inavalid password"
                    }
                )
                 

        else:
            return templates.TemplateResponse(
                request=request,
                name="LoginTemplate.html",
                context={
                    "messaage":"Invalid Email"
                }
            )
        


    except Exception as e:
        return templates.TemplateResponse(
            name="RegisterTemplate.html",
            request=request,
            context={
                "error_message":f"Error {e} occured while registration"
            }

        )



@supplier_router.post("/new_stock")
def add_stock(request:Request,part_name=Form(...),quantity=Form(...),cost_price=Form(...),
             brand=Form(...),reference=Form(...),database:Session=Depends(get_session),supplier=Depends(get_current_supplier)):
    try:
        new_stock=Stock(
            part_name=part_name,quantity=quantity,cost_price=cost_price,
            brand=brand,reference=reference,supplier_id=supplier.id

        )
        database.add(new_stock)
        database.commit()
        return templates.TemplateResponse(
            request=request,
            name="StocksTemplate.html",
            context={
                "message":"stock added successfully"
            }
        )


    except Exception as e:
        return templates.TemplateResponse(
            name="AddStockTemplate.html",
            request=request,
            context={
                "error_message":f"Error {e} occured "
            }
        )


@supplier_router.post("/validate_request")
def validate_request(id_request:int,supplier=Depends(get_current_supplier),database:Session=Depends(get_session)):
    try:
        target_request=database.query(SupplyRequest).filter(SupplyRequest.id==id_request).first()
        target_request.status="valid"
        database.commit()
        return  {"message":"Request validated successfully"}
    except Exception as e:
        return{
                "message":f"error message {e}"
            }
        


@supplier_router.delete("/delete_request")
def delete_request(id_request:int,supplier=Depends(get_current_supplier),database:Session=Depends(get_session)):
    try:
        supply_request=database.query(SupplyRequest).filter(SupplyRequest.id==id_request).first()
        database.delete(supply_request)
        database.commit()
        return {"message":"Request Deleted successfully"}

    except Exception as e:
           return {
                "message":f"error occured in {e}"
            }
   


@supplier_router.get("/logout")
def logout(request:Request):
    return templates.TemplateResponse(
        name="LoginTemplate.html",
        request=request
    )