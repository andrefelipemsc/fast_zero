from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='username', email='username@mail.com', password='password'
    )
    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.id == 1))

    assert result.id == 1
