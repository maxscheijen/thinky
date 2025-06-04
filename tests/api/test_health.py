from fastapi.testclient import TestClient

from thinky.api.main import create_app

app = create_app()
client = TestClient(app)


def test_health():
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
