from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, services, deps

router = APIRouter(
    prefix="/cats",
    tags=["Cats"],
)

@router.post("/", response_model=schemas.Cat, status_code=status.HTTP_201_CREATED)
async def create_spy_cat(cat: schemas.CatCreate, db: Session = Depends(deps.get_db)):
    is_valid_breed = await services.validate_cat_breed(cat.breed)
    if not is_valid_breed:
        raise HTTPException(status_code=400, detail=f"Breed '{cat.breed}' is not a valid cat breed.")
    return crud.create_cat(db=db, cat=cat)

@router.get("/", response_model=List[schemas.Cat])
def read_spy_cats(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    cats = crud.get_cats(db, skip=skip, limit=limit)
    return cats

@router.get("/{cat_id}", response_model=schemas.Cat)
def read_spy_cat(cat_id: int, db: Session = Depends(deps.get_db)):
    db_cat = crud.get_cat(db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat

@router.patch("/{cat_id}", response_model=schemas.Cat)
def update_cat_salary_endpoint(cat_id: int, cat_update: schemas.CatUpdate, db: Session = Depends(deps.get_db)):
    db_cat = crud.get_cat(db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    if cat_update.salary is None:
        raise HTTPException(status_code=400, detail="Salary must be provided for update.")
    return crud.update_cat_salary(db=db, cat_id=cat_id, salary=cat_update.salary)

@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_spy_cat(cat_id: int, db: Session = Depends(deps.get_db)):
    db_cat = crud.get_cat(db, cat_id=cat_id)
    if db_cat is None:
        raise HTTPException(status_code=404, detail="Cat not found")
    crud.delete_cat(db=db, cat_id=cat_id)
    return