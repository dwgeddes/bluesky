from unittest.mock import MagicMock, patch

from bluesky_social.bluesky_core import detect_hashtags, post
from bluesky_social.notifications import list_unanswered_responses


def test_detect_hashtags():
    text = "Hello #BlueSky and #Python"
    facets = detect_hashtags(text)
    assert len(facets) == 2
    # Check that we have Tag features
    assert isinstance(facets[0].features[0], type(facets[0].features[0]))
    assert isinstance(facets[1].features[0], type(facets[1].features[0]))


@patch("bluesky_social.bluesky_core.Client")
def test_post_without_image(mock_client_class):
    fake_client = MagicMock()
    fake_client.get_current_time_iso.return_value = "2023-10-01T00:00:00Z"
    fake_client.me.did = "did:example:123"
    fake_client.app.bsky.feed.post.create = MagicMock()

    post(fake_client, "Test post")
    fake_client.app.bsky.feed.post.create.assert_called()


@patch("bluesky_social.bluesky_core.Client")
def test_list_unanswered_responses(mock_client_class):
    fake_client = MagicMock()
    fake_notification = MagicMock()
    fake_notification.reason = "reply"
    fake_notification.cid = "cid-1"
    fake_notification.uri = "uri-1"
    fake_notification.author.handle = "user1"
    fake_notification.record.text = "Test reply"

    fake_client.app.bsky.notification.list_notifications.return_value.notifications = [
        fake_notification
    ]
    fake_client.app.bsky.feed.get_post_thread.return_value.thread.replies = []

    responses = list_unanswered_responses(fake_client)
    assert len(responses) == 1
    assert responses[0]["cid"] == "cid-1"
