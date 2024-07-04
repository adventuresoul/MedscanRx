import pytest
import requests

BASE_URL = "http://localhost:8000"

def get_access_token(email, password):
    response = requests.post(f"{BASE_URL}/auth/login", data = {"email": email, "password": password})
    return response.json().get("access_token")

@pytest.fixture
def auth_token():
    email = "admin@admin.com"
    password = "admin@2003"
    return get_access_token(email, password)

def test_upload_file(auth_token):
    url = f"{BASE_URL}/ocr/files"
    headers = {"Authorization": f"Bearer {auth_token}"}
    files = {"file": open("test_image.jpg", "rb")}
    
    response = requests.post(url, headers=headers, files=files) 
    
    assert response.status_code == 202
    json_response = response.json()
    assert "file_id" in json_response
    assert "file_name" in json_response

def test_get_text_from_image(auth_token):
    file_id = "78c18035-f18c-4a84-8157-46070e40cb96"
    url = f"{BASE_URL}/ocr/files/{file_id}/text"
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = requests.post(url, headers=headers)
    
    assert response.status_code == 200
    json_response = response.json()
    assert "Effects" in json_response

def test_get_users(auth_token):
    url = f"{BASE_URL}/users"
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response, list)

def test_create_user():
    url = f"{BASE_URL}/users"
    data = {
        "username": "new_user",
        "email": "new_user@example.com",
        "contact": "1234567890",
        "password": "password123"
    }
    
    response = requests.post(url, data=data)
    
    assert response.status_code == 201
    json_response = response.json()
    assert "message" in json_response

# def test_delete_user(auth_token):
#     url = f"{BASE_URL}/users"
#     headers = {"Authorization": f"Bearer {auth_token}"}
#     data = {"email": "user_user@example.com"}
    
#     response = requests.delete(url, headers=headers, data=data)
    
#     assert response.status_code == 200
#     json_response = response.json()
#     assert "message" in json_response

def test_check_user_existence():
    url = f"{BASE_URL}/users/check-existance"
    data = {"email": "admin@admin.com"}
    
    response = requests.post(url, data=data)
    
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response

def test_update_user_profile(auth_token):
    url = f"{BASE_URL}/users/me"
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {
        "username": "admin",
        "new_email": "admin@admin.com",
        "new_contact": "7975963827",
        "new_password": "admin@2003#"
    }
    
    response = requests.put(url, headers=headers, data=data)
    
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response

def test_reset_password():
    url = f"{BASE_URL}/users/reset-password"
    data = {
        "email": "admin@admin.com",
        "new_password": "admin@2003"
    }
    
    response = requests.post(url, data=data)
    
    assert response.status_code == 200
    json_response = response.json()
    assert "message" in json_response

