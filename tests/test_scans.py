def test_create_scan(client):
    response = client.post(
        "/scans",
        json={
            "barcode": "9002490100070",
            "source": "test-client",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["barcode"] == "9002490100070"
    assert data["source"] == "test-client"
    assert data["deposit_cents"] == 25
    assert "id" in data
    assert "scanned_at" in data


def test_list_scans_starts_empty(client):
    response = client.get("/scans")

    assert response.status_code == 200
    assert response.json() == []


def test_list_scans_after_create(client):
    client.post(
        "/scans",
        json={
            "barcode": "9002490100070",
            "source": "test-client",
        },
    )

    response = client.get("/scans")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["barcode"] == "9002490100070"

def test_delete_scan(client):
    # Create a scan to delete
    response = client.post(
        "/scans",
        json={
            "barcode": "9002490100070",
            "source": "test-client",
        },
    )
    scan_id = response.json()["id"]

    # Delete the scan
    delete_response = client.delete(f"/scans/{scan_id}")
    assert delete_response.status_code == 204

    # Verify the scan is deleted
    get_response = client.get("/scans")
    assert get_response.status_code == 200
    assert all(scan["id"] != scan_id for scan in get_response.json())

def test_delete_nonexistent_scan(client):
    response = client.delete("/scans/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Scan not found"}
    