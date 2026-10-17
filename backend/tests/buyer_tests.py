from  pytest_fixtures import initialize_clinet,get_supplier


def test_login_template(iniialize_client):
    
    reponse= iniialize_client.get("/buyer/login")
    assert reponse.status_code==200
    assert 'name="email"' in reponse.text
    
    

def test_register_template(initialize_client):
    reponse= initialize_client.get("/user/register")
    assert reponse.status_code==200
    assert 'name="email"' in reponse.text
    print(reponse.text)
    
    
    

def test_dashboard_template(initialize_client, get_user):


    response = initialize_client.get("/user/dashboard")
    
    assert response.status_code == 200
    assert get_user.last_name in response.text.lower()
    assert get_user.first_name in response.text
    print(response.text)
    


    


def test_add_aplication_template(initialize_client,get_user):

    reponse=initialize_client.get("/user/add_application")
    
    assert reponse.status_code==200
    assert "Add New Job application" in reponse.text

def test_get_applications_template(initialize_client,get_user):

    reponse=initialize_client.get("/user/get_applications")
    print(reponse.text)
    assert reponse.status_code==200
    assert "All your jobs Applications" in reponse.text    
    
    
    

    

def test_register(initialize_client):
    reponse=initialize_client.post("/user/register",
                                   data={
                                       "first_name":"neymar",
                                       "last_name":"junior",
                                       "email":"neymar@gmail.com",
                                       "password":"qwerty",
                                       "phone_number":"11"
                                   },follow_redirects=False)
    assert reponse.status_code==303
    assert reponse.headers["location"]=="/user/login"



def test_login(initialize_client,create_user):
    reponse=initialize_client.post("/user/login",
                                   data={
                                       "email":create_user.email,
                                       "password":"qwerty"  
                                   },follow_redirects=False)
    assert reponse.status_code==303
    assert reponse.headers["location"]=="/user/dashboard"
    



    
    
def test_add_application(initialize_client,monkeypatch,tmp_path,get_user):
    
    monkeypatch.setattr(services,"users_dir",str(tmp_path/"users_files"))
    
    reponse=initialize_client.post("/user/add_application",
                                   data={
                                       "job_position":"Ingenieur",
                                       "company":"Amazon",
                                       "job_type":"Remote",
                                       "job_location":"USA",
                                       "website":"Amazon.com"
                                       
                                   },
                                   files={
                                       "cv_file":(
                                           "cv.pdf",
                                           b'%PDF-1.4 fake pdf content',
                                           "application/pdf"
                                       )
                                   })
    print(reponse.text)
    assert reponse.status_code==200
    file_path = (
        tmp_path / "users_files" / f"user-{get_user.id}"
        / "Ingenieur" / "Amazon-cv.pdf"
    )
    
    assert file_path.exists()
    assert file_path.read_bytes()==b"%PDF-1.4 fake pdf content"
    
    
    
    
    
 
    
    
    
def test_update_application(initialize_client,create_application,get_user):
    reponse=initialize_client.post("/user/update_status",
                                   params={"id_application": create_application.id},
                                   data={"status": "Accepted"},
                                   follow_redirects=False,)
    print(reponse.text)
    assert reponse.status_code==303
    
    assert reponse.headers["location"]=="/user/get_applications"
    
    


def test_download(initialize_client,create_application,get_user):
    reponse=initialize_client.get("/user/download_cv",
                                  params={
                                      "application_id":create_application.id
                                  })
    print(reponse.text)
    assert reponse.status_code==200
    assert reponse.headers["content-type"]=="application/pdf"
    assert reponse.content == b"%PDF-1.4 fake pdf content"
    assert "attachment" in reponse.headers["content-disposition"]
    


def test_delete_application(initialize_client,create_application,get_user):
    reponse=initialize_client.post("/user/delete_application",
                                  params={"application_id":create_application.id})
    
    print(reponse.text)
    assert reponse.status_code==200
    assert "All your jobs Applications" in reponse.text
    

    

def test_logout(initialize_client,get_user):
    reponse=initialize_client.get("/user/logout",follow_redirects=False)
    assert reponse.status_code==303
    assert reponse.headers["location"]=="/user/login"
    
  


  
  
