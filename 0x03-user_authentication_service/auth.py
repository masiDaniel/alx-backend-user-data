#!/usr/bin/env python3
"""
Defines a class Auth
"""

from db import DB
from bcrypt import hashpw, gensalt, checkpw
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    Returns the hash password
    """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """
    Returns a string representation of the
    new UUID
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self) -> None:
        """
        Initializes values
        """
        self._db = DB()

    def register_user(self, email: str,
                      password: str) -> User:
        """
        Registers a user
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            password = _hash_password(password)
            user = User(email=email, hashed_password=password)
            self._db._session.add(user)
            self._db._session.commit()
            return user
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        Locates a user by email, if user exists it checks
        whether the password is the valid and returns True
        otherwise returns False
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        else:
            return checkpw(password.encode('utf-8'),
                           user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Finds user corresponding to the email
        generates a new UUID and stores it and returns
        session ID
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        else:
            user.session_id = _generate_uuid()
            self._db._session.add(user)
            self._db._session.commit()
            return user.session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Returns the corresponding User or None
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return user
