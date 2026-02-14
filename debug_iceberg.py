import os
from pyspark.sql import SparkSession

print("--- DEBUG: Démarrage ---")

# Configuration explicite
spark = SparkSession.builder \
    .appName("Lakehouse-Debug") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
    .config("spark.sql.catalog.spark_catalog.type", "hadoop") \
    .config("spark.sql.catalog.spark_catalog.warehouse", "s3a://warehouse/") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", "s3a://warehouse/") \
    .config("spark.sql.catalog.demo", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.demo.type", "hadoop") \
    .config("spark.sql.catalog.demo.warehouse", "s3a://warehouse/demo") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "password") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .getOrCreate()

print("✅ Spark Session initialisée.")

print("🛠️ Test: Création namespace...")
try:
    spark.sql("CREATE NAMESPACE IF NOT EXISTS local.gold_db")
    print("✅ Namespace 'gold_db' OK.")
except Exception as e:
    print(f"❌ ERREUR Namespace: {e}")

print("🛠️ Test: Création table...")
try:
    spark.sql("""
        CREATE TABLE IF NOT EXISTS local.gold_db.final_users (
            json_payload STRING
        ) USING iceberg
    """)
    print("✅ Table 'final_users' OK.")
except Exception as e:
    print(f"❌ ERREUR Table: {e}")

spark.stop()
print("--- DEBUG: Fin ---")
