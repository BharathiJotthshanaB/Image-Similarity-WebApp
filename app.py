from flask import Flask, render_template, request
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)

# Ensure upload folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load pretrained ResNet50 model
# NOTE: Using DEFAULT weights to avoid deprecation warnings
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

# Image preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def get_features(img_path):
    """Extract feature vector from image using pretrained ResNet50."""
    img = Image.open(img_path).convert('RGB')
    tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        features = model(tensor)
    return features.numpy().flatten()

def cosine_similarity(v1, v2):
    """Compute cosine similarity between two feature vectors."""
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

@app.route('/', methods=['GET', 'POST'])
def index():
    score = None
    img1 = img2 = None

    if request.method == 'POST':
        f1 = request.files['image1']
        f2 = request.files['image2']

        if f1 and f2:
            # Save uploaded images
            path1 = os.path.join(UPLOAD_FOLDER, f1.filename)
            path2 = os.path.join(UPLOAD_FOLDER, f2.filename)
            f1.save(path1)
            f2.save(path2)

            # Extract features and calculate similarity
            v1, v2 = get_features(path1), get_features(path2)
            score = float(cosine_similarity(v1, v2))

            # Save filenames for template display
            img1, img2 = f1.filename, f2.filename

    return render_template('index.html', score=score, img1=img1, img2=img2)

if __name__ == '__main__':
    app.run(debug=True)
