from fastapi import FastAPI
from routes.buyer_routes import buyer_router
from routes.seller_routes import seller_router
from routes.supplier_routes import supplier_router
app=FastAPI()
app.include_router(seller_router)
app.include_router(buyer_router)
app.include_router(supplier_router)

