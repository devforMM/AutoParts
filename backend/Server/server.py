from fastapi import FastAPI,Request
from routes.buyer_routes import buyer_router
from routes.seller_routes import seller_router
from routes.supplier_routes import supplier_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

templates=Jinja2Templates("../front-end/buyer")

app=FastAPI()

@app.exception_handler(404)
async def not_found(request:Request,exc):
    return templates.TemplateResponse(
        request=request,
        name="404.html",
        status_code=404
    )

@app.exception_handler(400)
async def inalid_token(request:Request,exc):
    return templates.TemplateResponse(
        request=request,
        name="401.html",
        status_code=401,
    )



app.mount("/styles",StaticFiles(directory="./styles"),name="styles")
app.mount("/images",StaticFiles(directory="./images"),name="images")
app.include_router(seller_router)
app.include_router(buyer_router)
app.include_router(supplier_router)

