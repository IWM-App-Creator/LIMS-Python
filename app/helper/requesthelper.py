from fastapi import Request

class RequestData:

    @staticmethod
    def params(request: Request):
        return request.state.params

    @staticmethod
    def jwt(request: Request):
        return request.state.jwt

    @staticmethod
    def user(request: Request):
        return request.state.user