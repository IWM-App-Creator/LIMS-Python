PUBLIC_APIS = {
    "/docs",
    "/openapi.json",
    "/favicon.ico",
}

PUBLIC_PREFIXES = (
    "/api/v1/auth/",
    "/redoc",
)

def isPublicEndpoint(path: str) -> bool:
    return (
        path in PUBLIC_APIS
        or any(path.startswith(prefix) for prefix in PUBLIC_PREFIXES)
    )