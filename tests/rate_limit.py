import pytest

from httpx import AsyncClient
from unittest.mock import AsyncMock, patch

from main import app


@pytest.mark.asyncio
async def test_auth_user_under_limit():

    with patch("middlewares.rate_limiter.redis_client") as mock_redis:

        mock_redis.get = AsyncMock(return_value="5")
        mock_redis.incr = AsyncMock()

        async with AsyncClient(
            app=app,
            base_url="http://test"
        ) as client:

            response = await client.get(
                "/books",
                headers={
                    "Authorization": "Bearer fake-token"
                }
            )

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_auth_user_limit_exceeded():

    with patch("middlewares.rate_limiter.redis_client") as mock_redis:

        mock_redis.get = AsyncMock(return_value="10")

        async with AsyncClient(
            app=app,
            base_url="http://test"
        ) as client:

            response = await client.get(
                "/books",
                headers={
                    "Authorization": "Bearer fake-token"
                }
            )

        assert response.status_code == 429


@pytest.mark.asyncio
async def test_anon_user_under_limit():

    with patch("middlewares.rate_limiter.redis_client") as mock_redis:

        mock_redis.get = AsyncMock(return_value="1")
        mock_redis.incr = AsyncMock()

        async with AsyncClient(
            app=app,
            base_url="http://test"
        ) as client:

            response = await client.get("/books")

        assert response.status_code == 200


@pytest.mark.asyncio
async def test_anon_user_limit_exceeded():

    with patch("middlewares.rate_limiter.redis_client") as mock_redis:

        mock_redis.get = AsyncMock(return_value="2")

        async with AsyncClient(
            app=app,
            base_url="http://test"
        ) as client:

            response = await client.get("/books")

        assert response.status_code == 429