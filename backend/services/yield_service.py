from ml.yield_prediction.predict_yield import predict_crop_yield

class YieldService:
    @staticmethod
    def calculate_estimated_yield(crop: str, area_acres: float = 2.0, rainfall: float = 120.0,
                                  temperature: float = 28.0, n: float = 80.0, p: float = 40.0,
                                  k: float = 40.0, ph: float = 6.5, season: str = "Kharif",
                                  fertilizer_usage_kg: float = 100.0) -> dict:
        """Calculates expected crop harvest yield metrics."""
        return predict_crop_yield(
            crop=crop,
            area_acres=float(area_acres),
            rainfall=float(rainfall),
            temperature=float(temperature),
            n=float(n),
            p=float(p),
            k=float(k),
            ph=float(ph),
            season=season,
            fertilizer_usage_kg=float(fertilizer_usage_kg)
        )
