"""Errors exposed by the provider layer."""


class PSAError(Exception):
    """Base exception for the PSA package."""


class ConfigurationError(PSAError):
    """Required local configuration is missing or invalid."""


class ProviderError(PSAError):
    """A provider request failed or returned an invalid response."""


class ResponseValidationError(ProviderError):
    """A provider response did not satisfy the expected data contract."""

