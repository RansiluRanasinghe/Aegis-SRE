import joblib
import pandas as pd
import os
from pathlib import Path

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
        self.feature_names = checkpoint['features']

        print("Aegis SRE: Model loaded successfully.")

    def predict(self, log_data:dict) -> dict:

        try:
            ordered_features = [log_data[feature] for feature in self.feature_names]
        except KeyError as e:
            raise ValueError(f"Aegis SRE: Missing required feature in input data: {e}")

        input_df = pd.DataFrame([ordered_features], columns=self.feature_names)

        scaled_data = self.scaler.transform(input_df)
        prediction = self.model.predict(scaled_data)[0]

        score = self.model.predict_proba(scaled_data)[1]
        is_anomaly = True if prediction == -1 else False

        return {
            "is_anomaly" : is_anomaly,
            "confidence_score" : float(score)
        }


ml_engine = AegisMlService()           