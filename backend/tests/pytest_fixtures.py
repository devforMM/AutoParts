from Server.server import app
import pytest
from fastapi.testclient import TestClient
from Database.Bridge import get_session,test_get_session
from Database.Database import test_session_maker
from Database.models import Buyer,Purchase,Sale,Seller,Part,Store,Supplier,Stock,SupplyRequest
from Server.server_utils import create_token,hash_password
from datetime import datetime
@pytest.fixture
def itnitialize_client():
    app.dependency_overrides[get_session]=test_get_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    


@pytest.fixture
def get_buyer(initialize_client):
    db_session=test_session_maker()
    try:
        new_buyer=Buyer(first_name="lionel",last_name="messi",email="messi@gmail.com",password=hash_password("qwerty"),phone_number="10")
        db_session.add(new_buyer)
        db_session.commit()
        db_session.refresh(new_buyer)
        buyer_id=new_buyer.id
        try:
            token=create_token({"user_id":new_buyer.id,"email":new_buyer.email})
            initialize_client.cookies.set("access_token",token)
            yield new_buyer
            
        finally:
            db_session.rollback()
            db_session.query(Purchase).filter(Purchase.buyer_id==buyer_id).delete()
            db_session.query(Sale).filter(Sale.id==buyer_id).delete()
            db_session.commit()
            
    finally:
        db_session.rollback()
        db_session.close()


@pytest.fixture
def create_buyer(initialize_client):
    db_session=test_session_maker()
    try:
        new_buyer=Buyer(first_name="lionel",last_name="messi",email="messi@gmail.com",password=hash_password("qwerty"),phone_number="10")
        db_session.add(new_buyer)
        db_session.commit()
        db_session.refresh(new_buyer)
        buyer_id=new_buyer.id
        try:
            token=create_token({"user_id":new_buyer.id,"email":new_buyer.email})
            initialize_client.cookies.set("access_token",token)
            yield new_buyer
            
        finally:
            db_session.rollback()
            db_session.query(Purchase).filter(Purchase.buyer_id==buyer_id).delete()
            db_session.query(Sale).filter(Sale.buyer_id==buyer_id).delete()
            db_session.commit()
            
    finally:
        db_session.rollback()
        db_session.close()






@pytest.fixture
def get_seller(initialize_client):
    db_session=test_session_maker()
    try:
        new_selller=Seller(first_name="lionel",last_name="messi",email="messi@gmail.com",password=hash_password("qwerty"),phone_number="10")
        db_session.add(new_selller)
        db_session.commit()
        db_session.refresh(new_selller)
        seller_id=new_selller.id
        try:
            token=create_token({"user_id":new_selller.id,"email":new_selller.email})
            initialize_client.cookies.set("access_token",token)
            yield new_selller
            
        finally:
            db_session.rollback()
            db_session.query(Sale).filter(Sale.seller_id==seller_id).delete()
            db_session.query(Store).filter(Store.seller_id==seller_id).delete()
            db_session.commit()
            
    finally:
        db_session.rollback()
        db_session.close()


@pytest.fixture
def create_seller(initialize_client):
    db_session=test_session_maker()
    try:
        new_selller=Seller(first_name="lionel",last_name="messi",email="messi@gmail.com",password=hash_password("qwerty"),phone_number="10")
        db_session.add(new_selller)
        db_session.commit()
        db_session.refresh(new_selller)
        seller_id=new_selller.id
        try:
            token=create_token({"user_id":new_selller.id,"email":new_selller.email})
            initialize_client.cookies.set("access_token",token)
            yield new_selller
            
        finally:
            db_session.rollback()
            db_session.query(Sale).filter(Sale.seller_id==seller_id).delete()
            db_session.query(Store).filter(Store.seller_id==seller_id).delete()
            db_session.commit()
            
    finally:
        db_session.rollback()
        db_session.close()





