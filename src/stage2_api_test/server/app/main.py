#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time        : 2026-05-18 09:48
# @Author      : Felix Cui
# @Email       : cuihediyzu@gmail.com
# @File        : main.py
# @PythonEnv   : Python 3.12 (pythonautotest-py312)
# @IDE         : PyCharm
# @Description : docker app
#
# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from typing import List, Optional
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
#
# # JWT配置
# SECRET_KEY = "your-secret-key-keep-it-safe"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# # 数据库模拟（SQLite文件，数据永久保存）
# from sqlalchemy import create_engine, Column, Integer, String, Boolean
# from sqlalchemy.orm import declarative_base, sessionmaker
#
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
#
# # 用户模型
# class DBUser(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)
#
# Base.metadata.create_all(bind=engine)
#
# # Pydantic模型
# class UserBase(BaseModel):
#     username: str
#     email: Optional[str] = None
#
# class UserCreate(UserBase):
#     password: str
#
# class User(BaseModel):
#     id: int
#     username: str
#     email: Optional[str] = None
#     is_active: bool
#
#     class Config:
#         from_attributes = True
#
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#
# class TokenData(BaseModel):
#     username: Optional[str] = None
#
# # 工具函数
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# def get_password_hash(password):
#     return password
#
# def verify_password(plain_password, hashed_password):
#     return plain_password == hashed_password
#
# def get_user(db, username: str):
#     return db.query(DBUser).filter(DBUser.username == username).first()
#
# def create_user(db, user: UserCreate):
#     db_user = DBUser(
#         username=user.username,
#         email=user.email,
#         hashed_password=get_password_hash(user.password)
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
# def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
# # FastAPI应用
# app = FastAPI(title="接口测试实战服务")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
#
# async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="无法验证凭据",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username=username)
#     if user is None:
#         raise credentials_exception
#     return user
#
# # ---------- 接口 ----------
#
# @app.get("/")
# def root():
#     return {"msg": "hello fastapi"}
#
#
# @app.post("/register", response_model=User, tags=["用户管理"])
# def register(user: UserCreate, db=Depends(get_db)):
#     db_user = get_user(db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="用户名已注册")
#     return create_user(db=db, user=user)
#
# @app.post("/login", response_model=Token, tags=["用户管理"])
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
#     user = get_user(db, username=form_data.username)
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="用户名或密码错误",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
#
# @app.get("/users/me", response_model=User, tags=["用户管理"])
# def read_users_me(current_user: DBUser = Depends(get_current_user)):
#     return current_user
#
# @app.get("/users", response_model=List[User], tags=["用户管理"])
# def read_users(skip: int = 0, limit: int = 100, db=Depends(get_db)):
#     return db.query(DBUser).offset(skip).limit(limit).all()
#
# @app.get("/users/{user_id}", response_model=User, tags=["用户管理"])
# def read_user(user_id: int, db=Depends(get_db)):
#     db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="用户不存在")
#     return db_user
#
# @app.put("/users/{user_id}", response_model=User, tags=["用户管理"])
# def update_user(
#     user_id: int,
#     user: UserCreate,
#     db=Depends(get_db),
#     current_user: DBUser = Depends(get_current_user)  # ✅ 需要鉴权
# ):
#     db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="用户不存在")
#     db_user.username = user.username
#     db_user.email = user.email
#     db_user.hashed_password = get_password_hash(user.password)
#     db.commit()
#     db.refresh(db_user)
#     return db_user
#
# @app.delete("/users/{user_id}", tags=["用户管理"])
# def delete_user(
#     user_id: int,
#     db=Depends(get_db),
#     current_user: DBUser = Depends(get_current_user)  # ✅ 需要鉴权
# ):
#     db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="用户不存在")
#     db.delete(db_user)
#     db.commit()
#     return {"message": "用户删除成功"}


# 增加用户管理、商品管理、订单管理 三组接口  用于电商接口测试实战服务


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# JWT配置
SECRET_KEY = "your-secret-key-keep-it-safe"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 数据库配置
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ---------- 用户模型 ----------
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

# ---------- 商品模型 ----------
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

# ---------- 订单模型 ----------
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="pending")

# 创建所有表
Base.metadata.create_all(bind=engine)

# ---------- Pydantic 模型 ----------
class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    is_active: bool
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class ProductOut(ProductCreate):
    id: int
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    product_id: int
    quantity: int

class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# ---------- 工具函数 ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return password

def verify_password(plain_password, hashed_password):
    return plain_password == hashed_password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------- FastAPI 应用 ----------
app = FastAPI(title="电商接口测试实战服务")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(DBUser).filter(DBUser.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# ==================== 用户接口 ====================
@app.get("/")
def root():
    return {"msg": "hello fastapi"}

@app.post("/register", response_model=UserOut, tags=["用户管理"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已注册")
    new_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login", response_model=Token, tags=["用户管理"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# ==================== 商品接口 ====================
@app.post("/products", response_model=ProductOut, tags=["商品管理"])
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products", response_model=List[ProductOut], tags=["商品管理"])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Product).offset(skip).limit(limit).all()

@app.get("/products/{product_id}", response_model=ProductOut, tags=["商品管理"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    return product

# ==================== 订单接口 ====================
@app.post("/orders", response_model=OrderOut, tags=["订单管理"])
def create_order(order: OrderCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    if product.stock < order.quantity:
        raise HTTPException(status_code=400, detail="库存不足")
    total_price = product.price * order.quantity
    db_order = Order(
        user_id=current_user.id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price,
        status="paid"
    )
    product.stock -= order.quantity
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/{order_id}", response_model=OrderOut, tags=["订单管理"])
def get_order(order_id: int, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return order