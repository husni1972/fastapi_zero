from dataclasses import asdict

import pytest
from sqlalchemy import select

from fastapi_zero.models import Todo, User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user_create = User(
            username='test',
            email='test@test',
            password='secret',
        )
        session.add(user_create)
        await session.commit()
        user_read = await session.scalar(
            select(User).where(User.username == 'test')
        )

    assert asdict(user_read) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
        'todos': [],
    }


@pytest.mark.asyncio
async def test_create_todo(session, user, mock_db_time):
    with mock_db_time(model=Todo) as time:
        todo = Todo(
            title='Test Todo',
            description='Test Description',
            state='draft',
            user_id=user.id,
        )

        session.add(todo)
        await session.commit()

        todo = await session.scalar(select(Todo))

        assert asdict(todo) == {
            'created_at': time,
            'description': 'Test Description',
            'id': 1,
            'state': 'draft',
            'title': 'Test Todo',
            'updated_at': time,
            'user_id': 1,
        }


@pytest.mark.asyncio
async def test_user_todo_relationship(session, user):
    todo = Todo(
        title='Test Todo',
        description='Test Description',
        state='draft',
        user_id=user.id,
    )

    session.add(todo)
    await session.commit()
    # Atualiza as informacoes do usuario com a lista de Todo (Ver Models)
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert user.todos == [todo]
