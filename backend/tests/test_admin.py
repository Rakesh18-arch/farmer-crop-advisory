def test_admin_stats_authorized(client, admin_headers):
    """Admin should be able to view system metrics and stats."""
    res = client.get("/api/admin/stats", headers=admin_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "metrics" in data
    assert "total_farmers" in data["metrics"]
    assert "popular_crops" in data

def test_admin_stats_unauthorized_farmer(client, auth_headers):
    """Normal farmers must be forbidden (403) from accessing admin metrics."""
    res = client.get("/api/admin/stats", headers=auth_headers)
    assert res.status_code == 403
    data = res.get_json()
    assert data["success"] is False

def test_admin_farmers_list(client, admin_headers, auth_headers):
    """Admin can query paginated list of registered farmers."""
    res = client.get("/api/admin/farmers?page=1&per_page=10", headers=admin_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "farmers" in data
    assert data["total"] >= 1

def test_admin_reports_csv_streaming(client, admin_headers):
    """Admin can export streaming CSV reports."""
    res = client.get("/api/admin/reports/farmers", headers=admin_headers)
    assert res.status_code == 200
    assert "text/csv" in res.content_type
    assert "User ID,Full Name,Email" in res.data.decode("utf-8")

def test_admin_reports_invalid_type(client, admin_headers):
    """Invalid report type yields 400 Bad Request."""
    res = client.get("/api/admin/reports/unsupported_report", headers=admin_headers)
    assert res.status_code == 400
    data = res.get_json()
    assert data["success"] is False

def test_toggle_farmer_status(client, admin_headers, auth_headers):
    """Admin can deactivate and reactivate farmer accounts."""
    farmers_res = client.get("/api/admin/farmers", headers=admin_headers)
    farmer_id = farmers_res.get_json()["farmers"][0]["id"]
    res = client.put(f"/api/admin/farmers/{farmer_id}/toggle-status", headers=admin_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "is_active" in data
