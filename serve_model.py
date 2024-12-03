from fastapi import FastAPI, File, UploadFile
import torch
from transformers import AutoImageProcessor, ResNetForImageClassification
from PIL import Image
import io

app = FastAPI()

processor = AutoImageProcessor.from_pretrained("./processor")
model = ResNetForImageClassification.from_pretrained("./model")


@app.get("/")
async def root():
    return 200, "OK"


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))
    inputs = processor(image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        label = model.config.id2label[predicted_class_idx]
    return {"label": label}
