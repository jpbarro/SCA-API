from sqlalchemy.orm import Session
from app import models, schemas

def get_cat(db: Session, cat_id: int):
    return db.query(models.Cat).filter(models.Cat.id == cat_id).first()

def get_cats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cat).offset(skip).limit(limit).all()

def create_cat(db: Session, cat: schemas.CatCreate):
    db_cat = models.Cat(**cat.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_cat_salary(db: Session, cat_id: int, salary: float):
    db_cat = get_cat(db, cat_id)
    if db_cat:
        db_cat.salary = salary
        db.commit()
        db.refresh(db_cat)
    return db_cat

def delete_cat(db: Session, cat_id: int):
    db_cat = get_cat(db, cat_id)
    if db_cat:
        db.delete(db_cat)
        db.commit()
    return db_cat