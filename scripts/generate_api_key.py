#!/usr/bin/env python3
"""Generate a secure API key for authentication."""
import secrets
import sys


def generate_api_key(length: int = 32) -> str:
    """Generate a cryptographically secure API key.
    
    Args:
        length: Length of the random bytes (default 32)
        
    Returns:
        URL-safe base64 encoded string
    """
    return secrets.token_urlsafe(length)


if __name__ == "__main__":
    key = generate_api_key()
    print("Generated API Key:")
    print(key)
    print("\nAdd this to your .env file:")
    print(f"API_KEY={key}")
    print("\nOr set as environment variable in Vercel:")
    print("Vercel Dashboard -> Settings -> Environment Variables")
