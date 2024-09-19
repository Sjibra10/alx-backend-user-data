#!/usr/bin/env python3
"""Session authentication code base"""

from flask.globals import session
from api.v1.auth.auth import Auth
from typing import Dict
from models.user import User
import uuid


class SessionAuth(Auth):
    """ inherites session from Auth"""

    user_id_by_session_id: Dict[str, str] = {}

    def create_session(self, user_id: str = None) -> str:
        """ create session ID"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def current_user(self, request=None):
        """ carent user code base"""
        cookie = self.session_cookie(request)
        session_user_id = self.user_id_for_session_id(cookie)
        user_id = User.get(session_user_id)
        return user_id
    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def destroy_session(self, request=None):
        """ destroy or delete"""
        cookie_data = self.session_cookie(request)
        if cookie_data is None:
            return False

        if not self.user_id_for_session_id(cookie_data):
            return False

        del self.user_id_by_session_id[cookie_data]
        return True
