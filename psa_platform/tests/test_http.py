from email.message import Message
from io import BytesIO
from unittest import TestCase
from unittest.mock import patch
from urllib.error import HTTPError

from psa_platform.errors import ProviderError, ResponseValidationError
from psa_platform.http import UrllibJsonTransport


class _Response:
    def __init__(self, value: bytes) -> None:
        self.value = value

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return None

    def read(self, _limit: int) -> bytes:
        return self.value


class HttpTests(TestCase):
    def test_rejects_non_https_origin(self) -> None:
        with self.assertRaisesRegex(ValueError, "HTTPS origin"):
            UrllibJsonTransport().get_json(base_url="http://example.com", path="/")

    @patch("psa_platform.http.urlopen")
    def test_decodes_json_object(self, urlopen) -> None:
        urlopen.return_value = _Response(b'{"ok": true}')
        result = UrllibJsonTransport().get_json(
            base_url="https://example.com",
            path="/data",
        )
        self.assertEqual(result, {"ok": True})

    @patch("psa_platform.http.urlopen")
    def test_http_error_does_not_leak_query_secret(self, urlopen) -> None:
        urlopen.side_effect = HTTPError(
            "https://example.com/data?api_key=supersecret",
            403,
            "Forbidden",
            Message(),
            BytesIO(),
        )
        with self.assertRaises(ProviderError) as raised:
            UrllibJsonTransport().get_json(
                base_url="https://example.com",
                path="/data",
                params={"api_key": "supersecret"},
            )
        self.assertNotIn("supersecret", str(raised.exception))

    @patch("psa_platform.http.urlopen")
    def test_rejects_non_json(self, urlopen) -> None:
        urlopen.return_value = _Response(b"not-json")
        with self.assertRaises(ResponseValidationError):
            UrllibJsonTransport().get_json(
                base_url="https://example.com",
                path="/data",
            )

