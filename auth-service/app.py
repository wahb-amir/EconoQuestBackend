import os
from fastapi import FastAPI, Response, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from services.auth import get_supabase

load_dotenv()

app = FastAPI()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,   # required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Cookie helper ─────────────────────────────────────

def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,        # 1 hour
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,      # 7 days
        path="/",
    )

def clear_auth_cookies(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

# ── Models ────────────────────────────────────────────

class LoginRequest(BaseModel):
    email:    str
    password: str

class RegisterRequest(BaseModel):
    email:    str
    password: str
    username: str | None = None

# ── Routes ────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth-service"}

@app.post("/auth/register")
async def register(req: RegisterRequest, response: Response):
    from services.auth import get_supabase_for_auth
    supabase = get_supabase_for_auth()  # ← changed
    try:
        result = supabase.auth.admin.create_user({
            "email":            req.email,
            "password":         req.password,
            "email_confirm":    True,   # mark as confirmed immediately
            "user_metadata":    {"username": req.username or req.email.split("@")[0]}
        })

        if not result.user:
            raise HTTPException(status_code=400, detail="Registration failed")

        # now sign them in to get session tokens
        supabase_anon = get_supabase()
        signin = supabase_anon.auth.sign_in_with_password({
            "email":    req.email,
            "password": req.password,
        })

        if signin.session:
            set_auth_cookies(
                response,
                signin.session.access_token,
                signin.session.refresh_token
            )

        return {
            "user": {
                "id":       result.user.id,
                "email":    result.user.email,
                "username": result.user.user_metadata.get("username"),
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/auth/login")
async def login(req: LoginRequest, response: Response):
    supabase = get_supabase()
    try:
        result = supabase.auth.sign_in_with_password({
            "email":    req.email,
            "password": req.password,
        })

        if not result.session:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        set_auth_cookies(
            response,
            result.session.access_token,
            result.session.refresh_token
        )

        return {
            "user": {
                "id":       result.user.id,
                "email":    result.user.email,
                "username": result.user.user_metadata.get("username"),
            }
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/auth/logout")
async def logout(response: Response, request: Request):
    supabase = get_supabase()
    access_token = request.cookies.get("access_token")

    if access_token:
        try:
            supabase.auth.admin.sign_out(access_token)
        except:
            pass  # best effort

    clear_auth_cookies(response)
    return {"message": "logged_out"}

@app.post("/auth/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token")

    supabase = get_supabase()
    try:
        result = supabase.auth.refresh_session(refresh_token)

        if not result.session:
            clear_auth_cookies(response)
            raise HTTPException(status_code=401, detail="Session expired")

        set_auth_cookies(
            response,
            result.session.access_token,
            result.session.refresh_token
        )

        return {
            "user": {
                "id":       result.user.id,
                "email":    result.user.email,
                "username": result.user.user_metadata.get("username"),
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        clear_auth_cookies(response)
        raise HTTPException(status_code=401, detail="Session expired")

@app.get("/auth/me")
async def me(request: Request):
    access_token = request.cookies.get("access_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    supabase = get_supabase()
    try:
        result = supabase.auth.get_user(access_token)
        if not result.user:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "user": {
                "id":       result.user.id,
                "email":    result.user.email,
                "username": result.user.user_metadata.get("username"),
            }
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/auth/google")
async def oauth_google(request: Request):
    supabase = get_supabase()
    result = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": f"{os.getenv('AUTH_SERVICE_URL')}/auth/callback"
        }
    })
    return {"url": result.url}

@app.get("/auth/github")
async def oauth_github(request: Request):
    supabase = get_supabase()
    result = supabase.auth.sign_in_with_oauth({
        "provider": "github",
        "options": {
            "redirect_to": f"{os.getenv('AUTH_SERVICE_URL')}/auth/callback"
        }
    })
    return {"url": result.url}

@app.get("/auth/callback")
async def oauth_callback(request: Request, response: Response):
    # Supabase sends code in query params
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    supabase = get_supabase()
    try:
        result = supabase.auth.exchange_code_for_session({"auth_code": code})

        if not result.session:
            raise HTTPException(status_code=400, detail="OAuth failed")

        set_auth_cookies(
            response,
            result.session.access_token,
            result.session.refresh_token
        )

        # redirect to frontend dashboard
        response.status_code = 302
        response.headers["location"] = f"{FRONTEND_URL}/dashboard"
        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))