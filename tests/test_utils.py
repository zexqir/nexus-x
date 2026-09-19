from nexus.utils import redact_secret
def test_redaction():
    assert "*" in redact_secret("AKIA1234567890123456")
    assert redact_secret("") == ""
