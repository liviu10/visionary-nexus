import os
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

def download_models():
    # Use a small, efficient model for transaction categorization
    model_name = "facebook/bart-large-mnli"  # Good for zero-shot classification
    # Alternative: "cross-encoder/nli-distilroberta-base" for even lighter weight
    
    print(f"Downloading model: {model_name}...")
    
    # Pre-download and cache everything
    pipeline("zero-shot-classification", model=model_name)
    
    print("Model downloaded and cached successfully.")

if __name__ == "__main__":
    download_models()
