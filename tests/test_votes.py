import pytest
from app import models

@pytest.fixture()
def post_vote_already(create_test_posts, session, create_test_user):
    voted_post = models.Vote(post_id=create_test_posts[3].id, user_id=create_test_user['id'])
    session.add(voted_post)
    session.commit()


def test_vote_on_post(create_authorized_test_client, create_test_posts):
    response = create_authorized_test_client.post("/vote/", json={"post_id": create_test_posts[0].id, "dir": 1})
    assert response.status_code == 201

def test_vote_twice_post(create_authorized_test_client, create_test_posts, post_vote_already):
    response = create_authorized_test_client.post("/vote/", json={"post_id": create_test_posts[3].id, "dir": 1})
    assert response.status_code == 409

def test_delete_vote(create_authorized_test_client, create_test_posts):
    response = create_authorized_test_client.post("/vote/", json={"post_id": create_test_posts[3].id, "dir": 0})
    assert response.status_code == 404

def test_vote_post_not_exist(create_authorized_test_client):
    response = create_authorized_test_client.post("/vote/", json={"post_id": 99999, "dir": 1})
    assert response.status_code == 404

def test_vote_no_log_user(client, create_test_posts):
    response = client.post("/vote/", json={"post_id": create_test_posts[3].id, "dir": 1})
    assert response.status_code == 401