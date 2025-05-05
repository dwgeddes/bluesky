"""
Core functionality for BlueSky social media platform.
Provides utilities for posting, handling hashtags, and managing responses.
"""

from typing import List, Optional, Dict, Any, TypedDict
import os
import re
import logging

from atproto import Client, models
from atproto.exceptions import AtProtocolError

from .auth import get_credentials, clear_credentials, authenticate_bluesky
from .image_utils import convert_to_jpeg
from .notifications import get_notifications, get_responses, list_posts_and_responses, list_unanswered_responses

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

DEFAULT_USERNAME = "jetsetjaxon.bsky.social"
MAX_POST_LENGTH = 300  # BlueSky post character limit

class ReplyRef(TypedDict):
    uri: str
    cid: str

class ResponseInfo(TypedDict):
    cid: str
    uri: str
    author: str
    text: str

def detect_hashtags(text: str) -> List[Dict[str, Any]]:
    """
    Detect hashtags in text and return formatted facets for BlueSky API.
    
    Args:
        text: The text to search for hashtags
        
    Returns:
        List of facet objects ready for the BlueSky API
    """
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
    """
    Post text and optionally an image to BlueSky.
    
    Args:
        client: Authenticated BlueSky client
        text: The text content of the post
        image_path: Optional path to an image file
        alt_text: Alternative text for the image
        reply_to: Optional reference to a post to reply to
        
    Raises:
        ValueError: If the post text exceeds character limits
        FileNotFoundError: If the image file cannot be found
        Exception: For any other posting errors
    """
    try:
        if len(text) > MAX_POST_LENGTH:
            raise ValueError(f"Text exceeds the maximum allowed length of {MAX_POST_LENGTH} characters.")
        
        embed = None
        if image_path:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")
                
            if os.path.getsize(image_path) > 1_000_000:  # 1MB
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
        
    except ValueError as e:
        logging.error(e, exc_info=True)
        print(e)
    except FileNotFoundError as e:
        logging.error(e, exc_info=True)
        print(e)
    except Exception as e:
        logging.error(f"Post error: {e}", exc_info=True)
        print(f"Post error: {e}")
