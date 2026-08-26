"""Small credential-safe JSON transport for approved HTTPS providers."""

from __future__ import annotations

import json
import socket
from typing import Any, Mapping, Protocol, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from .errors import ProviderError, ResponseValidationError

JsonData = dict[str, Any] | list[Any]
QueryValue = str | int | float | Sequence[str]


class JsonTransport(Protocol):
    def get_json(
        self,
        *,
        base_url: str,
        path: str,
        params: Mapping[str, QueryValue] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float = 20.0,
    ) -> JsonData: ...


class UrllibJsonTransport:
    """GET JSON while keeping query-string secrets out of raised errors."""

    def __init__(self, *, max_response_bytes: int = 25_000_000) -> None:
        if max_response_bytes < 1:
            raise ValueError("max_response_bytes must be positive")
        self.max_response_bytes = max_response_bytes

    def get_json(
        self,
        *,
        base_url: str,
        path: str,
        params: Mapping[str, QueryValue] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float = 20.0,
    ) -> JsonData:
        self._validate_target(base_url, path)
        query = urlencode(params or {}, doseq=True)
        url = f"{base_url.rstrip('/')}{path}"
        if query:
            url = f"{url}?{query}"
        request = Request(
            url,
            headers={"Accept": "application/json", **dict(headers or {})},
            method="GET",
        )

        try:
            with urlopen(request, timeout=timeout) as response:
                raw = response.read(self.max_response_bytes + 1)
        except HTTPError as exc:
            raise ProviderError(
                f"Provider returned HTTP {exc.code} for {path}"
            ) from None
        except (URLError, TimeoutError, socket.timeout) as exc:
            raise ProviderError(f"Provider request failed for {path}: {type(exc).__name__}") from None

        if len(raw) > self.max_response_bytes:
            raise ResponseValidationError(f"Provider response exceeded the size limit for {path}")
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ResponseValidationError(f"Provider returned invalid JSON for {path}") from None
        if not isinstance(payload, (dict, list)):
            raise ResponseValidationError(f"Provider returned an invalid JSON root for {path}")
        return payload

    @staticmethod
    def _validate_target(base_url: str, path: str) -> None:
        target = urlsplit(base_url)
        if target.scheme != "https" or not target.netloc or target.path not in ("", "/"):
            raise ValueError("base_url must be an HTTPS origin")
        if not path.startswith("/") or path.startswith("//") or "://" in path:
            raise ValueError("path must be an absolute path on the configured origin")

