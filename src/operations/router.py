from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

# Роутер объединяет набор эндпойнтов
router = APIRouter(
    prefix="/operations",
    tags=["Operation"] 
)

@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    """Получаем сессию, под наш запрос. Выбираем все записи в таблице operations.
    Фильтруем по полю type."""
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        x = 1 / 0

        # return result.mappings().all()
        return{
            "status": "success",
            "data": None,
            "details": "На ноль делить нельзя!!!"
        }
    except ZeroDivisionError:
        return{
            "status": "error",
            "data": None,
        "details": "На ноль делить нельзя!!!"
        }
    except:
        return{
            "status": "error",
            "data": None,
            "details": None
        }
    

@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    """Добавление данных с помощью POST-запроса.Вовзращаем статус добавления данных.
    OperationCreate - Pydantic schema. new_operation - экземпляр класса Pydantic и далее распаковка в {}.
    После execute(выполнить), всегда должен быть commit(совершить)."""
    stmt = insert(operation).values(**new_operation.__dict__)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}