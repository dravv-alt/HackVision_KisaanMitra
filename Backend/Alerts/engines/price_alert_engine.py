"""
Price Alert Engine - Economic Monitoring
"""

import uuid
from typing import List
from datetime import datetime
from ..models import FarmerProfile, FarmerCropContext, AlertRecord
from ..repositories import MarketRepo
from ..constants import AlertType, AlertUrgency, PriceTrend, Language


class PriceAlertEngine:
    def generate(
        self, 
        farmer: FarmerProfile, 
        crops: List[FarmerCropContext], 
        market_repo: MarketRepo
    ) -> List[AlertRecord]:
        """
        Monitor mandi price fluctuations and trigger alerts for +/- 15% changes.
        """
        alerts = []
        
        for crop in crops:
            market = market_repo.get_latest_price(crop.cropKey, farmer.district)
            if not market:
                continue
                
            # Trigger alert for significant change (>15%)
            if abs(market.changePct) >= 15.0:
                is_rise = market.trend == PriceTrend.RISING
                urgency = AlertUrgency.HIGH
                
                title = "Price Alert" if farmer.language == Language.ENGLISH else "कीमत अलर्ट"
                
                if is_rise:
                    msg = (f"Market price for {crop.cropName} rising (+{market.changePct}%). Consider selling soon."
                           if farmer.language == Language.ENGLISH else
                           f"{crop.cropName} के बाज़ार भाव बढ़ रहे हैं (+{market.changePct}%)। जल्द बेचने पर विचार करें।")
                else:
                    msg = (f"Price alert! {crop.cropName} prices falling ({market.changePct}%). Suggestions: HOLD stock."
                           if farmer.language == Language.ENGLISH else
                           f"कीमत अलर्ट! {crop.cropName} के दाम गिर गए हैं ({market.changePct}%)। सुझाव: स्टॉक रोक कर रखें।")

                alerts.append(AlertRecord(
                    alertId=str(uuid.uuid4()),
                    farmerId=farmer.farmerId,
                    alertType=AlertType.PRICE,
                    title=title,
                    message=msg,
                    urgency=urgency,
                    related={"cropKey": crop.cropKey, "mandi": market.mandi, "change": market.changePct},
                    scheduledAt=datetime.now()
                ))
                
        return alerts
