#!/usr/bin/env python3
""" This module contains the Json response class
"""
from json import dumps
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from .custom_json_encoder import (
    CustomJSONEncoder,
)  # Ensure you import the custom JSON encoder


class JsonResponseDict(JSONResponse):

    def __init__(
        self, message: str, data: dict | None = None, error: str = "", status_code=200
    ):
        """initialize your response"""
        self.message = message
        self.data = data
        self.error = error
        self._status_code = status_code
        super().__init__(
            content=jsonable_encoder(
                self.response(), custom_encoder={datetime: lambda v: v.isoformat()}
            ),
            status_code=status_code,
        )

    def __repr__(self):
        return {
            "message": self.message,
            "data": self.data,
            "error": self.error,
            "status_code": self._status_code,
        }

    def __str__(self):
        """string representation"""
        return dumps(
            {
                "message": self.message,
                "data": self.data,
                "error": self.error,
                "status_code": self._status_code,
            },
            cls=CustomJSONEncoder,
        )

    def response(self):
        """return a json response dictionary"""
        print(f"response: {format(self)}")
        if self._status_code >= 300:
            return {
                "message": self.message,
                "error": self.error,
                "status_code": self._status_code,
            }
        else:
            return {
                "message": self.message,
                "data": self.data,
                "status_code": self._status_code,
            }
