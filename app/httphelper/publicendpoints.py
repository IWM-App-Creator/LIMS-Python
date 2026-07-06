PUBLIC_APIS = {
    "/docs",
    "/openapi.json",
    "/favicon.ico",
    "/backend/docs",
}

PUBLIC_PREFIXES = (
    "/api/v1/auth/",
    "/api/v1/workspace/isvalidws",
    "/redoc",
    "/backend/api/v1/auth/",
)

def isPublicEndpoint(path: str) -> bool:
    return (
        path in PUBLIC_APIS
        or any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES)
    )