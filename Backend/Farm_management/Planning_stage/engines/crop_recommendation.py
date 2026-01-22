"""
Crop Recommendation Engine - scores and recommends crops
Uses multi-factor scoring algorithm
"""
from typing import List
from ..models import (
    CropRecord, CropRecommendation, FarmerProfile, 
    EnvironmentalContext, PlanningRequest
)
from ..constants import (
    Season, RiskPreference, CROP_SCORING_WEIGHTS
)


class CropRecommendationEngine:
    """Engine for scoring and recommending crops"""
    
    def __init__(self):
        """Initialize recommendation engine"""
        self.weights = CROP_SCORING_WEIGHTS
    
    def recommend(
        self,
        request: PlanningRequest,
        farmer: FarmerProfile,
        env: EnvironmentalContext,
        crops: List[CropRecord],
        season: Season
    ) -> List[CropRecommendation]:
        """
        Generate crop recommendations with scoring
        
        Args:
            request: Planning request with preferences
            farmer: Farmer profile
            env: Environmental/weather context
            crops: Available crop records
            season: Current/target season
            
        Returns:
            Top 3 recommended crops with scores and reasoning
        """
        scored_crops = []
        
        for crop in crops:
            # Score the crop
            score, reasons, risks = self._score_crop(
                crop, farmer, env, season, request.risk_preference
            )
            
            # Build recommendation
            if score > 20:  # Only include viable crops
                recommendation = CropRecommendation(
                    crop_key=crop.crop_key,
                    crop_name=crop.crop_name,
                    crop_name_hi=crop.crop_name_hi,
                    score=round(score, 2),
                    profit_level=crop.profit_level,
                    reasons=reasons,
                    risks=risks,
                    crop_requirements=crop.requirements,
                    seed_material_sources=crop.procurement_sources,
                    sowing_window_hint=self._get_sowing_hint(crop, season),
                    next_best_action=self._get_next_action(crop)
                )
                scored_crops.append(recommendation)
        
        # Sort by score and return top 3
        scored_crops.sort(key=lambda x: x.score, reverse=True)
        return scored_crops[:3]
    
    def _score_crop(
        self,
        crop: CropRecord,
        farmer: FarmerProfile,
        env: EnvironmentalContext,
        season: Season,
        risk_pref: RiskPreference
    ) -> tuple:
        """
        Score a single crop based on multiple factors
        
        Returns:
            (score, reasons, risks)
        """
        score = 0.0
        reasons = []
        risks = list(crop.risks)
        
        # 1. SOIL MATCH (0-30 points)
        soil_score = self._score_soil_match(crop, farmer)
        score += soil_score
        if soil_score > 20:
            reasons.append(f"Excellent soil match ({farmer.soil_type.value})")
        elif soil_score > 10:
            reasons.append(f"Good soil compatibility")
        
        # 2. SEASON MATCH (0-25 points)
        season_score = self._score_season_match(crop, season)
        score += season_score
        if season_score > 20:
            reasons.append(f"Perfect season match ({season.value})")
        elif season_score > 12:
            reasons.append(f"Suitable for current season")
        
        # 3. RAINFALL FIT (0-15 points)
        rain_score = self._score_rainfall_fit(crop, env)
        score += rain_score
        if rain_score > 10:
            reasons.append("Good rainfall alignment")
        elif rain_score < 5 and env.rain_mm_next_7_days < crop.climate.rain_min_mm:
            risks.append("Insufficient rainfall forecast")
        
        # 4. TEMPERATURE FIT (0-10 points)
        temp_score = self._score_temperature_fit(crop, env)
        score += temp_score
        if temp_score > 7:
            reasons.append("Optimal temperature conditions")
        elif temp_score < 3:
            risks.append("Temperature outside ideal range")
        
        # 5. IRRIGATION MATCH (0-10 points)
        irrig_score = self._score_irrigation_match(crop, farmer)
        score += irrig_score
        if irrig_score > 7:
            reasons.append(f"Irrigation system well-suited")
        
        # 6. PROFIT PREFERENCE (0-10 points)
        profit_score = self._score_profit_preference(crop, risk_pref)
        score += profit_score
        if profit_score > 7:
            reasons.append(f"{crop.profit_level.value.title()} profit potential")
        
        # 7. RISK PENALTY (subtract up to 15 points)
        risk_penalty = self._calculate_risk_penalty(crop, risk_pref, env)
        score -= risk_penalty
        
        # Weather-specific risks
        if env.rain_mm_next_7_days > 150 and "rain" in crop.crop_name.lower():
            risks.append("Heavy rainfall may delay operations")
        
        return max(0, score), reasons, risks
    
    def _score_soil_match(self, crop: CropRecord, farmer: FarmerProfile) -> float:
        """Score soil type compatibility"""
        if farmer.soil_type in crop.suitable_soils:
            return self.weights["SOIL_MATCH"]
        
        # Partial score for similar soils
        similar_soils = {
            "alluvial": ["loamy"],
            "loamy": ["alluvial", "clay"],
            "sandy": ["desert"],
        }
        
        soil_name = farmer.soil_type.value
        if soil_name in similar_soils:
            for similar in similar_soils[soil_name]:
                if any(s.value == similar for s in crop.suitable_soils):
                    return self.weights["SOIL_MATCH"] * 0.6
        
        return 0
    
    def _score_season_match(self, crop: CropRecord, season: Season) -> float:
        """Score season compatibility"""
        if season in crop.seasons or Season.YEAR_ROUND in crop.seasons:
            return self.weights["SEASON_MATCH"]
        return 0
    
    def _score_rainfall_fit(self, crop: CropRecord, env: EnvironmentalContext) -> float:
        """Score rainfall alignment"""
        if not crop.climate.rain_min_mm or not crop.climate.rain_max_mm:
            return self.weights["RAINFALL_FIT"] * 0.5  # Unknown, give neutral
        
        rain = env.rain_mm_next_7_days
        rain_min = crop.climate.rain_min_mm
        rain_max = crop.climate.rain_max_mm
        
        if rain_min <= rain <= rain_max:
            return self.weights["RAINFALL_FIT"]
        elif rain < rain_min:
            # Below minimum
            shortage = (rain_min - rain) / rain_min
            return max(0, self.weights["RAINFALL_FIT"] * (1 - shortage))
        else:
            # Above maximum
            excess = (rain - rain_max) / rain_max
            return max(0, self.weights["RAINFALL_FIT"] * (1 - excess * 0.5))
    
    def _score_temperature_fit(self, crop: CropRecord, env: EnvironmentalContext) -> float:
        """Score temperature alignment"""
        if not crop.climate.temp_min_c or not crop.climate.temp_max_c:
            return self.weights["TEMPERATURE_FIT"] * 0.5
        
        temp = env.temperature_c
        temp_min = crop.climate.temp_min_c
        temp_max = crop.climate.temp_max_c
        
        if temp_min <= temp <= temp_max:
            return self.weights["TEMPERATURE_FIT"]
        elif temp < temp_min:
            deviation = (temp_min - temp) / temp_min
            return max(0, self.weights["TEMPERATURE_FIT"] * (1 - deviation))
        else:
            deviation = (temp - temp_max) / temp_max
            return max(0, self.weights["TEMPERATURE_FIT"] * (1 - deviation))
    
    def _score_irrigation_match(self, crop: CropRecord, farmer: FarmerProfile) -> float:
        """Score irrigation system compatibility"""
        if farmer.irrigation_type in crop.irrigation_supported:
            return self.weights["IRRIGATION_MATCH"]
        
        # Partial score for compatible systems
        compatible = {
            "tube_well": ["canal", "sprinkler"],
            "canal": ["tube_well"],
            "drip": ["sprinkler"],
            "sprinkler": ["drip"],
        }
        
        irrig = farmer.irrigation_type.value
        if irrig in compatible:
            for compat in compatible[irrig]:
                if any(i.value == compat for i in crop.irrigation_supported):
                    return self.weights["IRRIGATION_MATCH"] * 0.6
        
        return 0
    
    def _score_profit_preference(self, crop: CropRecord, risk_pref: RiskPreference) -> float:
        """Score based on profit level and risk preference"""
        profit_values = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "very_high": 4
        }
        
        profit_val = profit_values.get(crop.profit_level.value, 2)
        
        if risk_pref == RiskPreference.SAFE:
            # Prefer low-medium profit
            if profit_val <= 2:
                return self.weights["PROFIT_PREFERENCE"]
            return self.weights["PROFIT_PREFERENCE"] * 0.5
        
        elif risk_pref == RiskPreference.BALANCED:
            # Prefer medium
            if profit_val == 2 or profit_val == 3:
                return self.weights["PROFIT_PREFERENCE"]
            return self.weights["PROFIT_PREFERENCE"] * 0.7
        
        else:  # HIGH_PROFIT
            # Prefer high-very_high
            if profit_val >= 3:
                return self.weights["PROFIT_PREFERENCE"]
            return self.weights["PROFIT_PREFERENCE"] * 0.5
    
    def _calculate_risk_penalty(
        self,
        crop: CropRecord,
        risk_pref: RiskPreference,
        env: EnvironmentalContext
    ) -> float:
        """Calculate penalty based on crop risks"""
        risk_count = len(crop.risks)
        
        if risk_pref == RiskPreference.SAFE:
            return risk_count * 3  # Heavy penalty for risky crops
        elif risk_pref == RiskPreference.BALANCED:
            return risk_count * 1.5  # Moderate penalty
        else:  # HIGH_PROFIT
            return risk_count * 0.5  # Light penalty
    
    def _get_sowing_hint(self, crop: CropRecord, season: Season) -> str:
        """Generate sowing window hint"""
        season_windows = {
            Season.KHARIF: "Sow in June-July with onset of monsoon",
            Season.RABI: "Sow in October-November after Kharif harvest",
            Season.ZAID: "Sow in March-April for summer harvest",
            Season.YEAR_ROUND: "Can be sown throughout the year with irrigation"
        }
        
        for s in crop.seasons:
            if s == season or s == Season.YEAR_ROUND:
                return season_windows.get(s, "Consult local agricultural officer for timing")
        
        return "Wait for appropriate season"
    
    def _get_next_action(self, crop: CropRecord) -> str:
        """Generate next best action"""
        return f"Visit nearest seed store or CSC to procure {crop.crop_name} seeds. Get soil tested if not done recently."
