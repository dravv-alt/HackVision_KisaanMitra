"""
Irrigation Alert Engine - Decision Logic
"""

import uuid
from typing import List
from datetime import datetime
from ..models import FarmerProfile, FarmerCropContext, WeatherContext, AlertRecord
from ..constants import AlertType, AlertUrgency, AlertStatus


class IrrigationAlertEngine:
    def generate(
        self, 
        farmer: FarmerProfile, 
        crops: List[FarmerCropContext], 
        weather: WeatherContext
    ) -> List[AlertRecord]:
        """
        Generate irrigation alerts based on weather forecast and crop status.
        Uses farmer profile to localize messages.
        """
        alerts = []
        
        # 1. Rain Expected Scenario
        if weather.rainForecastBool or weather.rainChancePct > 60:
            for crop in crops:
                # Flowering stage makes this more critical
                urgency = AlertUrgency.HIGH if crop.subStage == "flowering" else AlertUrgency.MEDIUM
                
                title = "Rain Alert" if farmer.language == "en" else "बारिश का अलर्ट"
                msg = (f"Stop irrigation for {crop.cropName} today. High chance of rain ({weather.rainChancePct}%)."
                       if farmer.language == "en" else
                       f"{crop.cropName} के लिए आज सिंचाई बंद करें। बारिश की अधिक संभावना ({weather.rainChancePct}%) है।")
                
                alerts.append(self._create_alert(
                    farmer.farmerId, title, msg, urgency, {"cropKey": crop.cropKey}
                ))

        # 2. Dry conditions / Heatwave scenario
        elif weather.temperatureC > 35 and weather.humidityPct < 40:
             for crop in crops:
                title = "Irrigation Update" if farmer.language == "en" else "सिंचाई अपडेट"
                msg = (f"Extreme heat detected ({weather.temperatureC}°C). Recommended to irrigate {crop.cropName}."
                       if farmer.language == "en" else
                       f"अत्यधिक गर्मी ({weather.temperatureC}°C) के कारण {crop.cropName} की सिंचाई करने की सलाह दी जाती है।")
                
                alerts.append(self._create_alert(
                    farmer.farmerId, title, msg, AlertUrgency.MEDIUM, {"cropKey": crop.cropKey}
                ))

        # Placeholder for IoT soil moisture triggers (future scope)
        # if soil_moisture_level < 20: ...
        
        return alerts

    def _create_alert(self, farmer_id, title, message, urgency, related):
        return AlertRecord(
            alertId=str(uuid.uuid4()),
            farmerId=farmer_id,
            alertType=AlertType.IRRIGATION,
            title=title,
            message=message,
            urgency=urgency,
            related=related,
            scheduledAt=datetime.now()
        )
