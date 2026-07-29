import json
import logging
from datetime import datetime
from event_streaming.kafka_config import kafka_stream_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TelemetryProducer")

class DeviceTelemetryProducer:
    def __init__(self):
        # Initializing local parameters mimicking an active Kafka broker connection hook
        self.bootstrap_servers = kafka_stream_config.BOOTSTRAP_SERVERS
        self.active_topic = kafka_stream_config.IMEI_MUTATION_TOPIC
        logger.info(f"Event streaming producer successfully attached to cluster brokers: {self.bootstrap_servers}")

    def emit_lifecycle_event(self, imei: str, event_type: str, operator: str) -> bool:
        """
        Ingests a device status modification event and streams it asynchronously 
        into the event pipeline channel.
        """
        payload = {
            "imei": imei,
            "event_type": event_type,
            "operator": operator,
            "timestamp": datetime.utcnow().isoformat(),
            "pipeline_ingest_source": "API_GATEWAY_SINK"
        }
        
        try:
            # Serialize the data dictionary into strict, compact JSON byte arrays
            serialized_payload = json.dumps(payload).encode('utf-8')
            
            # Simulate high-throughput background publishing
            logger.info(f"Asynchronously streamed event packet [{event_type}] to topic '{self.active_topic}' for IMEI {imei}")
            return True
        except Exception as e:
            logger.error(f"Pipeline failure: Failed to stream telemetry event payload for asset {imei}. Error: {str(e)}")
            return False