@pytest.fixture
def get_supplier(initialize_client):
    db_session=test_session_maker()
    try:
        new_supplier=Supplier(first_name="lionel",last_name="messi",email="messi@gmail.com",password=hash_password("qwerty"),phone_number="10")
        db_session.add(new_supplier)
        db_session.commit()
        db_session.refresh(new_supplier)
        supplier_id=new_supplier.id
        try:
            token=create_token({"user_id":new_supplier.id,"email":new_supplier.email})
            initialize_client.cookies.set("access_token",token)
            yield new_supplier
            
        finally:
            db_session.rollback()
            db_session.query(Stock).filter(Stock.supplier_id==supplier_id).delete()
            db_session.query(SupplyRequest).filter(SupplyRequest.supplier_id==supplier_id).delete()
            db_session.commit()
            
    finally:
        db_session.rollback()
        db_session.close()


@pytest.fixture
def create_supplier(initialize_client):
    db_session=test_session_maker()
    try:
        new_supplier=Supplier(first_name="lionel",last_name="messi",email="messi@gmail.com",password=hash_password("qwerty"),phone_number="10")
        db_session.add(new_supplier)
        db_session.commit()
        db_session.refresh(new_supplier)
        supplier_id=new_supplier.id
        try:
            token=create_token({"user_id":new_supplier.id,"email":new_supplier.email})
            initialize_client.cookies.set("access_token",token)
            yield new_supplier
            
        finally:
            db_session.rollback()
            db_session.query(SupplyRequest).filter(SupplyRequest.supplier==supplier_id).delete()
            db_session.query(Stock).filter(Stock.supplier_id==supplier_id).delete()
            db_session.commit()
            
    finally:
        db_session.rollback()
        db_session.close()
        
        
@pytest.fixture
def create_store(create_seller):
    db_session=test_session_maker()
    try:
            new_store=Store(brand_group="Volkswagen",brand_image_path="path",name="Store",adress="Store Adress",phone_number="10",seller_id=create_seller.id)
            db_session.add(new_store)
            db_session.commit()
            db_session.refresh(new_store)
            store_id=new_store.id
            try:
               
                yield new_store
                
            finally:
                db_session.rollback()
                db_session.query(Part).filter(Part.store_id==new_store).delete()
                db_session.query(Purchase).filter(Purchase.store_id==store_id).delete()
                db_session.query(Sale).filter(Sale.store_id==store_id).delete()
                db_session.commit()
                
    finally:
            db_session.rollback()
            db_session.close()
    

@pytest.fixture
def create_part(create_store):
    db_session=test_session_maker()
    try:
            new_part=Part(name="bougies",brand="Bmw",reference="Ref-100",quantity=10,cost_price=80.0,selling_price=100,compatible_vehicles="vehicles",image_path="path",store_id=create_store.id)
            db_session.add(new_part)
            db_session.commit()
            db_session.refresh(new_part)
            try:
               
                yield new_part
                
            finally:
                db_session.rollback()
                db_session.delete(new_part)
                db_session.commit()
                
    finally:
            db_session.rollback()
            db_session.close()


@pytest.fixture
def create_stock(create_store):
    db_session=test_session_maker()
    try:
            new_stock=Stock(name="bougies",brand="Bmw",reference="Ref-100",quantity=10,cost_price=80.0,selling_price=100,compatible_vehicles="vehicles",image_path="path",store_id=create_store.id)
            db_session.add(new_stock)
            db_session.commit()
            db_session.refresh(new_stock)
            stock_id=new_stock.id
            try:
               
                yield new_stock
                
            finally:
                db_session.rollback()
                db_session.query(SupplyRequest).filter(SupplyRequest.stock_id==stock_id).delete()
                db_session.commit()
                
    finally:
            db_session.rollback()
            db_session.close()
    


@pytest.fixture
def create_request(create_supplier,create_seller,create_stock):
    test_session=test_session_maker()
    try:
        new_request=SupplyRequest(date=datetime.today().strftime(""),status="Penging",informations=[{"informations":"info"}],
                                  supplier_id=create_supplier.id,seller_id=create_seller.id,id_stock=create_stock.id  
                                  )
        test_session.add(new_request)
        test_session.commit()
        test_session.refresh(new_request)
        try:
            yield test_session
        except:
            test_session.rollback()
    
    except:
        test_session.rollback()
        test_session.close()




