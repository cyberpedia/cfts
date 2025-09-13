import os
from slowapi import Limiter
from slowapi.util import get_remote_address

# Use REDIS_URL from environment for the limiter's storage, with a local fallback
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")

limiter = Limiter(key_func=get_remote_address, storage_uri=redis_url)
