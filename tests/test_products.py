def test_create_product_with_minimal_data(client):
    response = client.post(
        "/products",
        json={
            "barcode": "9001234567890",
            "name": "Test Bottle",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["barcode"] == "9001234567890"
    assert data["name"] == "Test Bottle"
    assert data["brand"] is None
    assert data["is_returnable"] is True
    assert data["return_locations"] is None
    assert data["thumbnail_url"] is None
    assert data["deposit_cents"] == 25
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_create_product_with_full_data(client):
    response = client.post(
        "/products",
        json={
            "barcode": "9009876543210",
            "name": "Vöslauer Mineralwasser 1.5L",
            "brand": "Vöslauer",
            "is_returnable": True,
            "return_locations": ["Billa", "Spar", "Hofer"],
            "thumbnail_url": "/static/bottle-thumbnails/9009876543210.jpg",
            "deposit_cents": 25,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["barcode"] == "9009876543210"
    assert data["name"] == "Vöslauer Mineralwasser 1.5L"
    assert data["brand"] == "Vöslauer"
    assert data["return_locations"] == ["Billa", "Spar", "Hofer"]
    assert data["thumbnail_url"] == "/static/bottle-thumbnails/9009876543210.jpg"
    assert data["deposit_cents"] == 25


def test_get_all_products(client):
    client.post(
        "/products",
        json={
            "barcode": "1111111111111",
            "name": "Bottle A",
        },
    )

    client.post(
        "/products",
        json={
            "barcode": "2222222222222",
            "name": "Bottle B",
        },
    )

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["barcode"] in ["1111111111111", "2222222222222"]
    assert data[1]["barcode"] in ["1111111111111", "2222222222222"]


def test_get_product_by_barcode(client):
    client.post(
        "/products",
        json={
            "barcode": "9001234567890",
            "name": "Test Bottle",
        },
    )

    response = client.get("/products/9001234567890")

    assert response.status_code == 200

    data = response.json()

    assert data["barcode"] == "9001234567890"
    assert data["name"] == "Test Bottle"


def test_get_product_returns_404_for_unknown_barcode(client):
    response = client.get("/products/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_create_product_fails_for_duplicate_barcode(client):
    payload = {
        "barcode": "9001234567890",
        "name": "Test Bottle",
    }

    first_response = client.post("/products", json=payload)
    second_response = client.post("/products", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Product with this barcode already exists"


def test_update_product(client):
    client.post(
        "/products",
        json={
            "barcode": "9001234567890",
            "name": "Old Name",
            "brand": "Old Brand",
        },
    )

    response = client.put(
        "/products/9001234567890",
        json={
            "name": "New Name",
            "brand": "New Brand",
            "return_locations": ["Billa", "Spar"],
            "deposit_cents": 30,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["barcode"] == "9001234567890"
    assert data["name"] == "New Name"
    assert data["brand"] == "New Brand"
    assert data["return_locations"] == ["Billa", "Spar"]
    assert data["deposit_cents"] == 30


def test_update_product_returns_404_for_unknown_barcode(client):
    response = client.put(
        "/products/does-not-exist",
        json={
            "name": "New Name",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


def test_delete_product(client):
    client.post(
        "/products",
        json={
            "barcode": "9001234567890",
            "name": "Test Bottle",
        },
    )

    delete_response = client.delete("/products/9001234567890")

    assert delete_response.status_code == 204

    get_response = client.get("/products/9001234567890")

    assert get_response.status_code == 404


def test_delete_product_returns_404_for_unknown_barcode(client):
    response = client.delete("/products/does-not-exist")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"