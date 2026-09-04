from pact import Verifier


def test_provider_verification():
    verifier = (
        Verifier("OpenMeteo")
        .add_source("./pacts")
        .add_transport(url="http://localhost:5001")
    )

    verifier.verify()