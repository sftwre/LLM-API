def test_create_session(test_client):

    # pass valid input
    response = test_client.get("/", params={"username": "Isaac"})
    assert response.status_code == 200
    assert "session_id" in response.json()
    assert "message" in response.json()

    # pass invalid input
    response = test_client.get("/")
    assert response.status_code == 422


def test_chat_completion(test_client):
    session_id = test_client.get("/", params={"username": "Isaac"}).json()["session_id"]

    # test valid session
    response = test_client.put(
        f"/chat/{session_id}", json={"payload": "Hello, what is your name?"}
    )
    assert response.status_code == 200

    # test invalid session
    response = test_client.put(
        "/chat/1234", json={"payload": "Hello, what is your name?"}
    )
    assert response.status_code == 404

    # test invalid input with no payload
    response = test_client.put(f"/chat/{session_id}", json={})
    assert response.status_code == 422


def test_chat_history(test_client):
    session_id = test_client.get("/", params={"username": "Isaac"}).json()["session_id"]

    # check empty chats with no sent messages
    response = test_client.get(f"/chat_history/{session_id}")
    assert response.status_code == 200

    response_dict = response.json()

    assert "payload" in response_dict and "" == response_dict["payload"]
    assert "session_id" in response_dict and session_id == response_dict["session_id"]
    assert "username" in response_dict and "Isaac" == response_dict["username"]
    assert (
        "message_history" in response_dict
        and len(response_dict["message_history"]) == 0
    )

    # pass invalid session id
    response = test_client.get(f"/chat_history/1234")
    assert response.status_code == 404

    # pass multiple payloads and check that they're present in chat history along with AI response
    payloads = [
        "Hello, what is your name?",
        "Please tell me a joke!",
        "Tell me something interesting about the show Seinfeld.",
    ]

    for payload in payloads:
        test_client.put(f"/chat/{session_id}", json={"payload": payload})

    response = test_client.get(f"/chat_history/{session_id}")
    assert response.status_code == 200

    message_history = response.json()["message_history"]
    assert len(message_history) == (len(payloads) * 2)
    assert message_history[0]["content"] == payloads[0]
    assert message_history[2]["content"] == payloads[1]
    assert message_history[4]["content"] == payloads[2]
