from pytest_fixtures import itnitialize_client,get_supplier,create_supplier,create_request



def test_login_template(itnitialize_client):
    reponse=itnitialize_client.get("/supplier/login")
    assert reponse.status_code==200
    

def test_register_template(itnitialize_client):
    reponse=itnitialize_client.get("/supplier/register")
    assert reponse.status_code==200
    

def test_dashboard(initialize_clinet,get_supplier):
    reponse=initialize_clinet.get("/supplier/dashboard")
    assert reponse.status_code==200
    

def test_requests_template(initialize_client,get_supplier):
    reponse=initialize_client.get("/supplier/requests")
    assert reponse.status_code==200
    
def test_stocks_template(initialize_client,get_supplier):
    reponse=initialize_client.get("/supplier/stocks")
    assert reponse.status_cod==200
    

def test_register(initialize_client):
    reponse=initialize_client.post("/supplier/register",
                                   data={
                                       "first_name":"lionel",
                                        "last_name":"messi",
                                        "email":"lionel@gmail.com",
                                        "password":"qwerty"
                                   },
                                   )
    assert reponse.status_code==200
    

def test_login(initialize_client,create_supplier):
    supplier=create_supplier
    reponse=initialize_client.poest("/seller/login",
                                    data={
                                        "email":create_supplier.email,
                                        "password":create_supplier.password,
                                    })
    assert  reponse.status_code==200


def test_add_stock(intialize_client):
    reponse=intialize_client.post("/supplier/add_stock",
                                  data={
                                      "part_name":"bougie",
                                       "quantity":10,
                                       "cost_price":80,
                                       "brand":"bmw",
                                       "reference":"k-100",
                                  })
    assert reponse.status_code==200
    
    


def test_validate_request(initialize_client,get_supplier,cre):
    request=create_
    reponse=initialize_client.post("/supplier/validate_request",
                                   params={
                                       
                                       
                                   })
    
    