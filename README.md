# 🚀 AWS Redshift Data Warehouse & ETL Pipeline

## **💌 Project Overview**
This project builds an **ETL pipeline** for **Sparkify**, a music streaming startup, using **Amazon Redshift**.  
The pipeline extracts **JSON log & song data** from **AWS S3**, stages it in **Redshift**, and transforms it into a **star schema** for analytical queries.  

---

## **📉 Database Schema**
The **star schema** consists of:
- **Fact Table**: `songplays` - Stores records of song play activity.
- **Dimension Tables**: `users`, `songs`, `artists`, `time`.

### **Schema Diagram**
```
        songplays (fact)
        ┌────────────────────────────────────────┐
        │ songplay_id │
        │ start_time  │
        │ user_id     │
        │ level       │
        │ song_id     │
        │ artist_id   │
        │ session_id  │
        │ location    │
        │ user_agent  │
        └────────────────────────────────────────┘
             ▲  
  ┌─────────────────────────────────────────┐
  │          │          │
┌────────────────────────────────────────────────────────────────────────┐
│   users   ││  songs   ││ artists  ││   time   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## **📚 Repository Structure**
| File | Description |
|------|------------|
| `create_tables.py` | Drops and creates Redshift tables before running ETL. |
| `etl.py` | Extracts, Loads, and Transforms (ETL) data from S3 to Redshift. |
| `sql_queries.py` | Contains SQL queries for creating, copying, and inserting data. |
| `dwh.cfg` | Configuration file storing AWS Redshift, IAM, and S3 settings. |
| `README.md` | This documentation file. |

---

## **💼 How to Run This Project**

### **1️⃣ Setup AWS Resources**
1. Create an **IAM Role** with `AmazonS3ReadOnlyAccess` and attach it to Redshift.
2. Create a **Redshift Cluster** and note:
   - **Cluster Endpoint**
   - **Database Name**
   - **Username & Password**
3. Update `dwh.cfg` with these values.

### **2️⃣ Run Python Scripts**
#### **🔹 Install Required Libraries**
Run:
```bash
pip install psycopg2 configparser
```

#### **🔹 Run `create_tables.py`**
This **drops and recreates tables** in Redshift:
```bash
python create_tables.py
```

#### **🔹 Run `etl.py`**
This **loads data from S3 → Redshift staging tables → Star schema**:
```bash
python etl.py
```

#### **🔹 Verify in Redshift**
Run:
```sql
1. SELECT COUNT(*) FROM songplays;
2. SELECT COUNT(*) FROM users;
3. SELECT COUNT(*) FROM songs;
4. SELECT COUNT(*) FROM artists;
5. SELECT COUNT(*) FROM time;
6. SELECT * FROM time LIMIT 5;
7. SELECT * FROM staging_events LIMIT 5;
8. SELECT * FROM staging_songs LIMIT 5;
9. SELECT s.title AS song, count(song) AS frequency 
10. FROM songplays sp 
    JOIN songs s ON (s.song_id = sp.song_id) 
    GROUP BY song
    ORDER BY count(*) desc
    LIMIT 5;
11. SELECT extract(hour from sp.start_time) as hour, count(hour) AS frequency
    FROM songplays sp
    GROUP BY hour
    ORDER BY count(*) desc
    LIMIT 5;


```
✅ If row counts are greater than `0`, ETL **ran successfully**!

---

## **🛠️ Cleanup (Avoid AWS Charges)**
Once done, **delete your Redshift Cluster**:
1. **Go to AWS Redshift Console**.
2. Select your cluster → **Click "Delete"**.

---

## **🚀 Next Steps**
✅ Optimize queries for performance.  
✅ Use **Apache Airflow** to schedule & automate the pipeline.  
✅ Deploy **multi-node Redshift cluster** for scalability.  


