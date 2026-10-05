from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from Database.Bridge import get_session
from Database.models import Buyer,Supplier,Store,Sale,Stock,SupplyRequest,Part
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi import Form
import os
from fastapi import UploadFile,File
from Server.server_utils import get_current_seller
from fastapi.exceptions import HTTPException
from datetime import datetime
from Server.server_utils import create_token,verifiy_password,hash_password
templates=Jinja2Templates("../front-end/seller")
seller_router=APIRouter(prefix="/seller",tags=["seller"])


##############################################       templates     ######################################################################

@seller_router.get("/login")
def login_template(request:Request):
    try:
        return templates.TemplateResponse(
            request=request,
            name="LoginTemplate.html"
        )

    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)


@seller_router.get("/register")
def register_template(request:Request):
    try:
        return  templates.TemplateResponse(
            request=request,
            name="RegisterTemplate.html"
        )

    except Exception as e:
        raise HTTPException(detail=f"server errror: {e}",status_code=400)


@seller_router.get("/dashboard")
def dashboard(request:Request,seller=Depends(get_current_seller)):
    try: 
        return templates.TemplateResponse(
            request=request,
            name="DashboardTemplate.html",
            context={
                "seller":seller,
                "len_stores":len(seller.stores),
                "len_requests":len(seller.requests)

            }
        )

    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Server Error: {e}")


@seller_router.get("/stores")
def stores(request:Request,seller=Depends(get_current_seller)):
    try:
        
        return templates.TemplateResponse(
            name="StoresTemplate.html",
            request=request,
            context={
                "stores":seller.stores
            }
            
        )

    except Exception as e:
        raise HTTPException(detail=f"Server Error : {e}",status_code=400)






@seller_router.get("/suppliers")
def get_suppliers(request:Request,seller=Depends(get_current_seller),database:Session=Depends(get_session)):
    try:
        suppliers=database.query(Supplier).all()
        print(suppliers)

        return templates.TemplateResponse(
            request=request,
            name="SuppliersTemplate.html",
            context={
                 "suppliers":suppliers
            }
        )


    except Exception as e:
        raise HTTPException(detail=f"Server Error : {e}",status_code=400)


@seller_router.get("/supplier_stocks")
def supplier_details(request:Request,supplier_id:int,seller=Depends(get_current_seller),database:Session=Depends(get_session)):
    try:
        supplier=database.query(Supplier).filter(Supplier.id==supplier_id).first()
        return templates.TemplateResponse(
            request=request,
            name="SupplierStocksTemplate.html",
            context={
                "supplier":supplier,
                "stocks":supplier.stocks
            }
        )

    except Exception as e:
        raise HTTPException(detail=f"Server Error {e}",status_code=400)




@seller_router.get("/store_details")
def store_details(request:Request,store_id:int,seller=Depends(get_current_seller),database:Session=Depends(get_session)):
    try:
        store=database.query(Store).filter(Store.id==store_id).first()
        print(store)
        return templates.TemplateResponse(
            request=request,
            name="StoreDetailsTemplate.html",
            context={
                "sales":store.sales,
                "store":store,
                "parts":store.parts
            }
        )

    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)






@seller_router.get("/requests")
def supply_requests(request:Request,seller=Depends(get_current_seller),database:Session=Depends(get_session)):
    try:
        supplyrequests=seller.requests
        return templates.TemplateResponse(
            name="SupplyRequestsTemplate.html",
            request=request,
            context={
                "requests":supplyrequests,
                "stores":seller.stores
            }
        )


    except Exception  as e:
        raise HTTPException(detail=F"Server Error :{e}",status_code=400)




@seller_router.get("/stores")
def stores_template(request:Request,seller=Depends(get_current_seller)):
    try:
        return templates.TemplateResponse(
            name="StoresTemplate.html",
            request=request,
            context={
                "stores":seller.stores
            }
        )


    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)



@seller_router.get("/store_sales")
def sales_template(request:Request,store_id:int,seller=Depends(get_current_seller),database:Session=Depends(get_session)):
    try:
        store=database.query(Store).filter(Store.id==store_id).first()
        
        return templates.TemplateResponse(
            name="SalesTemplate.html",
            request=request,
            context={
                "sales":seller.stores,
                "store":store
            }
        )


    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)





@seller_router.get("/add_store")
def add_store_template(request:Request,seller=Depends(get_current_seller)):
    try:
        return templates.TemplateResponse(
            name="AddStoretemplate.html",
            request=request,
            context={
                "stores":seller.stores
            }
        )


    except Exception as e:
        raise HTTPException(detail=f"Server Error: {e}",status_code=400)



from Database.models import Seller

