# future
from __future__ import annotations

# stdlib
from typing import Any
from typing import Union

# third party
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey
from nacl.signing import VerifyKey

# relative
from .base import SyftBaseModel
from .serializable import serializable

SIGNING_KEY_FOR = "SigningKey for"


@serializable()
class SyftVerifyKey(SyftBaseModel):
    verify_key: VerifyKey

    def __init__(self, verify_key: Union[str, VerifyKey]) -> None:
        if isinstance(verify_key, str):
            verify_key = VerifyKey(bytes.fromhex(verify_key))
        super().__init__(verify_key=verify_key)

    def __str__(self) -> str:
        return self.verify_key.encode(encoder=HexEncoder).decode("utf-8")

    @staticmethod
    def from_string(key_str: str) -> SyftVerifyKey:
        return SyftVerifyKey(verify_key=VerifyKey(bytes.fromhex(key_str)))

    @property
    def verify(self) -> str:
        return str(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SyftVerifyKey):
            return False
        return self.verify_key == other.verify_key

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return self.verify_key.__hash__()


@serializable()
class SyftSigningKey(SyftBaseModel):
    signing_key: SigningKey

    def __init__(self, signing_key: Union[str, SigningKey]) -> None:
        if isinstance(signing_key, str):
            signing_key = SigningKey(bytes.fromhex(signing_key))
        super().__init__(signing_key=signing_key)

    @property
    def verify_key(self) -> SyftVerifyKey:
        return SyftVerifyKey(verify_key=self.signing_key.verify_key)

    def __str__(self) -> str:
        return self.signing_key.encode(encoder=HexEncoder).decode("utf-8")

    @staticmethod
    def generate() -> SyftSigningKey:
        return SyftSigningKey(signing_key=SigningKey.generate())

    @staticmethod
    def from_string(key_str: str) -> SyftSigningKey:
        return SyftSigningKey(signing_key=SigningKey(bytes.fromhex(key_str)))

    def __repr__(self) -> str:
        return f"<{SIGNING_KEY_FOR}: {self.verify}>"

    @property
    def verify(self) -> str:
        return str(self.verify_key)

    def __hash__(self) -> int:
        return self.signing_key.__hash__()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SyftSigningKey):
            return False
        return self.signing_key == other.signing_key


SyftCredentials = Union[SyftVerifyKey, SyftSigningKey]


@serializable()
class UserLoginCredentials(SyftBaseModel):
    email: str
    password: str
