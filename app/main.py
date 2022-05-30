from fastapi import Body, Depends, FastAPI,Response,status,HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from  . import models,schemas
from .database import engine,get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)



while True:
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='na1',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        print('Connecting to database failed')
        print('Error :',error)
        

app=FastAPI()


@app.get('/')
def myapi():
    return 'hi nirvikaar how are you'

    
@app.get('/posts',response_model=list[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
 
    posts=db.query(models.Post).all()
    return posts

@app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(data:schemas.PostCreate,db:Session=Depends(get_db)):
   
    new_post=models.Post(**data.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id:int,db:Session=Depends(get_db)):
   
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id : {id} was  not found')
        
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id)

   
        
    if post.first()==None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'post with id : {id} was  not found') 
        
    else:
        post.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int,data:schemas.PostCreate,db:Session=Depends(get_db)):
  
    post=db.query(models.Post).filter(models.Post.id==id)
    if  post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'post with id : {id} was  not found')
    else:
        post.update(data.dict(),synchronize_session=False) 
        db.commit()
    return post.first()
    


