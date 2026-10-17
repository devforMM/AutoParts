from Database.Database import test_session_maker
from Database.models import Buyer,Purchase,Sale,Seller,Part,Store,Supplier,Stock,SupplyRequest


def delete_supplier(email):
    test_session=test_session_maker()
    try:
       target_supplier=test_session.query(Supplier).filter(Supplier.email==email).first()
       test_session.query(Stock).filter(Stock.supplier_id==target_supplier.id).delete()
       test_session.query(SupplyRequest).filter(SupplyRequest.supplier_id==target_supplier.id).delete()
       test_session.delete(target_supplier)
       test_session.commit()
    except:
        test_session.rollback()
        test_session.close()

def delete_buyer(email):
    test_session=test_session_maker()
    try:
        target_buyer=test_session.query(Buyer).filter(Buyer.email==email).first()
        test_session.query(Purchase).filter(Purchase.buyer_id==target_buyer.id).delete()
        test_session.query(Sale).filter(Sale.buyer_id==target_buyer.id).delete()
        test_session.delete(target_buyer)
        test_session.commit()
    except:
            test_session.rollback()
            test_session.close()
    

def delete_seller(email):
    test_session=test_session_maker()
    try:
        target_seller=test_session.query(Seller).filter(Seller.email==email).first()
        test_session.query(Sale).filter(Sale.seller_id==target_seller.id).delete()
        test_session.query(Store).filter(Store.seller_id==target_seller.id).delete()
        test_session.delete(target_seller)
        test_session.commit()
    except:
        test_session.rollback()
        test_session.close()
        
    
    


def delete_store(adress):
    test_session=test_session_maker()
    try:
        target_store=test_session.query(Store).filter(Store.adress==adress).first()
        test_session.query(Part).filter(Part.store_id==target_store.id).delete()
        test_session.query(Purchase).filter(Purchase.store_id==target_store.id).delete()
        test_session.query(Sale).filter(Sale.store_id==target_store.id).delete()
        test_session.delete(target_store)
        test_session.commit()
    except:
        test_session.rollback()
        test_session.close()
        
        



def delete_stock(reference):
    test_session=test_session_maker()
    try:
        target_stock=test_session.query(Stock).filter(Stock.reference==reference).first()
        test_session.query(Stock).filter(SupplyRequest.id_stock==target_stock.id).delete()
        test_session.delete(target_stock)
        test_session.commit()
    except:
        test_session.rollback()
        test_session.close()
    

def delete_part(reference):
    test_session=test_session_maker()
    try:
        target_part=test_session.query(Part).filter(Part.reference==reference).first()
        test_session.delete(target_part)
        test_session.commit()
    
    except:
        test_session.close()
        test_session.commit()
        
    
    
def delete_request(stock_id):
    test_session=test_session_maker()
    try:
        target_request=test_session.query(SupplyRequest).filter(SupplyRequest.id==stock_id).delete()
        test_session.delete(target_request)
        test_session.commit()
    except:
        test_session.close()
        test_session.commit()
    

def 



