PUBLIC_APIS = {
    "/docs",
    "/openapi.json",
    "/favicon.ico",
    "/backend/docs",
    "/api/v1/workspace/isvalidws",
    "/api/v1/workspace/isvalidws",
    "/api/v1/workspace/getlist",
}

PUBLIC_PREFIXES = (
    "/api/v1/auth/",
    "/backend/api/v1/auth/",
)

def isPublicEndpoint(path: str) -> bool:
    return (
        path in PUBLIC_APIS
        or any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES)
    )