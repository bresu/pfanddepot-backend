def test_stats_empty_database(client):
    response = client.get("/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["total_items"] == 0
    assert data["total_cents"] == 0
    assert data["total_euros"] == 0

def test_stats_with_scans(client):
    client.post("/scans", json={"barcode": "123", "source": "test"})
    client.post("/scans", json={"barcode": "456"})

    response = client.get("/stats")

    assert response.status_code == 200

    data = response.json()

    assert data["total_items"] == 2
    assert data["total_cents"] == 50
    assert data["total_euros"] == 0.5