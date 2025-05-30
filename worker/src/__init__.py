from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import io
import base64
from config import RABBITMQ_CONFIG
import pika
import json
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def generate_caption(base64_image: str) -> str:
    try:
        image_bytes = base64.b64decode(base64_image)
        img = Image.open(io.BytesIO(image_bytes))

        inputs = processor(img, return_tensors="pt")
        out = model.generate(**inputs)
        result = processor.decode(out[0], skip_special_tokens=True)
        return result
    except Exception as e:
        print(e)
        return "Erro ao gerar caption"

def process_message(ch, method, properties, body):
    try:
        message = json.loads(body)
        image_id = message.get('id')
        base64_image = message.get('image')

        print(f"Recebendo mensagem: {image_id}")
     
        if not image_id or not base64_image:
            raise ValueError("ID e imagem são obrigatórios")


        caption = generate_caption(base64_image)

        response = {
            'id': image_id,
            'caption': caption
        }
        print(f"Enviando mensagem: {response}")
        ch.basic_publish(
            exchange=RABBITMQ_CONFIG['exchange'],
            routing_key=RABBITMQ_CONFIG['routing_key'],
            body=json.dumps(response)
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("except", e)
        ch.basic_nack(delivery_tag=method.delivery_tag)


def main():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_CONFIG['host'], 
            port=RABBITMQ_CONFIG['port'], 
            credentials=pika.PlainCredentials(
                RABBITMQ_CONFIG['user'], 
                RABBITMQ_CONFIG['password']
                )
            )
        )
        global channel
        channel = connection.channel()

        # criar filas
        channel.queue_declare(queue=RABBITMQ_CONFIG['queue_image'])
        channel.queue_declare(queue=RABBITMQ_CONFIG['queue_response'])

        # consumir mensagens da fila de imagens
        channel.basic_consume(queue=RABBITMQ_CONFIG['queue_image'], on_message_callback=process_message, auto_ack=False)

        channel.start_consuming()

    except Exception as e:
        print(f"Erro na conexão com a fila: {e}")
        raise

    finally: 
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    main()
