from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.dependencies import get_db
from app.core.security import validate_internal_api_key
from app.models.models import Categories
from app.schemas.category import CategoryRequest


router = APIRouter(tags=["categories"], dependencies=[Depends(validate_internal_api_key)])

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/all-categories", status_code=status.HTTP_200_OK)
async def get_all_categories(db: db_dependency):
    return db.query(Categories).all()


@router.get("/category/{category_id}", status_code=status.HTTP_200_OK)
async def get_category_by_id(category_id: int, db: db_dependency):
    category_model = db.query(Categories).filter(Categories.id == category_id).first()

    if category_model is not None:
        category = {
            "id": category_model.id,
            "name": category_model.name,
            "description": category_model.description
        }
    
        return category
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")


@router.post("/create-category", status_code=status.HTTP_201_CREATED)
async def create_category(category_request: CategoryRequest, db: db_dependency):
    category = Categories(
        name=category_request.name,
        description=category_request.description
    )
    try:
        db.add(category)
        db.commit()
        db.refresh(category)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists"
        )

    return {
        "message": "Category created successfully",
        "category_id": category.id,
        "category_name": category.name
    }

@router.put("/update-category", status_code=status.HTTP_202_ACCEPTED)
async def update_category(db: db_dependency, category_id: int, category_request: CategoryRequest):
    category_model = db.query(Categories).filter(Categories.id == category_id).first()

    if category_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    category_model.name = category_request.name
    category_model.description = category_request.description
    
    db.add(category_model)
    db.commit()

    return {
        "message": "Category updated successfully",
        "category_id": category_model.id,
        "category_name": category_model.name
    }