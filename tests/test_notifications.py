import pytest
from bluesky_social.notifications import get_notifications, get_responses, list_posts_and_responses, list_unanswered_responses

class DummyNotification:
    def __init__(self, author, reason, cid, uri, text):
        self.author = type("obj", (), {"handle": author})
        self.reason = reason
        self.cid = cid
        self.uri = uri
        self.record = type("obj", (), {"text": text})

class DummyReply:
    def __init__(self, text, author, cid, uri):
        self.post = type("obj", (), {
            "record": type("obj", (), {"text": text}),
            "author": type("obj", (), {"handle": author}),
            "cid": cid,
            "uri": uri
        })

class DummyThread:
    def __init__(self, replies):
        self.thread = type("obj", (), {"replies": replies})

class DummyClient:
    def __init__(self):
        self.me = type("obj", (), {"handle": "dummy_handle", "did": "dummy_did"})
        # Dummy notification list and feed logic
        def list_notifications():
            return type("obj", (), {"notifications": [
                DummyNotification("user1", "info", "cid1", "uri1", "text1"),
                DummyNotification("user2", "reply", "cid2", "uri2", "text2")
            ]})
        def get_post_thread(query):
            # Simulate thread with one reply for a given post uri
            reply = DummyReply("reply text", "user3", "cid3", "uri3")
            return DummyThread([reply])
        def get_author_feed(query):
            post = type("obj", (), {
                "post": type("obj", (), {"record": type("obj", (), {"text": "post text"}), "uri": "uri_post"}),
                "reply_count": 1
            })
            return type("obj", (), {"feed": [post]})
        self.app = type("obj", (), {}) 
        self.app.bsky = type("obj", (), {}) 
        self.app.bsky.notification = type("obj", (), {"list_notifications": list_notifications})
        self.app.bsky.feed = type("obj", (), {
            "get_post_thread": get_post_thread,
            "get_author_feed": get_author_feed
        })

def test_get_notifications(capsys):
    client = DummyClient()
    get_notifications(client)
    captured = capsys.readouterr().out
    assert "Notification" in captured

def test_get_responses():
    client = DummyClient()
    responses = get_responses(client, "uri_test")
    assert responses[0]["text"] == "reply text"

def test_list_posts_and_responses(capsys):
    client = DummyClient()
    list_posts_and_responses(client)
    captured = capsys.readouterr().out
    assert "post text" in captured

def test_list_unanswered_responses():
    client = DummyClient()
    responses = list_unanswered_responses(client)
    assert isinstance(responses, list)
