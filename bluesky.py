"""
BlueSky Command-Line Interface

This module handles argument parsing and calls functions from bluesky_core.
"""

import sys, argparse
from atproto import Client
import logging

# ...existing configuration, logging, etc...
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

from bluesky_core import (get_credentials, clear_credentials, authenticate_bluesky, post,
                          get_notifications, list_unanswered_responses)

service_name = "Bluesky"
username = "jetsetjaxon.bsky.social"

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Post text or images to BlueSky.",
        usage="python bluesky_post.py --text 'Your text here' [--image /path/to/image] [--alt 'Alternative text']"
    )
    parser.add_argument("--text", type=str, help="The text to post.", required=False)
    parser.add_argument("--image", type=str, help="Path to an image file.", required=False)
    parser.add_argument("--alt", type=str, help="Alternative text for image.", default="Image")
    parser.add_argument("--clear-credentials", action="store_true", help="Clear stored credentials")
    parser.add_argument("--get-notifications", action="store_true", help="Show notifications")
    parser.add_argument("--get-responses", action="store_true", help="List unanswered responses")
    args = parser.parse_args()
    
    if args.clear_credentials:
        clear_credentials()
        return

    password = get_credentials(service_name, username)
    client = Client()
    try:
        authenticate_bluesky(client, username, password)
    except Exception as e:
        print(f"Authentication error: {e}")
        sys.exit(1)

    if args.get_notifications:
        get_notifications(client)
    elif args.get_responses:
        responses = list_unanswered_responses(client)
        if responses:
            for resp in responses:
                print(f"Unanswered response from {resp['author']}: {resp['text']}")
        else:
            print("No unanswered responses found.")
    elif args.image:
        post(client, args.text, args.image, args.alt)
    else:
        post(client, args.text)

if __name__ == "__main__":
    main()