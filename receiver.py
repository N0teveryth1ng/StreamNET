from confluent_kafka import Consumer
import os
import json
import time
from sqlalchemy import create_engine, text
from dotenv import load_dotenv








load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)

config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'group.id': 'my-python-group',
    'auto.offset.reset': 'earliest',
    }  



KAFKA_USERNAME = os.getenv('KAFKA_USERNAME')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD')


# SASL security protocol
if KAFKA_USERNAME and KAFKA_PASSWORD:
    config.update({
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN',
        'sasl.username': KAFKA_USERNAME,
        'sasl.password': KAFKA_PASSWORD
    })
    
    
    
# subscribe to the server
c = Consumer(config)
c.subscribe(['system_data'])


print("Waiting for messages... Press Ctrl+C to exit.")


batch_buffer = []
MAX_BATCH_SIZE = 1000
MAX_WAIT_TIME = 2.0
last_flush_time = time.time()




# store the data in DB
def flush_to_destination():
    global batch_buffer, last_flush_time
    if not batch_buffer:
        last_flush_time = time.time()
        return

    try:
        print(f"Flushing {len(batch_buffer)} records to database")
        with engine.begin() as conn:
            query = text("""
                INSERT INTO system_events (id, timestamp, service_name, environment, event_type, message, metadata)
                VALUES (:id, :timestamp, :service_name, :environment, :event_type, :message, :metadata)
            """)
            conn.execute(query, batch_buffer)

        batch_buffer.clear()
        last_flush_time = time.time()

    except Exception as e:
        print(f"Storage Error: {e}")







# polling to the server
try:
    while True:
        msg = c.poll(1.0) # Wait up to 1 second for a message
        
        if msg is None:
            if time.time() - last_flush_time >= MAX_WAIT_TIME:
                flush_to_destination()
            continue
        
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        print(f"Received message: {msg.value().decode('utf-8')}")


except KeyboardInterrupt:
    print("stopping Consumer")
finally:
    c.close()
    
    
