from fastapi import FastAPI,Response, status
from fastapi.responses import JSONResponse
# from recomm.recomsystem import get_recommendations_new
from recomm import recomsystem as rec
application = FastAPI()
app=application
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}

@app.get("/recommend/{show_name}",status_code=200)
async def read_item(show_name:str,):
    try:
        pdsr=rec.get_recommendations_new(show_name)
    except:
        Response.status_code=status.HTTP_403_FORBIDDEN
        return {"message":"Movie Not Found in Database"}
    lst=list(pdsr.values)
    print(lst)
    return JSONResponse(content=lst,media_type="application/json")