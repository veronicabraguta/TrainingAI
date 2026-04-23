import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_create_post():
    payload = {
        "title": "QA test",
        "body": "learning API testing",
        "userId": 1
    }

    response = requests.post(f"{BASE_URL}/posts", json=payload)

    # 1) status code
    assert response.status_code == 201

    # 2) body -> json
    data = response.json()

    # 3) validări pe câmpuri
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]

    # 4) serverul a generat un id
    assert "id" in data