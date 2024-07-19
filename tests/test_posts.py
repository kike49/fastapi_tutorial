import pytest
from app import schemas

# RETRIEVE POSTS
def test_get_all_posts(client, create_test_posts):
    response = client.get("/posts/")
    assert len(response.json()) == len(create_test_posts)
    assert response.status_code == 200

def test_get_one_posts(client, create_test_posts):
    response = client.get(f"/posts/{create_test_posts[0].id}")
    assert response.status_code == 200

def test_get_one_posts_not_exist(client):
    response = client.get("/posts/999999")
    assert response.status_code == 404

# CREATE POSTS
@pytest.mark.parametrize("title, content", [("new title", "new content"), ("new title2", "new content2"), ("new title3", "new content3")])
def test_create_post(create_authorized_test_client, create_test_user, title, content):
    response = create_authorized_test_client.post("/posts/", json={"title": title, "content": content})
    created_post = schemas.PostResponse(**response.json()) # Converts the JSON response body into a Python dictionary
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == True # Checks if default value is True
    assert created_post.owner_id == create_test_user['id']

def test_create_post_no_user(client):
    response = client.post("/posts/", json={"title": "title", "content": "content"})
    assert response.status_code == 401

# DELETE POSTS
def test_delete_post_no_user(client, create_test_posts):
    response = client.delete(f"/posts/{create_test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post(create_authorized_test_client, create_test_posts):
    response = create_authorized_test_client.delete(f"/posts/{create_test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_not_exist(create_authorized_test_client):
    response = create_authorized_test_client.delete(f"/posts/99999")
    assert response.status_code == 404

def test_delete_other_user_post(create_authorized_test_client, create_test_posts):
    response = create_authorized_test_client.delete(f"/posts/{create_test_posts[3].id}")
    assert response.status_code == 403

# UPDATE POSTS
def test_update_post(create_authorized_test_client, create_test_posts):
    data = {"title": "new title", "content": "updated content"}
    response = create_authorized_test_client.put(f"/posts/{create_test_posts[0].id}", json=data)
    assert response.status_code == 200
    assert create_test_posts[0].title == "new title"

def test_update_other_user_post(create_authorized_test_client, create_test_posts):
    data = {"title": "new title", "content": "updated content"}
    response = create_authorized_test_client.put(f"/posts/{create_test_posts[3].id}", json=data)
    assert response.status_code == 403

def test_no_logged_user_update_post(client, create_test_posts):
    response = client.put(f"/posts/{create_test_posts[0].id}")
    assert response.status_code == 401

def test_update_post_not_exist(create_authorized_test_client):
    data = {"title": "new title", "content": "updated content"}
    response = create_authorized_test_client.put("/posts/99999", json=data)
    assert response.status_code == 404