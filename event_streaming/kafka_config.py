class KafkaStreamConfig:
    BOOTSTRAP_SERVERS=["localhost:9092"]  # reference only; no broker connection in simulation mode
    IMEI_GENESIS_TOPIC="telecom.device.genesis"
    IMEI_MUTATION_TOPIC="telecom.device.lifecycle"
    SECURITY_ALERT_TOPIC="telecom.security.alerts"
    CONSUMER_GROUP_ID="telecom-lake-ingestion-workers"
kafka_stream_config=KafkaStreamConfig()
