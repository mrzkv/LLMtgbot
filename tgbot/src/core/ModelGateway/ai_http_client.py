from enum import Enum
from types import TracebackType
from typing import Any

import aiohttp
import orjson


class Methods(Enum):
    """Enumeration of standard HTTP methods."""
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

class AIHttpClient:
    """
    Asynchronous HTTP client optimized for maximum performance with aiohttp.

    This client is designed for a lifecycle where it's initialized once,
    used for multiple requests, and then can be discarded, relying on
    proper session closure to prevent resource leaks.
    It ensures `aiohttp.ClientSession` is reused efficiently across requests.
    """

    def __init__(
            self,
            base_url: str = "",
            headers: dict[str, str] | None = None,
            cookies: dict[str, str] | None = None,
            timeout: float = 30.0,
    ) -> None:
        """
        Initializes the HTTP client with default settings.

        Args:
            base_url (str): The base URL for all requests made by this client.
            headers (Dict[str, str] | None): Default headers to be sent with all requests.
            cookies (Dict[str, str] | None): Default cookies to be sent with all requests.
            timeout (float): Total timeout for each request in seconds.
                                       This covers connection, send, and read timeouts.
        """
        self._base_url: str = base_url
        self._default_headers: dict[str, str] = headers if headers is not None else {}
        self._default_cookies: dict[str, str] = cookies if cookies is not None else {}
        self._timeout: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=timeout)

        self._session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers=self._default_headers,
            cookies=self._default_cookies,
            timeout=self._timeout,
            base_url=self._base_url,
            json_serialize=orjson.dumps,
        )

    async def _request(
            self,
            method: Methods,
            path: str,
            headers: dict[str, str] | None = None,
            cookies: dict[str, str] | None = None,
            json_data: dict[str, Any] | None = None,
            data: str | bytes | dict[str, Any] | None = None,
            params: dict[str, str] | None = None,
            allow_redirects: bool = True,
    ) -> aiohttp.ClientResponse:
        """Internal method for executing HTTP requests using the persistent ClientSession."""
        combined_headers: dict[str, str] = {**self._default_headers, **(headers or {})}
        combined_cookies: dict[str, str] = {**self._default_cookies, **(cookies or {})}

        async with self._session.request(
                method.value, # Access the string value of the Enum
                path,
                headers=combined_headers,
                cookies=combined_cookies,
                json=json_data,
                data=data,
                params=params,
                allow_redirects=allow_redirects,
        ) as response:
            response.raise_for_status()
            return response

    async def get(
            self,
            path: str,
            headers: dict[str, str] | None = None,
            cookies: dict[str, str] | None = None,
            params: dict[str, str] | None = None,
            allow_redirects: bool = True,
    ) -> aiohttp.ClientResponse:
        """Performs a GET request."""
        return await self._request(Methods.GET, path, headers=headers, cookies=cookies, params=params,
                                   allow_redirects=allow_redirects)

    async def post(
            self,
            path: str,
            headers: dict[str, str] | None = None,
            cookies: dict[str, str] | None = None,
            json_data: dict[str, Any] | None = None,
            data: str | bytes | dict[str, Any] | None = None,
            params: dict[str, str] | None = None,
            allow_redirects: bool = True,
    ) -> aiohttp.ClientResponse:
        """Performs a POST request."""
        return await self._request(Methods.POST, path, headers=headers, cookies=cookies, json_data=json_data,
                                   data=data, params=params, allow_redirects=allow_redirects)

    async def put(
            self,
            path: str,
            headers: dict[str, str] | None = None,
            cookies: dict[str, str] | None = None,
            json_data: dict[str, Any] | None = None,
            data: str | bytes | dict[str, Any] | None = None,
            params: dict[str, str] | None = None,
            allow_redirects: bool = True,
    ) -> aiohttp.ClientResponse:
        """Performs a PUT request."""
        return await self._request(Methods.PUT, path, headers=headers, cookies=cookies, json_data=json_data,
                                   data=data, params=params, allow_redirects=allow_redirects)

    async def delete(
            self,
            path: str,
            headers: dict[str, str] | None = None,
            cookies: dict[str, str] | None = None,
            json_data: dict[str, Any] | None = None,
            data: str | bytes | dict[str, Any] | None = None,
            params: dict[str, str] | None = None,
            allow_redirects: bool = True,
    ) -> aiohttp.ClientResponse:
        """Performs a DELETE request."""
        return await self._request(Methods.DELETE, path, headers=headers, cookies=cookies, json_data=json_data,
                                   data=data, params=params, allow_redirects=allow_redirects)

    async def patch(
        self,
        path: str,
        headers: dict[str, str] | None = None,
        cookies: dict[str, str] | None = None,
        json_data: dict[str, Any] | None = None,
        data: str | bytes | dict[str, Any] | None = None,
        params: dict[str, str] | None = None,
        allow_redirects: bool = True,
    ) -> aiohttp.ClientResponse:
        """Performs a PATCH request."""
        return await self._request(Methods.PATCH, path, headers=headers, cookies=cookies, json_data=json_data,
                                   data=data, params=params, allow_redirects=allow_redirects)


    async def close(self) -> None:
        """
        Explicitly closes the underlying aiohttp.ClientSession.
        This must be called when the HttpClient instance is no longer needed
        to properly release network resources.
        """
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> "AIHttpClient":
        """Enters the async context for the client."""
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        """Exits the async context, ensuring the aiohttp session is closed."""
        await self.close()
