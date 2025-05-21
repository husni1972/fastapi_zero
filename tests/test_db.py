from dataclasses import asdict

from sqlalchemy import select

from fastapi_zero.models import User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user_create = User(
            username='test',
            email='test@test',
            password='secret',
        )
        session.add(user_create)
        session.commit()
        user_read = session.scalar(select(User).where(User.username == 'test'))

    assert asdict(user_read) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
    }
