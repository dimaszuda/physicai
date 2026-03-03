from supabase import create_client
from ..config import SUPABASE_URL, SUPABASE_KEY

_client = None


def get_supabase():
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise RuntimeError("Supabase connection info missing; run config.ensure_configured()")
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _client
