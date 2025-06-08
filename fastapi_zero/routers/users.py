from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from fastapi_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]
T_FilterPage = Annotated[FilterPage, Query()]


@router.get('/current', status_code=HTTPStatus.OK, response_model=UserPublic)
def get_user(current_user: T_CurrentUser):
    return current_user


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema, session: T_Session):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                detail='User already exists',
                status_code=HTTPStatus.CONFLICT,
            )
        elif db_user.email == user.email:
            raise HTTPException(
                detail='Email already exists', status_code=HTTPStatus.CONFLICT
            )

    hash_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password=hash_password,
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    session: T_Session,
    filter_users: T_FilterPage,
):
    query = await session.scalars(
        select(User).limit(filter_users.limit).offset(filter_users.offset)
    )

    db_users = query.all()

    return {'users': db_users}


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def read_user(user_id: int, session: T_Session):
    db_user = await session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    session: T_Session,
    current_user: T_CurrentUser,
    user_id: int,
    user: UserSchema,
):
    if current_user.id != user_id:
        raise HTTPException(
            detail='Not enough permissions', status_code=HTTPStatus.FORBIDDEN
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        await session.commit()
        await session.refresh(current_user)

        return current_user
    except Exception as e:
        raise HTTPException(
            detail=f'Testando {e}', status_code=HTTPStatus.FAILED_DEPENDENCY
        )

    # PERDE O SENTIDO POIS NÃO ESTA SE BUSCANDO MAIS BUSCANDO A
    # INFORMAÇÃO DO BANCO DE DADOS
    # except IntegrityError:
    #     raise HTTPException(
    #         detail='Username or Email already exists',
    #         status_code=HTTPStatus.CONFLICT,
    #     )


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(
    session: T_Session,
    current_user: T_CurrentUser,
    user_id: int,
):
    if current_user.id != user_id:
        raise HTTPException(
            detail='Not enough permissions', status_code=HTTPStatus.FORBIDDEN
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
