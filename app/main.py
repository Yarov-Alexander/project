from fastapi import FastAPI, HTTPException, status
from .modules.categories.routers import router as categories_router

app = FastAPI()
app.include_router(categories_router)
@app.get("/lop/{lop_id}", status_code=200)
def check(lop_id: int):
    if lop_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid lop id")
    return {"Message": "Hello World!"}