# microsoft/resnet-50
import uuid

import torch
from transformers import AutoImageProcessor, ResNetForImageClassification
from datasets import load_dataset
import pprint


images = load_dataset("./data")
processor = AutoImageProcessor.from_pretrained("./processor")
model = ResNetForImageClassification.from_pretrained("./model")

with torch.no_grad():
    inputs = [processor(image, return_tensors="pt") for image in images["train"]["image"]]
    labels = [
        model.config.id2label[model(**_input).logits.argmax(-1).item()] for _input in inputs
    ]
    filenames = [
        img.filename.split("/")[-1] if hasattr(img, "filename") else uuid.uuid1()
        for img in images
    ]

    results = {filename: label for filename, label in zip(filenames, labels)}
    pprint.pprint(results)
