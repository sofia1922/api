from fastapi import Request, HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from core.redis import redis_client

AUTH_LIMIT = 10
ANON_LIMIT = 2
WINDOW = 60


async def rate_limiter(request: Request):

    auth_header = request.headers.get("Authorization")

    if auth_header:
        key = f"rate_limit:auth:{auth_header}"
        limit = AUTH_LIMIT
    else:
        client_ip = request.client.host
        key = f"rate_limit:anon:{client_ip}"
        limit = ANON_LIMIT

    current = await redis_client.get(key)

    if current is None:
        await redis_client.set(key, 1, ex=WINDOW)
        return

    current = int(current)

    if current >= limit:
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )

    await redis_client.incr(key)