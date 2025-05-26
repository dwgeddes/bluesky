"""
BlueSky Command-Line Interface

This module handles argument parsing and calls functions from bluesky_core.
"""

import argparse
import logging
import sys

from atproto import Client

from .auth import authenticate_bluesky, clear_credentials, get_credentials
from .bluesky_core import post
from .config import DEFAULT_LOG_LEVEL, DEFAULT_USERNAME, LOG_FORMAT, SERVICE_NAME
from .notifications import (
    get_notifications,
    list_posts_and_responses,
    list_unanswered_responses,
)

# Configure logging
logging.basicConfig(level=getattr(logging, DEFAULT_LOG_LEVEL), format=LOG_FORMAT)


def main() -> None:
    """
    Main entry point for the CLI application.
    """
    parser = argparse.ArgumentParser(
        description="Post text or images to BlueSky and manage your account.",
        usage="bluesky [options]",
    )
    parser.add_argument("--text", type=str, help="The text to post.")
    parser.add_argument("--image", type=str, help="Path to an image file.")
    parser.add_argument(
        "--alt", type=str, help="Alternative text for image.", default="Image"
    )
    parser.add_argument(
        "--clear-credentials", action="store_true", help="Clear stored credentials"
    )
    parser.add_argument(
        "--get-notifications", action="store_true", help="Show notifications"
    )
    parser.add_argument(
        "--get-responses", action="store_true", help="List unanswered responses"
    )
    parser.add_argument(
        "--list-posts", action="store_true", help="List your posts and their responses"
    )
    parser.add_argument(
        "--username",
        type=str,
        help=f"BlueSky username (default: {DEFAULT_USERNAME})",
        default=DEFAULT_USERNAME,
    )

    args = parser.parse_args()

    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Handle clearing credentials separately as it doesn't require authentication
    if args.clear_credentials:
        clear_credentials()
        return

    # All other operations require authentication
    username = args.username
    password = get_credentials(SERVICE_NAME, username)
    client = Client()

    try:
        authenticate_bluesky(client, username, password)
        print(f"Successfully authenticated as {username}")
    except Exception as e:
        print(f"Authentication error: {e}")
        sys.exit(1)

    # Handle various command line options
    try:
        if args.get_notifications:
            notifications = get_notifications(client)
            if notifications:
                print(f"\nYou have {len(notifications)} notifications.")
            else:
                print("No notifications found or an error occurred.")

        elif args.get_responses:
            responses = list_unanswered_responses(client)
            if responses:
                print(f"\nYou have {len(responses)} unanswered responses:")
                for i, resp in enumerate(responses, 1):
                    print(f"{i}. From: {resp['author']}")
                    print(f"   Text: {resp['text']}")
                    print()
            else:
                print("No unanswered responses found.")

        elif args.list_posts:
            list_posts_and_responses(client)

        elif args.image or args.text:
            # Ensure text is provided
            text = args.text or ""
            if not text and not args.image:
                print("Error: Please provide text content or an image to post.")
                sys.exit(1)

            post(client, text, args.image, args.alt)

    except Exception as e:
        logging.error(f"Error in command execution: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
