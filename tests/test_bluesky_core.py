import unittest
from unittest.mock import MagicMock, patch
from bluesky_social.bluesky_core import detect_hashtags, post, list_unanswered_responses

class TestBlueSkyCore(unittest.TestCase):

    def test_detect_hashtags(self):
        text = "Hello #BlueSky and #Python"
        facets = detect_hashtags(text)
        self.assertEqual(len(facets), 2)
        self.assertEqual(facets[0]["features"][0]["tag"], "BlueSky")
        self.assertEqual(facets[1]["features"][0]["tag"], "Python")

    @patch("bluesky_social.bluesky_core.Client")
    def test_post_without_image(self, mock_client_class):
        fake_client = MagicMock()
        fake_client.get_current_time_iso.return_value = "2023-10-01T00:00:00Z"
        fake_client.me.did = "did:example:123"
        fake_client.app.bsky.feed.post.create = MagicMock()

        post(fake_client, "Test post")
        fake_client.app.bsky.feed.post.create.assert_called()

    @patch("bluesky_social.bluesky_core.Client")
    def test_list_unanswered_responses(self, mock_client_class):
        fake_client = MagicMock()
        fake_notification = MagicMock()
        fake_notification.reason = "reply"
        fake_notification.cid = "cid-1"
        fake_notification.uri = "uri-1"
        fake_notification.author.handle = "user1"
        fake_notification.record.text = "Test reply"

        fake_client.app.bsky.notification.list_notifications.return_value.notifications = [fake_notification]
        fake_client.app.bsky.feed.get_post_thread.return_value.thread.replies = []

        responses = list_unanswered_responses(fake_client)
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0]["cid"], "cid-1")

if __name__ == "__main__":
    unittest.main()
