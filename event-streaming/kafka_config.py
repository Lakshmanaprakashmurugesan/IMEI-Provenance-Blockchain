import os

class KafkaStreamConfig:
    # Cluster Connectivity
    BOOTSTRAP_SERVERS: list = ["localhost:9092"]
    
    # Core Stream Channel Topics
    IMEI_GENESIS_TOPIC: str = "telecom.device.genesis"
    IMEI_MUTATION_TOPIC: str = "telecom.device.lifecycle"
    SECURITY_ALERT_TOPIC: str = "telecom.security.alerts"
    
    # Performance Configurations
    ACK_POLICY: str = "all"  # Requires all cluster brokers to acknowledge receipts
    MAX_REQUEST_SIZE_BYTES: int = 5242880  # 5MB processing allocation window
    CONSUMER_GROUP_ID: str = "telecom-lake-ingestion-workers"

kafka_stream_config = KafkaStreamConfig()