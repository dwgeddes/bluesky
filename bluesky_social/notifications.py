"""
Notifications module for the BlueSky social network.

This module provides utilities for fetching and managing BlueSky notifications 
and post responses.
"""
import logging
from typing import List, Dict, Any

def get_notifications(client) -> List[Dict[str, Any]]:
    """
    Fetch notifications from the BlueSky network.
    
    Args:
        client: An authenticated BlueSky client
        
    Returns:
        A list of notification information dictionaries
    """
    try:
        notifications = client.app.bsky.notification.list_notifications().notifications
        result = []
        for notification in notifications:
            info = {
                "author": getattr(notification.author, "handle", None),
                "reason": getattr(notification, "reason", None),
                "cid": getattr(notification, "cid", None),
                "uri": getattr(notification, "uri", None),
                "text": getattr(getattr(notification, "record", None), "text", None)
            }
            print(f"Notification from {info['author']}: {info['reason']}")
            result.append(info)
        return result
    except Exception as e:
        logging.error(f"Notifications error: {e}", exc_info=True)
        print(f"Notifications error: {e!r}")
        return []

def get_responses(client, post_id: str) -> List[Dict[str, Any]]:
    """
    Fetch responses to a specific post.
    
    Args:
        client: An authenticated BlueSky client
        post_id: URI of the post to get responses for
        
    Returns:
        A list of response information dictionaries
    """
    try:
        thread = client.app.bsky.feed.get_post_thread({'uri': post_id})
        responses = []
        if hasattr(thread.thread, 'replies') and thread.thread.replies:
            for reply in thread.thread.replies:
                responses.append({
                    'text': getattr(getattr(reply.post, "record", None), "text", None),
                    'author': getattr(getattr(reply.post, "author", None), "handle", None),
                    'cid': getattr(reply.post, "cid", None),
                    'uri': getattr(reply.post, "uri", None)
                })
        return responses
    except Exception as e:
        logging.error(f"Responses error: {e}", exc_info=True)
        print(f"Responses error: {e!r}")
        return []

def list_posts_and_responses(client) -> None:
    """
    List all posts and their responses for the authenticated user.
    
    Args:
        client: An authenticated BlueSky client
    """
    try:
        feed = client.app.bsky.feed.get_author_feed({'actor': client.me.handle}).feed
        for post in feed:
            print(f"Post: {getattr(getattr(post, 'post', None).record, 'text', None)}")
            if getattr(post, 'reply_count', 0) > 0:
                try:
                    thread = client.app.bsky.feed.get_post_thread({'uri': post.post.uri})
                    if hasattr(thread.thread, 'replies') and thread.thread.replies:
                        for reply in thread.thread.replies:
                            print(f"  Reply: {getattr(getattr(reply.post, 'record', None), 'text', None)}")
                except Exception as e:
                    logging.error(f"Error fetching replies: {e}", exc_info=True)
                    print(f"Error fetching replies: {e!r}")
    except Exception as e:
        logging.error(f"Listing error: {e}", exc_info=True)
        print(f"Listing error: {e!r}")

def list_unanswered_responses(client) -> List[Dict[str, Any]]:
    """
    List all unanswered responses to the user's posts.
    
    Args:
        client: An authenticated BlueSky client
        
    Returns:
        A list of unanswered response information dictionaries
    """
    unanswered = []
    try:
        notifications = client.app.bsky.notification.list_notifications().notifications
        for notification in notifications:
            if getattr(notification, "reason", None) == 'reply':
                try:
                    thread = client.app.bsky.feed.get_post_thread({'uri': notification.uri})
                    replies = getattr(thread.thread, 'replies', [])
                    if not replies or not any(
                        getattr(getattr(reply.post, "author", None), "handle", None) == client.me.handle
                        for reply in replies
                    ):
                        unanswered.append({
                            'cid': getattr(notification, "cid", None),
                            'uri': getattr(notification, "uri", None),
                            'author': getattr(notification.author, "handle", None),
                            'text': getattr(getattr(notification, "record", None), "text", None)
                        })
                except Exception as e:
                    logging.error(f"Error processing thread for notification {getattr(notification, 'uri', None)}: {e}", exc_info=True)
                    print(f"Error processing thread for notification {getattr(notification, 'uri', None)}: {e!r}")
        return unanswered
    except Exception as e:
        logging.error(f"Unanswered responses error: {e}", exc_info=True)
        print(f"Unanswered responses error: {e!r}")
        return []
