from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import io
import base64


processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def generate_caption(base64_image):
    image_bytes = base64.b64decode(base64_image)
    img = Image.open(io.BytesIO(image_bytes))

    inputs = processor(img, return_tensors="pt")
    out = model.generate(**inputs)
    result = processor.decode(out[0], skip_special_tokens=True)
    print("result: ", result)
    return result
