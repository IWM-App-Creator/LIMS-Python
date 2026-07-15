from fastapi import Request, UploadFile

class RequestData:

    @staticmethod
    def params(request: Request):
        return request.state.params

    @staticmethod
    def jwt(request: Request):
        return request.state.jwt

    @staticmethod
    async def file(request: Request, field_name: str) -> UploadFile | None:
        form = await request.form()
        return form.get(field_name)