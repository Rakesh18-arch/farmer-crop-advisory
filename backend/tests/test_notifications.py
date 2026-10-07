def test_get_notifications(client, auth_headers):
    """Authenticated farmer can fetch in-app notifications."""
    res = client.get("/api/notifications", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "unread_count" in data
    assert "notifications" in data

def test_mark_all_notifications_read(client, auth_headers):
    """Authenticated farmer can bulk-mark notifications as read."""
    res = client.put("/api/notifications/mark-all-read", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
