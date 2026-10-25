from app.main import health_check


def test_health_check_returns_service_status() -> None:
    assert health_check() == {"status": "ok", "service": "researchflow-api"}
