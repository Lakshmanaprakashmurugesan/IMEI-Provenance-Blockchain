import json, logging
from datetime import datetime, timezone
from .kafka_config import kafka_stream_config
logger=logging.getLogger("TelemetryProducer")
class DeviceTelemetryProducer:
    """Kafka-compatible serialization simulation. No broker is contacted."""
    def __init__(self): self.active_topic=kafka_stream_config.IMEI_MUTATION_TOPIC
    def build_lifecycle_event(self, imei, event_type, operator):
        payload={"imei":imei,"event_type":event_type,"operator":operator,"timestamp":datetime.now(timezone.utc).isoformat(),"simulation":True}
        return json.dumps(payload,separators=(",",":"),sort_keys=True).encode()
    def emit_lifecycle_event(self, imei, event_type, operator):
        packet=self.build_lifecycle_event(imei,event_type,operator)
        logger.info("SIMULATED_EMIT topic=%s imei=%s bytes=%s",self.active_topic,imei,len(packet))
        return {"status":"SIMULATED_EMIT","topic":self.active_topic,"packet":packet}
