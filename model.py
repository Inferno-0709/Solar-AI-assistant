from transformers import TFSegformerForSemanticSegmentation, SegformerFeatureExtractor
from PIL import Image
import numpy as np
import tensorflow as tf

# Load model + feature extractor
def load_tf_segmentation_model():
    model = TFSegformerForSemanticSegmentation.from_pretrained("nvidia/segformer-b0-finetuned-ade-512-512")
    extractor = SegformerFeatureExtractor.from_pretrained("nvidia/segformer-b0-finetuned-ade-512-512")
    return model, extractor

# Run prediction
def segment_rooftop(model, extractor, image):
    inputs = extractor(images=image, return_tensors="tf")
    outputs = model(**inputs)
    logits = outputs.logits  # shape: (batch, num_classes, height, width)

    # Get predicted class per pixel
    predicted = tf.math.argmax(logits, axis=1)
    predicted_mask = predicted[0].numpy().astype(np.uint8)

    return predicted_mask
