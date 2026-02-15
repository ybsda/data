# Useful Commands for Lakehouse Demo

## 1. Kafka Operations

### List all topics
```bash
sudo docker exec data-kafka-1 kafka-topics --bootstrap-server localhost:9092 --list
```

### Read first 10 messages from PostgreSQL topic
```bash
sudo docker exec data-kafka-1 kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic dbserver1.public.users \
  --from-beginning \
  --max-messages 10
```

### Continuous consumption from a topic
```bash
sudo docker exec data-kafka-1 kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic dbserver1.public.users
```

---

## 2. Debezium Connect Operations

### List active connectors
```bash
curl -s http://localhost:8083/connectors
```

### Check status of a specific connector
```bash
curl -s http://localhost:8083/connectors/inventory-connector/status
```

### Register a new connector (Postgres example)
```bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" \
  http://localhost:8083/connectors/ -d @postgres-connector.json
```

---

## 3. Infrastructure & Logs

### Check all running containers
```bash
sudo docker compose -f data/docker-compose.yml ps
```

### View Debezium Connect logs
```bash
sudo docker compose -f data/docker-compose.yml logs debezium-connect --tail 100 -f
```

### View Kafka logs
```bash
sudo docker compose -f data/docker-compose.yml logs kafka --tail 100 -f
```

---

## 4. Testing CDC (Insert Data)

### Insert a new record into PostgreSQL
```bash
sudo docker exec -it data-db-postgres-1 psql -U admin -d customer_db -c "INSERT INTO users (name) VALUES ('Bob');"
```

### Update a record in PostgreSQL
```bash
sudo docker exec -it data-db-postgres-1 psql -U admin -d customer_db -c "UPDATE users SET name = 'ANZER' WHERE name = 'Charlie';"
```

### Delete a record in PostgreSQL
```bash
sudo docker exec -it data-db-postgres-1 psql -U admin -d customer_db -c "DELETE FROM users WHERE name = 'Charlie';"
```

> **Note:** To see the `before` state in update and delete events, the table must have `REPLICA IDENTITY FULL` enabled:
> `ALTER TABLE users REPLICA IDENTITY FULL;`
