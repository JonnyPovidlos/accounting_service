from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from accounting_service.category.schemas import BaseCategory, Category
from accounting_service.category.service import CategoryService
from exceptions import NoResultFoundCustom

router = APIRouter(prefix='/categories', tags=['category'])


@router.post('',
             status_code=status.HTTP_201_CREATED,
             response_model=Category)
def create_category(category_create: BaseCategory,
                    service: CategoryService = Depends()):
    category = service.create_category(category_create)
    return category


@router.patch('/{category_id}',
              status_code=status.HTTP_202_ACCEPTED,
              response_model=Category)
def update_category(category_id: int,
                    category_update: BaseCategory,
                    service: CategoryService = Depends()):
    try:
        category = service.update_category(category_id, category_update)
        return category
    except NoResultFoundCustom:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete('/{category_id}',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int,
                    service: CategoryService = Depends()):
    try:
        service.delete_category(category_id)
        return {}
    except NoResultFoundCustom:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
