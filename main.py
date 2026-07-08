from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from confluent_kafka import Producer
import os, json




app = FastAPI()
templates = Jinja2Templates(directory="templates")




    
# cofigure kafka  (data ingestion from main.py)
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
KAFKA_USERNAME = os.getenv('KAFKA_USERNAME')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD')

kafka_config = {'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS}

# Add SASL authentication if username is provided (for Cloud Kafka like Confluent)
if KAFKA_USERNAME and KAFKA_PASSWORD:
    kafka_config.update({
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': 'PLAIN', # Confluent Cloud uses PLAIN
        'sasl.username': KAFKA_USERNAME,
        'sasl.password': KAFKA_PASSWORD
    })

producer = None



def delivery_report(err, msg):
    if err is not None:
        print(f"[KAFKA ERROR] message delivery failed: {err}")
    else:
        print(f"[KAFKA SUCCESS] delivered to {msg.topic()} [{msg.partition()}]")


def get_producer():
    global producer
    if producer is None:
        try:
            producer = Producer(kafka_config)
        except Exception as exc:    
            print(f"[KAFKA INIT ERROR] {exc}")
            producer = False
    return producer if producer is not False else None





# presist event fucntion 
# def persist_event(payload):
    event_record = {
        'id': str(payload.event_id),
        'timestamp': payload.timestamp,
        'service_name': payload.source,
        'environment': os.getenv('ENVIRONMENT', 'dev'),
        'event_type': payload.event_name,
        'message': json.dumps(payload.payload),
        'metadata': json.dumps(payload.payload),
    }
    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO system_events (id, timestamp, service_name, environment, event_type, message, metadata)
                VALUES (:id, :timestamp, :service_name, :environment, :event_type, :message, :metadata)
            """),
            event_record,
        )





# connect input html file
@app.get("/input", response_class=HTMLResponse)
async def get_input(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="input.html"
    )
    
    
    
# connect data input to kafka
@app.post("/get_data" )
async def get_data(request: Request):
        
    try:
        data = await request.json()
        kafka_producer = get_producer()
        if kafka_producer is not None:
            try:    
                print(f"Data In Pocket {data} ..👍")
                
                kafka_producer.produce(topic="system_data", key='id1', value=json.dumps(data), callback=delivery_report)
                kafka_producer.flush(timeout=2)
                return {"success":"message sent successfully"}             
                
            except Exception as e:
                return {"error": str(e)}
        
        else:
            return {"error": "kafka producer unavailable"}
    
    
        persist_event(payload)
            return {"status": "Data received and stored locally ✌️}
        
    except Exception as e:
        return {"error": str(e)}, 500
    





@app.get("/health")
async def root():
    return {"message": "Checks OK - ✅"}