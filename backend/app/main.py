from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from app.cores.database import Base,engine,get_db
from app.api import auth
from app.api import category



Base.metadata.create_all(bind=engine)

app = FastAPI(title="freshmart")

app.include_router(auth.router)
app.include_router(category.router)


@app.get('/')
def root():
    return {'msg':'freshmart is live'}