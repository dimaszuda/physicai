import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def ensure_configured():
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("Supabase connection info missing; please set SUPABASE_URL and SUPABASE_KEY in env or .env")
