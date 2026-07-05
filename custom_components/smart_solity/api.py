"""API client for the Solity cloud service."""

import asyncio
import base64
from dataclasses import dataclass
import hashlib
import json

from aiohttp import ClientError, ClientSession

BASE_URL = "https://www.smartsolity.com/api_v2"
REQUEST_TIMEOUT = 10


class SmartSolityError(Exception):
    """Base error for the smart_solity API client."""


class SmartSolityAuthError(SmartSolityError):
    """Raised when login, or a relogin attempt, fails."""


class SmartSolityApiError(SmartSolityError):
    """Raised when an authenticated call keeps failing after a successful relogin."""


class SmartSolityConnectionError(SmartSolityError):
    """Raised when the API cannot be reached."""


@dataclass
class SmartSolityDevice:
    """Static metadata for a Solity lock device."""

    device_id: str
    nickname: str
    maker_name: str
    model_name: str


@dataclass
class SmartSolityStatus:
    """Live status of a Solity lock device."""

    is_locked: bool
    battery: int


class SmartSolityApiClient:
    """Client for the smartsolity.com cloud API."""

    def __init__(self, session: ClientSession, password: str) -> None:
        """Initialize the client."""
        self._session = session
        self._password = password
        self._token: str | None = None

    async def login(self) -> None:
        """Log in and store the session token."""
        hashed_pwd = base64.b64encode(
            hashlib.sha256(self._password.encode()).digest()
        ).decode()
        payload = {
            "phoneToken": self._password,
            "hashedPwd": hashed_pwd,
            "appSource": "0",
            "emailId": self._password,
            "lang": "3",
        }
        data = await self._request("POST", "/login", payload)
        contents = data["contents"]
        if data["result"] != 0 or contents["loginResult"] != 0:
            raise SmartSolityAuthError(
                contents["loginMessage"] or "invalid credentials"
            )
        self._token = contents["token"]

    async def get_my_device(self) -> SmartSolityDevice:
        """Return the single lock device registered to this account."""
        data = await self._authorized_request("GET", "/myDevice")
        device = data["contents"]["myDeviceList"][0]
        return SmartSolityDevice(
            device_id=device["myDeviceId"],
            nickname=device["myDeviceNickName"],
            maker_name=device["myDeviceMakerName"],
            model_name=device["myDeviceModelName"],
        )

    async def get_status(self, device_id: str) -> SmartSolityStatus:
        """Return the current lock/battery status."""
        data = await self._authorized_request(
            "PUT",
            f"/controlDevice/{device_id}",
            {
                "lang": "3",
                "appSource": "0",
                "optionValue": "",
                "controlType": "get_status",
            },
        )
        message = json.loads(data["contents"]["controlDeviceMessage"])
        return SmartSolityStatus(
            is_locked=message["deadBolt"] == 1, battery=message["battery"]
        )

    async def lock(self, device_id: str) -> None:
        """Lock the device."""
        await self._authorized_request(
            "PUT",
            f"/controlDevice/{device_id}",
            {"lang": "3", "appSource": "0", "optionValue": "1", "controlType": "close"},
        )

    async def unlock(self, device_id: str) -> None:
        """Unlock the device."""
        await self._authorized_request(
            "PUT",
            f"/controlDevice/{device_id}",
            {"lang": "3", "appSource": "0", "optionValue": "1", "controlType": "open"},
        )

    async def _authorized_request(
        self, method: str, path: str, payload: dict[str, str] | None = None
    ) -> dict:
        """Make an authenticated request, retrying once after a fresh login."""
        if self._token is None:
            await self.login()
        data = await self._request(method, path, payload)
        if data["result"] != 0:
            await self.login()
            data = await self._request(method, path, payload)
            if data["result"] != 0:
                raise SmartSolityApiError(data["errorMessage"] or "request failed")
        return data

    async def _request(
        self, method: str, path: str, payload: dict[str, str] | None = None
    ) -> dict:
        """Make a single request to the API."""
        headers = {"Authorization": self._token} if self._token else {}
        try:
            async with asyncio.timeout(REQUEST_TIMEOUT):
                response = await self._session.request(
                    method, f"{BASE_URL}{path}", json=payload, headers=headers
                )
                return await response.json(content_type=None)
        except (TimeoutError, ClientError) as err:
            raise SmartSolityConnectionError(str(err)) from err
