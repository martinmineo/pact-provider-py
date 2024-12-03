import os
import time
from multiprocessing import Process
from typing import Generator, Any
from unittest.mock import MagicMock

import pytest
from dotenv import load_dotenv
from flask import request
from pact import Verifier
from yarl import URL

from src.provider import app, User

PROVIDER_URL = URL("http://localhost:8081")


@pytest.fixture(scope="session")
def broker() -> Generator[URL, Any, None]:
    load_dotenv()
    broker_url: str = os.getenv("BROKER_URL")
    yield URL(broker_url)
    return


@pytest.fixture(scope="session")
def provider_url() -> URL:
    return PROVIDER_URL


@app.route("/_pact/provider_states", methods=["POST"])
async def mock_pact_provider_states() -> dict[str, str] | tuple[dict[str, None], int]:
    if not request.is_json:
        return {"result": None}, 400  # Bad Request
    if request.json is None:
        msg = "Request must be JSON"
        raise ValueError(msg)
    state: str = request.json.get("state")
    mapping = {
        "user_1_exists": mock_user_1_exists
    }
    if state in mapping:
        mapping[state]()
        return {"result": "success"}
    return {"result": None}, 400


@pytest.fixture(scope="module")
def verifier() -> Generator[Verifier, Any, None]:
    proc = Process(target=run_server, daemon=True)
    verifier = Verifier(
        provider="pact-provider-py",
        provider_base_url=str(PROVIDER_URL),
    )
    proc.start()
    time.sleep(2)
    yield verifier
    proc.kill()


def run_server() -> None:
    app.run(
        host=PROVIDER_URL.host,
        port=PROVIDER_URL.port,
    )


def mock_user_1_exists() -> None:
    import src.provider

    src.provider.FAKE_DB = MagicMock()
    src.provider.FAKE_DB.get.return_value = User(
        id=1,
        name="Alice",
        email="alice@mail.com",
        age=78
    )
    print(src.provider.FAKE_DB)
