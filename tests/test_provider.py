from pact import Verifier
from yarl import URL

PROVIDER_URL = URL("http://localhost:8081")


def test_against_broker(broker: URL, verifier: Verifier, provider_url: URL) -> None:
    code, _ = verifier.verify_with_broker(
        broker_url=str(broker),
        broker_username=broker.user,
        broker_password=broker.password,
        publish_version="0.0.1",
        publish_verification_results=True,
        provider_states_setup_url=str(provider_url / "_pact" / "provider_states"),
    )

    assert code == 0
