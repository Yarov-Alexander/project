from fastapi import APIRouter, status, HTTPException
from .services import CategoryServices
from .schemas import Category as CategorySchema

router = APIRouter(
    prefix="/categories",
    tags=["categories"],
)


@router.get("/", response_model=list[CategorySchema])
async def get_all_categories(db : AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех категорий товаров.
    """
    result = await db.scalars(select(CategoryModel).where(CategoryModel.is_active == True))

    return result.all()


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_admin)):
    """
    Создаёт новую категорию.
    """
    if category.parent_id is not None:
        stmt = select(CategoryModel).where(CategoryModel.id == category.parent_id, CategoryModel.is_active == True)

        result = await db.scalars(stmt)
        parent = result.first()
        if parent is None:
            raise HTTPException(status_code=400, detail="Parent category not found")
    db_category = CategoryModel(**category.model_dump())
    db.add(db_category)
    await db.commit()

    return db_category


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int, category: CategoryCreate, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_admin)):
    """
    Обновляет категорию по её ID.
    """
    stmp = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active == True)
    result = await db.scalars(stmp)
    db_category = result.first()

    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    if db_category.parent_id is not None:
        stm = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active == True)
        result = await db.scalars(stm)
        parent = result.first()

        if parent is None:
            raise HTTPException(status_code=400, detail="Parent category not found")

        if parent.id == category_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category cannot be its own parent")

    await db.execute(update(CategoryModel).where(CategoryModel.id == category_id).values(**category.model_dump()))
    await db.commit()
    return db_category


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, db: AsyncSession = Depends(get_async_db), current_user: UserModel = Depends(get_current_admin)):
    """
    Удаляет категорию по её ID.
    """
    stmp = select(CategoryModel).where(CategoryModel.id == category_id, CategoryModel.is_active == True)
    res = await db.scalars(stmp)
    result = res.first()
    if result is None:
        raise HTTPException(status_code=404, detail="Category not found")
    await db.execute(update(CategoryModel).where(CategoryModel.id == category_id).values(is_active=False))
    await db.commit()
    return {"message": f"Категория с ID {category_id} удалена (заглушка)"}