#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """
    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str,
                 hashed_password: str) -> User:
        """
        Saves a user to the database and returns a user object
        """
        user1 = User()
        user1.email = email
        user1.hashed_password = hashed_password
        self._session.add(user1)
        self._session.commit()
        return user1

    def find_user_by(self, **kwargs) -> User:
        """
        Takes in arbitary keyword arguments and returns the
        first row found in the users table as filtered by the
        method's input arguments.
        """
        for x, y in kwargs.items():
            try:
                query = (self._session.query(User)
                         .filter(User.__dict__[x] == y).one())
            except KeyError:
                raise InvalidRequestError
            except NoResultFound:
                raise NoResultFound
            else:
                return query

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Uses find_user_by to locate the user to update
        then updates the user's attributes as passed and
        returns None
        """
        user = self.find_user_by(id=user_id)
        for x, y in kwargs.items():
            if x in user.__dict__:
                user.__dict__[x] = y
                self._session.add(user)
                self._session.commit()
            else:
                raise ValueError
