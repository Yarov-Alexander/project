from fastapi import FastAPI, HTTPException, status


app = FastAPI()

@app.get("/lop/{lop_id}", status_code=200)
def check(lop_id: int):
    if lop_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid lop id")
    return {"Message": "Hello World!"}