from fastapi_users.authentication import CookieTransport, AuthenticationBackend, JWTStrategy


cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600)

# Ключе Secret нужен для кодирования и декодирования токенов, обычно переносят его в секреты(.env)
SECRET = "SECRET"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


# Создание transport и strategy (cookie_transport и JWT)
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

