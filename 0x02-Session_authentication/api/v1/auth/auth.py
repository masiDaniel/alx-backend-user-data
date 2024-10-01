#!/usr/bin/env python3
"""
Defines a class Auth
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    defines Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) \
            -> bool:
        """
        Returns False
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for x in excluded_paths:
            if path.strip('/') == x.strip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        if request is None:
            return None
        if request.headers.get('Authorization'):
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        return None
