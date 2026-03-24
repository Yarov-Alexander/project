from fastapi import FastAPI, HTTPException, status
from .modules.categories.routers import router as categories_router
from app.modules.users.routers import router as users_router
from app.modules.CartItem.routers import router as cart_router
from app.modules.reviews.routers import router as reviews_router
from app.modules.products.routers import router as products_router

app = FastAPI()
app.include_router(categories_router)
app.include_router(users_router)
app.include_router(cart_router)
app.include_router(reviews_router)
app.include_router(products_router)
@app.get("/", status_code=200)
def check(lop: str):
    if not lop.isalpha():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid lop ")
    return {"Message": f"Hello!"}