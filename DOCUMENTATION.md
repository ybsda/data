# Data Lakehouse Project Documentation

This document records the setup and configuration steps for the Data Lakehouse demonstration environment.

## Architecture Overview
- **Sources:** PostgreSQL, MySQL (Sales & HR)
- **Ingestion:** Kafka & Debezium (CDC)
- **Storage:** MinIO (S3-compatible Iceberg warehouse)
- **Compute:** Apache Spark & Trino

## Setup Steps

### 1. Initial Service Configuration
To support a single-broker Kafka environment, the following environment variables were updated in `data/docker-compose.yml`:

**Kafka:**
- `KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1`
- `KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1`
- `KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1`

**Debezium Connect:**
- `CONFIG_STORAGE_REPLICATION_FACTOR: 1`
- `OFFSET_STORAGE_REPLICATION_FACTOR: 1`
- `STATUS_STORAGE_REPLICATION_FACTOR: 1`

### 2. Starting the Environment
Start the core infrastructure and source databases:
```bash
sudo docker compose -f data/docker-compose.yml up -d kafka debezium-connect db-postgres
```

### 3. Configuring PostgreSQL Connector
A connector named `inventory-connector` was registered to capture changes from the `customer_db`.

**Configuration (`postgres-connector.json`):**
```json
{
  "name": "inventory-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "db-postgres",
    "database.port": "5432",
    "database.user": "admin",
    "database.password": "admin",
    "database.dbname": "customer_db",
    "topic.prefix": "dbserver1",
    "schema.include.list": "public",
    "plugin.name": "pgoutput"
  }
}
```

**Registration Command:**
```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d @postgres-connector.json
```

### 4. Verification
- **Connector Status:** `curl -s http://localhost:8083/connectors/inventory-connector/status`
- **Kafka Topics:** `sudo docker exec data-kafka-1 kafka-topics --bootstrap-server localhost:9092 --list`
- **Data Ingestion:** `sudo docker exec data-kafka-1 kafka-console-consumer --bootstrap-server localhost:9092 --topic dbserver1.public.users --from-beginning --max-messages 1`

---

## CDC Data Quality

### Enabling Full State Capture (Before/After)
By default, PostgreSQL logs only the primary key values for the `before` state in update/delete events to minimize WAL (Write-Ahead Log) size. This results in the `before` field being `null` in Debezium events for non-primary key columns.

To capture the complete state of a record before a change occurs, we enabled **Replica Identity Full** on the source tables:

```sql
ALTER TABLE users REPLICA IDENTITY FULL;
```

**Why this is important:**
- **Auditing:** Enables tracking exactly what values changed (old value vs. new value).
- **Downstream Logic:** Essential for stream processing applications that need the previous state to calculate deltas or manage stateful aggregations.
- **Lakehouse Synchronization:** Ensures that the data lake can correctly handle updates and deletes by identifying the specific record state being replaced.
