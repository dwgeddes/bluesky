import logging
from typing import List, Dict, Any

def get_notifications(client) -> None:
    try:
        notifications = client.app.bsky.notification.list_notifications().notifications
        for notification in notifications:
            print(f"Notification from {notification.author.handle}: {notification.reason}")
    except Exception as e:
        logging.error(f"Notifications error: {e}")
        print(f"Notifications error: {e}")

def get_responses(client, post_id: str) -> List[Dict[str, Any]]:
    try:
        thread = client.app.bsky.feed.get_post_thread({'uri': post_id})
        responses = []
        if hasattr(thread.thread, 'replies'):
            responses = [{
                'text': reply.post.record.text,
                'author': reply.post.author.handle,
                'cid': reply.post.cid,
                'uri': reply.post.uri
            } for reply in thread.thread.replies]
        return responses
    except Exception as e:
        logging.error(f"Responses error: {e}")
        raise

def list_posts_and_responses(client) -> None:
    try:
        feed = client.app.bsky.feed.get_author_feed({'actor': client.me.handle}).feed
        for post in feed:
            print(f"Post: {post.post.record.text}")
            if getattr(post, 'reply_count', 0) > 0:
                try:
                    thread = client.app.bsky.feed.get_post_thread({'uri': post.post.uri})
                    if hasattr(thread.thread, 'replies'):
                        for reply in thread.thread.replies:
                            print(f"  Reply: {reply.post.record.text}")
                except Exception as e:
                    logging.error(f"Error fetching replies: {e}")
                    print(f"Error fetching replies: {e}")
    except Exception as e:
        logging.error(f"Listing error: {e}")
        print(f"Listing error: {e}")

def list_unanswered_responses(client) -> List[Dict[str, Any]]:
    unanswered = []
    try:
        notifications = client.app.bsky.notification.list_notifications().notifications
        for notification in notifications:
            if notification.reason == 'reply':
                thread = client.app.bsky.feed.get_post_thread({'uri': notification.uri})
                if not hasattr(thread.thread, 'replies') or not any(
                    reply.post.author.handle == client.me.handle for reply in thread.thread.replies
                ):
                    unanswered.append({
                        'cid': notification.cid,
                        'uri': notification.uri,
                        'author': notification.author.handle,
                        'text': notification.record.text
                    })
        return unanswered
    except Exception as e:
        logging.error(f"Unanswered responses error: {e}")
        raise
