import unittest
from unittest.mock import MagicMock, patch
from bluesky_core import detect_hashtags, convert_to_jpeg, post, get_notifications, list_unanswered_responses, ReplyRef

class TestBlueSkyCore(unittest.TestCase):

    def test_detect_hashtags(self):
        text = "Hello #BlueSky and #Python"
        facets = detect_hashtags(text)
        self.assertEqual(len(facets), 2)
        self.assertIn("BlueSky", facets[0]["features"][0]["tag"])
        self.assertIn("Python", facets[1]["features"][0]["tag"])

    @patch("bluesky_core.Image.open")
    def test_convert_to_jpeg(self, mock_open):
        # Setup a fake image object with a convert and save method
        fake_image = MagicMock()
        mock_open.return_value = fake_image
        fake_image.convert.return_value = fake_image
        fake_image.save.return_value = None
        
        jpeg_path = convert_to_jpeg("test.png")
        self.assertTrue(jpeg_path.endswith(".jpeg"))
        fake_image.convert.assert_called_with("RGB")
        fake_image.save.assert_called()

    @patch("bluesky_core.Client")
    def test_post_without_image(self, mock_client_class):
        # Create a fake client with necessary attributes and methods
        fake_client = MagicMock()
        fake_client.get_current_time_iso.return_value = "2023-10-01T00:00:00Z"
        fake_client.me.did = "did:example:123"
        # Set up fake methods on nested attributes as needed
        fake_client.upload_blob.return_value.blob = "fake_blob"
        fake_client.app.bsky.feed.post.create = MagicMock()

        # Call post with text only
        post(fake_client, "Test post")
        fake_client.app.bsky.feed.post.create.assert_called()

    @patch("bluesky_core.Client")
    def test_list_unanswered_responses(self, mock_client_class):
        fake_client = MagicMock()
        # Create fake notifications, with one reply notification that has no replies
        fake_notification = MagicMock()
        fake_notification.reason = "reply"
        fake_notification.cid = "cid-1"
        fake_notification.uri = "uri-1"
        fake_notification.author.handle = "user1"
        fake_record = MagicMock()
        fake_record.text = "Test reply"
        fake_notification.record = fake_record

        fake_client.app.bsky.notification.list_notifications.return_value.notifications = [fake_notification]

        # Simulate thread with no replies
        fake_thread = MagicMock()
        type(fake_thread.thread).replies = property(lambda self: [])
        fake_client.app.bsky.feed.get_post_thread.return_value = fake_thread

        responses = list_unanswered_responses(fake_client)
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0]["cid"], "cid-1")

if __name__ == "__main__":
    unittest.main()
