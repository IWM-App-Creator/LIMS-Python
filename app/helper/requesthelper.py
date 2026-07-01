from fastapi import Request

class RequestHelper:

    @staticmethod
    async def init(request: Request):
        request.state.headers = dict(request.headers)
        request.state.jwt = request.headers.get("authorization")
        if request.method == "GET":
            request.state.params = dict(request.query_params)
        else:
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type:
                request.state.params = await request.json()
            else:
                request.state.params = dict(await request.form())