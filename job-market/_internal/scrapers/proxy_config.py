#!/usr/bin/env python3
"""Shared proxy configuration for the job-market pipeline.

Uses the same proxy as the fetch-youtube skill: DataImpulse credentials
from ``~/.config/youtube/.env`` (or ``DATAIMPULSE_*`` env vars), with the
legacy Oxylabs settings as a fallback. DataImpulse takes precedence when
both are configured — the same rule as
``~/.agents/skills/fetch-youtube/youtube.py``.

Credentials are resolved in this order (first win, never overwritten):
  1. Already-exported environment variables / project ``.env``
  2. ``~/.config/youtube/.env`` (the youtube skill's machine-local config)

The proxy URL is built in memory and never printed; use
``masked_proxy_url()`` for safe logging.
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from urllib.parse import quote

from dotenv import load_dotenv

load_dotenv()  # project .env, found by walking up from cwd
load_dotenv(Path.home() / ".config" / "youtube" / ".env", override=False)


def _dataimpulse_endpoint() -> str:
    """Resolve the DataImpulse host:port."""
    endpoint = os.environ.get("DATAIMPULSE_ENDPOINT")
    if not endpoint:
        host = os.environ.get("DATAIMPULSE_HOST", "gw.dataimpulse.com")
        port = os.environ.get("DATAIMPULSE_PORT", "823")
        endpoint = f"{host}:{port}"
    return endpoint.removeprefix("http://").removeprefix("https://").rstrip("/")


def _build_dataimpulse_proxy_url() -> str | None:
    """Build a DataImpulse proxy URL from environment variables."""
    user = os.environ.get("DATAIMPULSE_USER")
    password = os.environ.get("DATAIMPULSE_PASSWORD")
    configured = any(
        os.environ.get(name)
        for name in (
            "DATAIMPULSE_USER",
            "DATAIMPULSE_PASSWORD",
            "DATAIMPULSE_ENDPOINT",
            "DATAIMPULSE_HOST",
            "DATAIMPULSE_PORT",
        )
    )
    if not configured:
        return None
    if not user or not password:
        raise ValueError(
            "DATAIMPULSE_USER and DATAIMPULSE_PASSWORD must be set together"
        )
    return (
        f"http://{quote(user, safe='')}:{quote(password, safe='')}@{_dataimpulse_endpoint()}"
    )


def _build_oxylabs_proxy_url() -> str | None:
    """Build an Oxylabs proxy URL from env vars (fallback)."""
    user = os.environ.get("OXYLABS_USER")
    endpoint = os.environ.get("OXYLABS_ENDPOINT")
    password = os.environ.get("OXYLABS_PASSWORD")
    if not user or not endpoint or not password:
        return None
    username = f"customer-{user}"
    return f"http://{username}:{quote(password, safe='')}@{endpoint}"


def get_proxy_url() -> str | None:
    """Return the configured proxy URL, preferring DataImpulse over Oxylabs."""
    return _build_dataimpulse_proxy_url() or _build_oxylabs_proxy_url()


def proxy_provider() -> str | None:
    """Return 'dataimpulse', 'oxylabs', or None when no proxy is configured."""
    if _build_dataimpulse_proxy_url():
        return "dataimpulse"
    if _build_oxylabs_proxy_url():
        return "oxylabs"
    return None


def masked_proxy_url() -> str | None:
    """Return the proxy URL with the password redacted, safe for logging."""
    url = get_proxy_url()
    if not url:
        return None
    try:
        scheme, rest = url.split("://", 1)
        creds, endpoint = rest.rsplit("@", 1)
        user, _ = creds.split(":", 1)
        return f"{scheme}://{user}:***@{endpoint}"
    except ValueError:
        return "***"


def get_requests_proxies() -> dict | None:
    """Return a ``requests``-compatible proxies dict, or None for direct."""
    url = get_proxy_url()
    if not url:
        return None
    return {"http": url, "https": url}


def get_playwright_proxy() -> dict | None:
    """Return a Playwright ``launch(proxy=...)`` dict, or None for direct."""
    provider = proxy_provider()
    if provider == "dataimpulse":
        return {
            "server": f"http://{_dataimpulse_endpoint()}",
            "username": os.environ.get("DATAIMPULSE_USER"),
            "password": os.environ.get("DATAIMPULSE_PASSWORD"),
        }
    if provider == "oxylabs":
        # Preserve the historic per-launch sticky session suffix.
        return {
            "server": f"http://{os.environ.get('OXYLABS_ENDPOINT')}",
            "username": (
                f"customer-{os.environ.get('OXYLABS_USER')}"
                f"-sessid-{int(time.time())}-sesstime-10"
            ),
            "password": os.environ.get("OXYLABS_PASSWORD"),
        }
    return None
