from pytest_fixtures import itnitialize_client,create_seller,create_store,get_seller,create_supplier,create_stock
from delete_functions import delete_seller,delete_store,delete_request,delete_part

def test_login_template(itnitialize_client):
    reponse=itnitialize_client.get("/seller/login")
    assert reponse.status_code==200
    assert """""" in reponse.text


def test_register_template(itnitialize_client):
    reponse=itnitialize_client.get("/seller/register")
    assert reponse.status_code==200


def test_dashboard_template(initialize_client):
    reponse=initialize_client.get("/seller/dashboard")
    assert  reponse.status_code==200
    
def test_stores_template(initialize_client,get_seller):
   reponse=initialize_client.get("/seller/stores")
   assert reponse.status_code==200


def test_suppliers_template(initialize_client,get_seller):
    reponse=initialize_client.get("/seller/suppliers")
    assert reponse.status_code==200
    

def test_supplier_details_template(initialize_client,get_seller,create_supplier):
    reponse=initialize_client.get("/seller/supplier_stocks",
                                  params={
                                      "supplier_id":create_supplier.id
                                  })
    assert reponse.status_code==200
    

def test_store_details_template(initialize_client,get_seller,create_store):
    reponse=initialize_client.get("/seller/store_details",
                                  params={
                                      "store_id":create_store.id
                                  })
    assert reponse.status==200

def test_requests_template(initialize_client,get_seller):
    reponse=initialize_client.get("/seller/requests")
    assert reponse.status_code==200

def test_stores_template(initialize_cllient,get_seller):
    reponse=initialize_cllient.get("/seller/stores")
    assert reponse.status_code==200
    

def test_stores_sales_template(initialize_client,get_seller,create_store):
    reponse=initialize_client.get("/seller/store_sales",
                                  params={
                                      "store_id":create_store.id
                                  })
    assert reponse.status_code==200
    


def test_add_store_template(initialize_client):
    reponse=initialize_client.get("/seller/add_store")
    assert reponse.status_code==200
    

def test_regsiter(initialize_client):
    reponse=initialize_client.get("/seller/register",
                                  data={
                                      "first_name":"lionel",
                                      "last_name":"messi",
                                      "email":"messi@gmail.com",
                                      "password":"qwerty",
                                      "phone_number":"10"
                                  },
                                  redirect_reponse=False)
    assert reponse.status_code==303
    assert reponse.headers["location"]=="/seller/login"
    delete_seller("messi@gmail.com")
    


def test_login(initialize_client,create_seller):
    
    reponse=initialize_client.get("/seller/login",
                                  data={
                                      "email":create_seller.email,
                                      "password":create_seller.password
                                  })
    assert reponse.status_code==303
    assert reponse.headers["location"]=="/seller/dashboard"


def test_create_store(initialize_client,get_seller):
    reponse=initialize_client.post("/seller/create_store",
                                   data={
                                       "brand_group":"volksawgen",
                                       "name":"vw_store",
                                       "adress":"madrid",
                                       "phone_number":"100",
                                   })
    assert reponse.status_code==200
    delete_store("madrid")
    

def test_add_request(initialize_client,get_seller,create_stock):
    reponse=initialize_client.post("/seller/add_request",
                                   data={
                                       "quantity":10
                                   },
                                   params={
                                       "stock_id":create_stock.id
                                   })
    assert reponse.status_code==200
    delete_request(create_stock.id)


def complete_request(initialize_client,get_seller,create_request,create_store):
    store=create_store
    request=create_request
    reponse= initialize_client.post("/seller/complete_request",
                                    data={
                                        "request_id":request.id,
                                        "store_id":store.id  
                                    })
    assert reponse.status_code==200
    delete_request(request.id)
    delete_store(store.adress)
    

def update_part(initialize_client,get_seller,create_part):
    part=create_part
    reponse=initialize_client.post("/seller/delete_part",
                                   params={
                                       "part_id":part.id
                                   })
    assert reponse.status_code==200
    delete_part(part.reference)
    


 
    
    
    
    
     

    