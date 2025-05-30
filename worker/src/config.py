import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega o arquivo .env do diretório raiz do projeto
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Configurações do RabbitMQ
RABBITMQ_CONFIG = {
    'host': os.getenv('RABBITMQ_HOST', 'localhost'),
    'port': int(os.getenv('RABBITMQ_PORT', 5672)),
    'user': os.getenv('RABBITMQ_USER', 'guest'),
    'password': os.getenv('RABBITMQ_PASSWORD', 'guest'),
    'exchange': os.getenv('RABBITMQ_EXCHANGE', ''),
    'routing_key': os.getenv('RABBITMQ_ROUTING_KEY', ''),
    'queue_image': os.getenv('RABBITMQ_QUEUE_IMAGE', ''),
    'queue_response': os.getenv('RABBITMQ_QUEUE_RESPONSE', '')
}