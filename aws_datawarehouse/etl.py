import psycopg2
from configparser import ConfigParser
from sql_queries import copy_table_queries, insert_table_queries


def load_config():
    """Loads configuration from dwh.cfg"""
    config = ConfigParser()
    config.read("dwh.cfg")
    return config


def connect_to_redshift():
    """Establishes connection to Redshift"""
    config = load_config()
    conn = psycopg2.connect(
        f"host={config.get('CLUSTER', 'host')} dbname={config.get('CLUSTER', 'db_name')} "
        f"user={config.get('CLUSTER', 'db_user')} password={config.get('CLUSTER', 'db_password')} "
        f"port={config.get('CLUSTER', 'db_port')}"
    )
    return conn.cursor(), conn


def load_staging_tables(cur, conn):
    """Loads data from S3 to Redshift staging tables"""
    print("Loading data into staging tables...")
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()
    print("Staging tables loaded successfully!")


def insert_into_tables(cur, conn):
    """Inserts data into final tables from staging"""
    print("Inserting data into final tables...")
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
    print("Data inserted into final tables successfully!")


def main():
    """Main ETL process"""
    cur, conn = connect_to_redshift()

    print("Starting ETL Pipeline...")
    load_staging_tables(cur, conn)
    insert_into_tables(cur, conn)

    conn.close()
    print("ETL Pipeline Completed Successfully!")


if __name__ == "__main__":
    main()
