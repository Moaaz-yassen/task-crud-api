# ============================================================
#  supabase_client.py — initializes the Supabase client
#  This file is imported wherever we need to talk to Supabase.
# ============================================================

import os
from supabase import create_client
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# create_client() connects to our Supabase project.
# This single instance is reused across the whole application.
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