@seller_router.post("/register")
def register(request:Request,first_name=Form(...),last_name=Form(...),password=Form(...),
             email=Form(...),phone_number=Form(...),database:Session=Depends(get_session)
             ):
    try:
        new_seller=Seller(first_name=first_name,last_name=last_name,email=email,password=hash_password(password),phone_number=phone_number)
        database.add(new_seller)
        database.commit()
        return templates.TemplateResponse(
            request=request,
            name="LoginTemplate.html"
        )

    except Exception as e:
        return templates.TemplateResponse(
            name="RegisterTemlate.html",
            request=request,
            context={
            "error_message":f"error message : {e}"}
        )





@seller_router.post("/login")
def login(request:Request,email=Form(...),password=Form(),database:Session=Depends(get_session)):
    try:
        seller=database.query(Seller).filter(Seller.email==email).first()
        if seller:
            seller=database.query(Seller).filter(Seller.email==email).first()
            if verifiy_password(password,seller.password):
                token=create_token({"id":seller.id,"email":seller.email})
                reponse=RedirectResponse(
                    url="/seller/dashboard",
                    status_code=303
                )
                reponse.set_cookie(
                    key="access_token",
                    value=token
                )
                return reponse
            else:
                return templates.TemplateResponse(
                    name="LoginTemplate.html",
                    request=request,
                    context={"message":"invalid email"}
                )
            
        else:
            return templates.TemplateResponse(
                name="LoginTemplate.html",
                request=request,
                context={
                    "message":"invalid email"
                }
            )
        
        

    except Exception as e:
        return templates.TemplateResponse(
            name="LoginTemplate.html",
            request=request,
            context={
                "error_message":f"Error message : {e}"
            }

        )


@seller_router.post("/create_store")
def create_store(request:Request,brand_group=Form(...),name=Form(...),adress=Form(...),phone_number=Form(...),seller=Depends(get_current_seller),database:Session=Depends(get_session)):
    try:
        print("ROUTE CALLED")
        new_store=Store(
            name=name,brand_group=brand_group,adress=adress,phone_number=phone_number,seller_id=seller.id
        )
        database.add(new_store)
        database.commit()

        return templates.TemplateResponse(
            request=request,
            name="StoresTemplate.html",
            context={
                "stores":seller.stores
            }
        )


    except Exception as e:
        database.rollback()
        return templates.TemplateResponse(
            request=request,
            name="AddStoretemplate.html",
            context={
                "message_error":f"Error message: {repr(e)}"
            }
            
        )




@seller_router.post("/add_request")
def add_request(request:Request,stock_id:int,quantity:int=Form(...),
                database:Session=Depends(get_session),seller=Depends(get_current_seller)):
    try:
        
        request_informations=[]
        stock=database.query(Stock).filter(Stock.id==stock_id).first() 
        supplier=database.query(Supplier).filter(Supplier.id==stock_id).first()
        request_informations.append(
                    {"stock_id":stock.id,"stock_name":stock.part_name,"quantity":quantity,"cost":stock.quantity*quantity,"stock_brand":stock.brand,"stock_refeence":stock.reference}
                )

                                
        new_request=SupplyRequest(
            date=datetime.today().strftime("%Y-%m-%d"),
            status="pending",
            informations=request_informations,
            supplier_id=stock.supplier_id,
            seller_id=seller.id,
            id_stock=stock.id,
        )
        database.add(new_request)
        database.commit()
        return templates.TemplateResponse(
            name="SupplyRequestsTemplate.html",
            request=request,
            context={"message":"request added succesfully ",
                     "requests":seller.requests
                     }
        )
                


    except Exception as e:
        return templates.TemplateResponse(
                    name="SupplierStocksTemplate.html",
                    request=request,
                    context={"error_message":f"Error {repr(e)} occured ",
                             "stocks":supplier.stocks}
                )



@seller_router.post("/complete_request")
def complete_request(request:Request,request_id:int,store_id:int=Form(...),database:Session=Depends(get_session),
                     seller=Depends(get_current_seller)):
    try:
        target_request=database.query(SupplyRequest).filter(SupplyRequest.id==request_id).first()
        target_stock=database.query(Stock).filter(Stock.id==target_request.id_stock).first()
        target_request.status="completed"
        for info in target_request.informations:
            new_part=Part(
                name=info["stock_name"],
                brand=info["stock_brand"],
                reference=info["stock_brand"],
                quantity=info["quantity"],
                cost_price=info["cost"],
                store_id=store_id,
            )
        database.add(new_part)
        target_stock.quantity-=new_part.quantity
        database.commit()
        store=database.query(Store).filter(Store.id==store_id).first()
        return templates.TemplateResponse(
                name="StoreDetailsTemplate.html",
                request=request,
                context={
                    "store":store,
                    "parts":store.parts,
                    "sales":store.sales
                }
            )


    except Exception as e:
        return templates.TemplateResponse(
            name="SupplyRequestsTemplate.html",
            request=request,
            context={
                "error_message":f"Error message {e}"
            }
        )



