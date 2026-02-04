from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timezone

from app.database.dependencies import get_db
from app.core.security import validate_internal_api_key
from app.models.models import Categories, Products
from app.schemas.product import ProductRequest


router = APIRouter(tags=["products"], dependencies=[Depends(validate_internal_api_key)])

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/all-products", status_code=status.HTTP_200_OK)
async def get_all_products(db: db_dependency):
    return db.query(Products).all()


@router.get("/product/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: int, db: db_dependency):
    product_model = db.query(Products).options(joinedload(Products.category)).filter(Products.id == product_id).first()

    if product_model is not None:
        product = {
            "id": product_model.id,
            "name": product_model.name,
            "description": product_model.description,
            "price": product_model.price,
            "stock": product_model.stock,
            "category": {
                "category_id": product_model.category.id,
                "category_name": product_model.category.name
            }
        }
    
        return product
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@router.get("/products-by-category/{category_id}", status_code=status.HTTP_200_OK)
async def get_products_by_category(category_id: int, db: db_dependency):
    products_model = db.query(Products).options(joinedload(Products.category)).filter(Products.category_id == category_id).all()

    if not products_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products found for this category")

    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock
        }
        for product in products_model
    ]


@router.post("/create-product/category/{category_id}", status_code=status.HTTP_201_CREATED)
async def create_product(category_id: int, product_request: ProductRequest, db: db_dependency):
    
    category_model = db.query(Categories).filter(Categories.id == category_id).first()
    product_model = db.query(Products).filter(Products.name == product_request.name, Products.category_id == category_id).first()

    if category_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    if product_model is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product already exists")
    
    product = Products(
        name=product_request.name,
        description=product_request.description,
        price=product_request.price,
        stock=product_request.stock,
        category_id=category_id,
        created_at=datetime.now(timezone.utc)
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "message": "Product created successfully",
        "product_id": product.id,
        "product_name": product.name,
        "product_description": product.description,
        "product_price": product.price,
        "product_stock": product.stock,
        "product_category_id": product.category_id,
        "product_category_name": product.category.name
    }


@router.put("/update-product/{product_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_product(db: db_dependency, product_id: int, product_request: ProductRequest):
    product_model = db.query(Products).filter(Products.id == product_id).first()

    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    product_model.name = product_request.name
    product_model.description = product_request.description
    product_model.price = product_request.price
    product_model.stock = product_request.stock
    product_model.category_id = product_model.category_id
    product_model.created_at = datetime.now(timezone.utc)
    
    db.add(product_model)
    db.commit()

    return {
        "message": "Product updated successfully",
        "product_id": product_model.id,
        "product_name": product_model.name
    }


@router.delete("/delete-product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(db: db_dependency, product_id: int):
    product_model = db.query(Products).filter(Products.id == product_id).first()

    if product_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    db.query(Products).filter(Products.id == product_id).delete()
    db.commit()