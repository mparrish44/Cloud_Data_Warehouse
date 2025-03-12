import psycopg2
from configparser import ConfigParser
from sql_queries import create_table_queries, drop_table_queries


def load_config():
    """Loads Redshift configuration from dwh.cfg"""
    config = ConfigParser()
    config.read("dwh.cfg")
    return config


def create_database():
    """Establishes connection to Redshift"""
    config = load_config()

    # Get Redshift connection details
    host = config.get("CLUSTER", "host")
    dbname = config.get("CLUSTER", "db_name")
    user = config.get("CLUSTER", "db_user")
    password = config.get("CLUSTER", "db_password")
    port = config.get("CLUSTER", "db_port")

    try:
        conn = psycopg2.connect(
            f"host={host} dbname={dbname} user={user} password={password} port={port}"
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        print("Connected to Redshift successfully!")
        return cur, conn
    except Exception as e:
        print(f"Error connecting to Redshift: {e}")
        return None, None


def drop_tables(cur, conn):
    """Drops all tables if they exist"""
    print("Dropping existing tables...")
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    print("All tables dropped successfully!")


def create_tables(cur, conn):
    """Creates tables based on queries in sql_queries.py"""
    print("Creating tables...")
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
    print("All tables created successfully!")


def main():
    """Main function to drop and create tables"""
    cur, conn = create_database()
    if cur and conn:
        drop_tables(cur, conn)
        create_tables(cur, conn)
        conn.close()
        print("Redshift Database Setup Complete!")


if __name__ == "__main__":
    main()
