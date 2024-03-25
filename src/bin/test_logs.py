from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_delete_logs_no_file():
    """
    Method to test when we try to delete a file not existing
    """
    response = client.delete("/logs")
    assert response.status_code == 404
    assert response.json() == {"detail": "No data available for this delete."}


def test_post_single_json():
    """
    Method to insert our example json single.json
    """
    file_path = "examples/single.json"
    with open(file_path, "rb") as file:
        response = client.post("/logs", files={"file": ("single.json", file, "application/json")},
                               data={"log_format": "JSON"})
        assert response.status_code == 200
        assert response.json() == {"message": "File inserted."}


def test_post_multi_json():
    """
    Method to insert our example json multi.json
    """
    file_path = "examples/multi.json"
    with open(file_path, "rb") as file:
        response = client.post("/logs", files={"file": ("multi.json", file, "application/json")},
                               data={"log_format": "JSON"})
        assert response.status_code == 200
        assert response.json() == {"message": "File inserted."}


def test_post_single_yml():
    """
    Method to insert our example yaml solo.yml
    """
    file_path = "examples/single.yml"
    with open(file_path, "rb") as file:
        response = client.post("/logs", files={"file": ("single.yml", file, "application/yaml")},
                               data={"log_format": "YML"})
        assert response.status_code == 200
        assert response.json() == {"message": "File inserted."}


def test_post_multi_yml():
    """
    Method to insert our example yaml multi.yml
    """
    file_path = "examples/multi.yml"
    with open(file_path, "rb") as file:
        response = client.post("/logs", files={"file": ("multi.yml", file, "application/yaml")},
                               data={"log_format": "YML"})
        assert response.status_code == 200
        assert response.json() == {"message": "File inserted."}


def test_post_wrong_format():
    """
    Method to test our API able to do not accept other format for the post method
    """
    file_path = "examples/multi.log"
    with open(file_path, "rb") as file:
        response = client.post("/logs", files={"file": ("multi.log", file, "application/log")},
                               data={"log_format": "JSON"})
        assert response.status_code == 400
        assert response.json() == {"message": "Invalid file format."}


def test_get_all_logs():
    """
    Method to  test our get without filter
    """
    response = client.request(method="GET", url="/logs", json={"log_format": "JSON"})
    assert response.status_code == 200
    assert len(response.json()) == 8


def test_get_logs_filter_before_time():
    """
    Method to  test our get with before time filter
    """
    response = client.request(method="GET", url="/logs", json={"log_format": "JSON",
                                                               "before_time": "2011-11-04 00:00:00"})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_logs_filter_after_time():
    """
    Method to  test our get with after time filter
    """
    response = client.request(method="GET", url="/logs", json={"log_format": "JSON",
                                                               "after_time": "2011-11-04 00:00:00"})
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_get_logs_filter_single_type():
    """
    Method to  test our get with one type filter
    """
    response = client.request(method="GET", url="/logs", json={"log_format": "JSON",
                                                               "type": ["c2"]})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_logs_filter_multi_type():
    """
    Method to  test our get with multi types filter
    """
    response = client.request(method="GET", url="/logs", json={"log_format": "JSON",
                                                               "type": ["c2", "phishing"]})
    assert response.status_code == 200
    assert len(response.json()) == 6


def test_get_logs_filter_ip_private():
    """
    Method to  test our get with ip filter at private
    """
    response = client.request(method="GET", url="/logs", json={"log_format": "JSON",
                                                               "ip": "private"})
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_get_logs_filter_ip_public():
    """
    Method to  test our get with ip filter at public
    """
    response = client.request(method="GET", url="/logs", json={"log_format": "JSON",
                                                               "ip": "public"})
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_delete_logs():
    """
    Method to  test our delete API
    """
    response = client.delete("/logs")
    assert response.status_code == 200
    assert response.json()["message"] == "Lines removed from the data folder."
    assert response.json()["count"] == 8


def test_get_no_logs():
    """
    Method to  test our GET API without Logs in the file
    """
    response = client.request(method="GET", url="/logs", json={"log_format": "JSON"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Data not available"}
