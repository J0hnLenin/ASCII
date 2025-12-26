import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

model_name = "dima806/facial_emotions_image_detection"

processor = AutoImageProcessor.from_pretrained(model_name, use_fast=True)
model = AutoModelForImageClassification.from_pretrained(model_name)

def predict_emotion(image, threshold):

    inputs = processor(images=image, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.nn.functional.softmax(logits, dim=-1)[0]
    
    confidence, predicted_class = torch.max(probabilities, dim=-1)
    confidence = confidence.item()
    predicted_class = predicted_class.item()
    
    emotion_label = model.config.id2label[predicted_class]

    if confidence >= threshold:
        return emotion_label

    return None