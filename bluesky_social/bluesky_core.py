"""
Core functionality for BlueSky social media platform.
Provides utilities for posting, handling hashtags, and managing responses.
"""

import logging
import os
import re
from typing import Optional, TypedDict

from atproto import Client, models

from .config import MAX_IMAGE_SIZE, MAX_POST_LENGTH
from .image_utils import convert_to_jpeg


class ReplyRef(TypedDict):
    uri: str
    cid: str


class ResponseInfo(TypedDict):
    cid: str
    uri: str
    author: str
    text: str


def detect_hashtags(text: str) -> list[models.AppBskyRichtextFacet.Main]:
    """
    Detect hashtags in text and return formatted facets for BlueSky API.

    Args:
        text: The text to search for hashtags

    Returns:
        List of facet objects ready for the BlueSky API
    """
    char_to_byte = [0]
    for char in text:
        char_to_byte.append(char_to_byte[-1] + len(char.encode("utf-8")))

    facets = []
    for m in re.finditer(r"#\w+", text):
        start, end = m.start(), m.end()
        facet = models.AppBskyRichtextFacet.Main(
            index=models.AppBskyRichtextFacet.ByteSlice(
                byte_start=char_to_byte[start], byte_end=char_to_byte[end]
            ),
            features=[models.AppBskyRichtextFacet.Tag(tag=m.group()[1:])],
        )
        facets.append(facet)
    return facets


def post(
    client: Client,
    text: str,
    image_path: Optional[str] = None,
    alt_text: str = "Image",
    reply_to: Optional[ReplyRef] = None,
) -> None:
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
            raise ValueError(
                f"Text exceeds the maximum allowed length of {MAX_POST_LENGTH} characters."
            )

        embed = None
        if image_path:
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            if os.path.getsize(image_path) > MAX_IMAGE_SIZE:  # 1MB
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
            created_at=client.get_current_time_iso(),
        )

        if reply_to:
            post_record.reply = models.AppBskyFeedPost.ReplyRef(
                parent=models.ComAtprotoRepoStrongRef.Main(
                    uri=reply_to["uri"], cid=reply_to["cid"]
                ),
                root=models.ComAtprotoRepoStrongRef.Main(
                    uri=reply_to["uri"], cid=reply_to["cid"]
                ),
            )

        if not client.me:
            raise Exception("Client not authenticated. Please authenticate first.")

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
