from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from .jwt_middleware import verify_jwt_token, extract_token_from_header

# Configuration
PROTECTED_PATHS = ["/apps/", "/run_sse", "/run"]
PUBLIC_PATHS = ["/", "/health", "/docs", "/openapi.json", "/list-apps"]

def add_cors_headers(response: JSONResponse) -> JSONResponse:
    """Add CORS headers to a response"""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

def create_error_response(status_code: int, message: str) -> JSONResponse:
    """Create an error response with CORS headers"""
    response = JSONResponse(
        status_code=status_code,
        content={"error": message}
    )
    return add_cors_headers(response)

def should_skip_jwt_validation(request: Request) -> bool:
    """Check if JWT validation should be skipped for this request"""
    return (
        request.url.path in PUBLIC_PATHS or
        request.method == "OPTIONS"
    )

def is_protected_path(request: Request) -> bool:
    """Check if the request path requires JWT protection"""
    return any(request.url.path.startswith(path) for path in PROTECTED_PATHS)

async def jwt_middleware(request: Request, call_next):
    """JWT middleware to protect agent endpoints"""
    print(f"🔍 Request to: {request.url.path} - Method: {request.method}")

    if should_skip_jwt_validation(request):
        print(f"✅ Skipping JWT for: {request.url.path}")
        return await call_next(request)

    if is_protected_path(request):
        print(f"🔒 JWT required for: {request.url.path}")
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            print("❌ No Authorization header provided")
            return create_error_response(401, "Authorization header required")

        try:
            token = extract_token_from_header(auth_header)
            user_info = verify_jwt_token(token)
            print(f"✅ JWT valid for user: {user_info.get('username')}")
            request.state.user = user_info

        except HTTPException as e:
            print(f"❌ JWT error: {e.detail}")
            return create_error_response(e.status_code, e.detail)
        except Exception as e:
            print(f"❌ JWT error: {str(e)}")
            return create_error_response(401, "Invalid authentication")

    return await call_next(request)
