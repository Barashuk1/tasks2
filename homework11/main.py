from fastapi import FastAPI, Depends
from sqlalchemy import and_, create_engine, Column, Integer, String, Date, extract, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List
from datetime import date, timedelta
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

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
    next_week = today + timedelta(days=7)
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

@app.post("/contacts/", response_model=ContactInDB)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact_db(db, contact)

@app.get("/contacts/", response_model=List[ContactInDB])
def read_contacts(
    q: str = None, 
    db: Session = Depends(get_db)
):
    return get_contacts(db, q)

@app.get("/contacts/birthdays", response_model=List[ContactInDB])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return get_contacts_upcoming_birthdays(db)

@app.get("/contacts/{contact_id}", response_model=ContactInDB)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    return get_contact(db, contact_id)

@app.put("/contacts/{contact_id}", response_model=ContactInDB)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db)):
    return update_contact_db(db, contact_id, contact)

@app.delete("/contacts/{contact_id}", response_model=ContactInDB)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    return delete_contact_db(db, contact_id)