@seller_router.post("/update_part")
def update_part(request:Request,part_id:int,selling_price=Form(...),compatible_vehicles=Form(...),seller=Depends(get_current_seller),database:Session=Depends(get_session)):
    try:
        part=database.query(Part).filter(Part.id==part_id).first()
        part.selling_price=selling_price
        part.compatible_vehicles=compatible_vehicles
        database.commit()
        return templates.TemplateResponse(
                        name="StoreDetailsTemplate.html",
                        request=request,
                        context={
                            "message":"Part updated succesfully",
                            "store":part.store,
                            "parts":part.store.parts,
                            "sales":part.store.sales
                        }
                    )

    except Exception as e:
        return templates.TemplateResponse(
                                name="StoreDetailsTemplate.html",
                                request=request,
                                context={
                                    "message":f"Error {repr(e)} occured ",
                                    "store":part.store,
                                    "parts":part.store.parts,
                                    "sales":part.store.sales
                                }
                            )



@seller_router.post("/add_brand_image")
async def brand_image(request:Request,store_id:int,image_file:UploadFile=File(),database:Session=Depends(get_session),seller=Depends(get_current_seller)):
    try:
        os.makedirs(f"./images/store-{store_id}",exist_ok=True)
        store=database.query(Store).filter(Store.id==store_id).first()
        data= await image_file.read()
        
        with open(f"./images/store-{store_id}/brand_image.png","wb") as target_image:
            target_image.write(data)
        store.brand_image_path=f"./images/store-{store_id}/brand_image.png"
        database.commit()
        return templates.TemplateResponse(
            request=request,
                        name="StoreDetailsTemplate.html",
                        context={
                            "sales":store.sales,
                            "store":store,
                            "parts":store.parts,
                            "messsage":"Brand Image added succesfully"
                        }

        )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="StoreDetailsTemplate.html",
            context={
                "error_message":f"Error {repr(e)} occured",
                "sales":store.sales,
                "store":store,
                "parts":store.parts
            }
                
            
        )



@seller_router.post("/add_part_image")
async def part_image(request:Request,store_id:int,part_id:int,image_file:UploadFile=File(),database:Session=Depends(get_session),seller=Depends(get_current_seller)):
    try:
        os.makedirs(f"./images/store-{store_id}/parts/",exist_ok=True)
        store=database.query(Store).filter(Store.id==store_id).first()
        part=database.query(Part).filter(Part.id==part_id).first()
        image_content= await image_file.read()
        with open(f"./images/store-{store_id}/parts/part-{part_id}.png","wb") as file:
            file.write(image_content)
        part.image_path=f"./images/store-{store_id}/parts/part-{part_id}.png"
        database.commit()
        return templates.TemplateResponse(
                    request=request,
                    name="StoreDetailsTemplate.html",
                                context={
                                    "sales":store.sales,
                                    "store":store,
                                    "parts":store.parts,
                                    "messsage":"Image part added succesfully"
                                }
        
        )




    except Exception as e:
        return templates.TemplateResponse(
            name="StoreDetailsTemplate.html",
            request=request,
            context={
                            "error_message":f"Error {repr(e)} occured",
                            "sales":store.sales,
                            "store":store,
                            "parts":store.parts
                        }
        )


@seller_router.post("/delete_part")
def delete_part(request:Request,part_id:int,seller=Depends(get_current_seller),database:Session=Depends(get_session)):
    try:
 
        part=database.query(Part).filter(Part.id==part_id).first()
        store=part.store
        database.delete(part)
        database.commit()
        return templates.TemplateResponse(
                        name="StoreDetailsTemplate.html",
                        request=request,
                        context={
                            "message":"Part deleted succesfully",
                            "store":store,
                            "parts":store.parts,
                            "sales":store.sales
                        }
                    )

    except Exception as e:
        return templates.TemplateResponse(
                                name="StoreDetailsTemplate.html",
                                request=request,
                                context={
                                    "message":f"Error {repr(e)} occured ",
                                    "store":store,
                                    "parts":store.parts,
                                    "sales":store.sales,
                                }
                            )

@seller_router.get("/logout")
def logout(request:Request,seller=Depends(get_current_seller)):
    return templates.TemplateResponse(
        name="LoginTemplate.html",
        request=request
    )