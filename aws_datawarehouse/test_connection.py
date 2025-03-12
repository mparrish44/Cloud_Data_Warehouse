import psycopg2
from configparser import ConfigParser

# Read config file
config = ConfigParser()
config.read("dwh.cfg")

# Print available sections for debugging
print("Available sections in dwh.cfg:", config.sections())

# Get database credentials
host = config.get("CLUSTER", "host")
dbname = config.get("CLUSTER", "db_name")
user = config.get("CLUSTER", "db_user")
password = config.get("CLUSTER", "db_password")
port = config.get("CLUSTER", "db_port")

# Connect to Redshift
try:
    conn = psycopg2.connect(
        f"host={host} dbname={dbname} user={user} password={password} port={port}"
    )
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    print("✅ Connected to Redshift successfully!")
    conn.close()
except Exception as e:
    print("❌ Error connecting to Redshift:", e)
