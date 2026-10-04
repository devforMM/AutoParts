from sqlalchemy import Column,Integer,Text,ForeignKey,Float,JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from Database.Database import Base,engine



class Buyer(Base):
    __tablename__="buyer"
    id=Column(Integer,primary_key=True,autoincrement=True)
    first_name=Column(Text,nullable=False)
    last_name=Column(Text,nullable=False)
    email=Column(Text,unique=True)
    password=Column(Text,nullable=False)
    adress=Column(Text,nullable=False)
    phone_number=Column(Text,nullable=False)
    purchases=relationship("Purchase",foreign_keys="Purchase.buyer_id",back_populates="buyer")
    



class Purchase(Base):
    __tablename__="purchase"
    id=Column(Integer,primary_key=True)
    date=Column(Text,nullable=False)
    parts=Column(JSON,nullable=False)
    total=Column(Float,nullable=False)
    buyer_id=Column(Integer,ForeignKey("buyer.id"),nullable=False)
    store_id=Column(Integer,ForeignKey("store.id"),nullable=False)
    store=relationship("Store",foreign_keys=store_id,back_populates="purchases")
    buyer=relationship("Buyer",foreign_keys=buyer_id,back_populates="purchases")





class Sale(Base):
    __tablename__="sale"
    id=Column(Integer,primary_key=True)
    date=Column(Text,nullable=False)
    buyer_id=Column(Integer,ForeignKey("buyer.id"))
    seller_id=Column(Integer,ForeignKey("seller.id"))
    parts=Column(JSON,nullable=False)
    cost=Column(Float,nullable=False)
    total=Column(Float,nullable=False)
    profit=Column(Float,nullable=False)
    store_id=Column(Integer,ForeignKey("store.id"),nullable=False)
    store=relationship("Store",back_populates="sales",foreign_keys=store_id)









class Seller(Base):
    __tablename__="seller"
    id=Column(Integer,primary_key=True,autoincrement=True)
    first_name=Column(Text,nullable=False)
    last_name=Column(Text,nullable=False)
    email=Column(Text,unique=True)
    password=Column(Text,nullable=False)
    phone_number=Column(Text,nullable=False)
    requests=relationship("SupplyRequest",foreign_keys="SupplyRequest.seller_id",back_populates="seller")
    stores=relationship("Store",foreign_keys="Store.seller_id",back_populates="seller")

    
    
    

 
    



class Part(Base):
    __tablename__="part"
    id=Column(Integer,primary_key=True,unique=True,autoincrement=True)
    name=Column(Text,nullable=False)
    brand=Column(Text,nullable=False)
    reference=Column(Text,nullable=False)
    quantity=Column(Integer,nullable=False)
    cost_price=Column(Float,nullable=False)
    selling_price=Column(Float,nullable=True)
    compatible_vehicles=Column(Text,nullable=True)
    image_path=Column(Text,nullable=True)
    store_id=Column(Integer,ForeignKey("store.id"),nullable=False)
    store=relationship("Store",foreign_keys=store_id,back_populates="parts")

    
    


    





        
    


class Store(Base):
    __tablename__="store"
    id=Column(Integer,autoincrement=True,primary_key=True)
    brand_group=Column(Text,nullable=False)
    name=Column(Text,nullable=False,unique=True)
    adress=Column(Text,nullable=False)
    phone_number=Column(Text,nullable=False)
    seller_id=Column(Integer,ForeignKey("seller.id"),nullable=False)
    seller=relationship(
        "Seller",back_populates="stores",foreign_keys=seller_id
    )
    parts=relationship(
        "Part",back_populates="store",foreign_keys="Part.store_id")
    purchases=relationship(
        "Purchase",back_populates="store",foreign_keys="Purchase.store_id")
    sales=relationship(
        "Sale",back_populates="store",foreign_keys="Sale.store_id")






class Supplier(Base):
    __tablename__="supplier"
    id=Column(Integer,primary_key=True,autoincrement=True)
    first_name=Column(Text,nullable=False)
    last_name=Column(Text,nullable=False)
    email=Column(Text,nullable=False)
    password=Column(Text,nullable=False)
    stocks=relationship("Stock",foreign_keys="Stock.supplier_id",back_populates="supplier")
    requests=relationship("SupplyRequest",foreign_keys="SupplyRequest.supplier_id",back_populates="supplier")




class Stock(Base):
    __tablename__="stock"
    id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    part_name=Column(Text,nullable=False)
    quantity=Column(Integer,nullable=False)
    cost_price=Column(Float,nullable=False)
    brand=Column(Text,nullable=False)
    reference=Column(Text,nullable=False)
    supplier_id=Column(Integer,ForeignKey("supplier.id"),nullable=False)
    supplier=relationship("Supplier",foreign_keys=supplier_id,back_populates="stocks")
    requests=relationship("SupplyRequest",foreign_keys="SupplyRequest.id_stock",back_populates="stock")





class SupplyRequest(Base):
    __tablename__="supplyrequest"
    id=Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    date=Column(Text,nullable=False)
    status=Column(Text,nullable=False)
    informations=Column(JSON,nullable=False)
    supplier_id=Column(Integer,ForeignKey("supplier.id"),nullable=False)
    seller_id=Column(Integer,ForeignKey("seller.id"),nullable=False)
    supplier=relationship("Supplier",foreign_keys=supplier_id,back_populates="requests")
    seller=relationship("Seller",foreign_keys=seller_id,back_populates="requests")
    id_stock=Column(Integer,ForeignKey("stock.id"),nullable=True)
    stock=relationship("Stock",foreign_keys=id_stock,back_populates="requests")



















Base.metadata.create_all(bind=engine)


