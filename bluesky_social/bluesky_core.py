"""
Core functionality for BlueSky.
"""

from typing import List, Optional, Dict, Any, TypedDict
import os, re, logging
from PIL import Image
from atproto import Client, models
from atproto.exceptions import AtProtocolError
import keyring
from bluesky_social.auth import get_credentials, clear_credentials, authenticate_bluesky
from bluesky_social.image_utils import convert_to_jpeg
from bluesky_social.notifications import get_notifications, get_responses, list_posts_and_responses, list_unanswered_responses

# ...existing configuration, logging, etc...
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

username = "jetsetjaxon.bsky.social"

class ReplyRef(TypedDict):
    uri: str
    cid: str

class ResponseInfo(TypedDict):
    cid: str
    uri: str
    author: str
    text: str

def detect_hashtags(text: str) -> List[Dict[str, Any]]:
    # ...existing code...
    char_to_byte = [0]
    for char in text:
        char_to_byte.append(char_to_byte[-1] + len(char.encode('utf-8')))
    facets = []
    for m in re.finditer(r"#\w+", text):
        start, end = m.start(), m.end()
        facets.append({
            "index": {"byteStart": char_to_byte[start], "byteEnd": char_to_byte[end]},
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": m.group()[1:]}]
        })
    return facets

def post(client: Client, text: str, image_path: Optional[str] = None, alt_text: str = "Image", 
         reply_to: Optional[ReplyRef] = None) -> None:
    try:
        embed = None
        if image_path:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
            if os.path.getsize(image_path) > 1_000_000:
                image_path = convert_to_jpeg(image_path)
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
            upload = client.upload_blob(image_data)
            image_ref = models.AppBskyEmbedImages.Image(alt=alt_text, image=upload.blob)
            embed = models.AppBskyEmbedImages.Main(images=[image_ref])
        facets = detect_hashtags(text)
        post_record = models.AppBskyFeedPost.Record(
            text=text,
            embed=embed,
            facets=facets,
            created_at=client.get_current_time_iso()
        )
        if reply_to:
            post_record.reply = models.AppBskyFeedPost.ReplyRef(
                parent=models.ComAtprotoRepoStrongRef.Main(uri=reply_to['uri'], cid=reply_to['cid']),
                root=models.ComAtprotoRepoStrongRef.Main(uri=reply_to['uri'], cid=reply_to['cid'])
            )
        client.app.bsky.feed.post.create(client.me.did, post_record)
        print("Post successfully published!")
    except FileNotFoundError as e:
        logging.error(e, exc_info=True)
        print(e)
    except Exception as e:
        logging.error(f"Post error: {e}", exc_info=True)
        print(f"Post error: {e}")
