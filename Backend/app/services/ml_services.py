import joblib
import pandas as pd
import os
import pathlib as Path

class AegisMlService:
    def __init__(self):
        
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        model_path = base_dir / "Model" / "aegis_sentinel_brain.joblib"

        print(f"Aegis SRE: Loading model from: {model_path}")

        if not model_path.exists():
            raise FileNotFoundError(f"Aegis SRE: Model file not found at: {model_path}")
        
        checkpoint = joblib.load(model_path)
        self.model = checkpoint['model']
        self.scaler = checkpoint['scaler']
        self.features = checkpoint['features']

        print("Aegis SRE: Model loaded successfully.")
        