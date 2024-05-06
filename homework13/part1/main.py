from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Date, extract, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from datetime import date, datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError
import jwt
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Path
from dotenv import load_dotenv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global limiter

    app.state.limiter = limiter
    app.add_exception_handler(
        RateLimitExceeded, _rate_limit_exceeded_handler
    )

    yield


load_dotenv()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(Date)

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactInDB(ContactBase):
    id: int

    class Config:
        orm_mode = True

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_contacts(db: Session, q: str = None):
    if q:
        return db.query(Contact).filter(Contact.first_name.contains(q) | Contact.last_name.contains(q) | Contact.email.contains(q)).all()
    return db.query(Contact).all()

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def create_contact_db(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact_db(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        for key, value in contact.dict().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact_db(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact

def search_contacts_by_name(db: Session, name: str):
    return db.query(Contact).filter(Contact.first_name.contains(name) | Contact.last_name.contains(name)).all()

def get_contacts_upcoming_birthdays(db: Session):
    today = date.today()
    query = (
        db.query(Contact)
        .filter(
            and_(
                extract('month', Contact.birthday) == today.month,
                extract('day', Contact.birthday) >= today.day
            )
        )
        .all()
    )
    return query

def send_verification_email(to_email, verification_link):
    from_email = os.getenv('FROM_EMAIL')
    email_password = os.getenv('EMAIL_PASSWORD')
    subject = "Verify your email"
    body = f"Click the following link to verify your email: {verification_link}"
    
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    server = smtplib.SMTP("smtp.example.com", 587)
    server.starttls()
    server.login(from_email, email_password)
    text = message.as_string()
    server.sendmail(from_email, to_email, text)
    server.quit()

def generate_verification_token(user_id: int):
    payload = {"user_id": user_id}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.get("/verify_email/{user_id}")
async def verify_email(db: Session = Depends(get_db), user_id: int = Path(..., title="User ID")):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        verification_token = generate_verification_token(user_id)
        verification_link = f"http://localhost:8000/verify_email/{user_id}?token={verification_token}"
        send_verification_email(user.email, verification_link)
        
        user.email_verified = True 
        db.commit()
        return {"message": "Email verification link sent successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/register/")
async def register_new_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/protected/")
async def read_protected_data(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {"message": "Protected data"}

@app.post("/contacts/", response_model=ContactInDB)
@limiter.limit("5/minute")
def create_contact(request, contact: ContactCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_contact_db(db, contact)


@app.put("/update_avatar/")
async def update_avatar(avatar_url: str, db: Session = Depends(get_db),  current_user: User = Depends(get_current_active_user)):
    current_user.avatar_url = avatar_url
    db.commit()
    return {"message": "Avatar updated successfully"}

@app.get("/contacts/", response_model=List[ContactInDB])
def read_contacts(
    q: str = None, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_active_user)
):
    return get_contacts(db, q)

@app.get("/contacts/birthdays", response_model=List[ContactInDB])
def upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_contacts_upcoming_birthdays(db)

@app.get("/contacts/{contact_id}", response_model=ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return get_contact(db, contact_id)

@app.put("/contacts/{contact_id}", response_model=ContactInDB)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return update_contact_db(db, contact_id, contact)

@app.delete("/contacts/{contact_id}", response_model=ContactInDB)
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return delete_contact_db(db, contact_id)
