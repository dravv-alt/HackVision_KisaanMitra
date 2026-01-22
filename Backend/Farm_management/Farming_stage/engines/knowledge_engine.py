"""
Knowledge Engine - The Decision Brain
Handles irrigation advice, input optimization, and harvest planning
"""

from datetime import date, timedelta
from typing import Optional
from ..models import (
    CropContext, EnvironmentalContext, MarketContext, AdvisoryOutput,
    CropStage, PriceTrend, UrgencyLevel
)


class KnowledgeEngine:
    """
    Core decision-making engine for farming recommendations
    Implements three key features:
    1. Irrigation Advisor
    2. Input Optimizer (Fertilizer/Pesticide)
    3. Harvest Planner
    """
    
    def __init__(self, use_llm: bool = False, llm_api_key: Optional[str] = None):
        """
        Initialize knowledge engine
        
        Args:
            use_llm: Whether to use LLM for complex queries (optional)
            llm_api_key: API key for LLM service (optional)
        """
        self.use_llm = use_llm
        self.llm_api_key = llm_api_key
    
    # ==================== FEATURE A: IRRIGATION ADVISOR ====================
    
    def get_irrigation_advice(
        self,
        crop: CropContext,
        environment: EnvironmentalContext
    ) -> AdvisoryOutput:
        """
        Provide irrigation recommendations based on weather and crop stage
        
        Args:
            crop: Current crop context
            environment: Weather conditions
            
        Returns:
            AdvisoryOutput with irrigation instructions
        """
        # Rain forecast - stop irrigation
        if environment.rain_forecast:
            return AdvisoryOutput(
                action_header="STOP IRRIGATION",
                spoken_advice=f"Rain is forecast in the next 24-48 hours. Stop irrigation for your {crop.name} crop to avoid waterlogging.",
                detailed_reasoning="Natural rainfall will provide sufficient moisture. Over-watering during rain can lead to root rot and fungal diseases.",
                urgency=UrgencyLevel.MODERATE
            )
        
        # High humidity - reduce irrigation
        if environment.humidity > 80:
            return AdvisoryOutput(
                action_header="REDUCE IRRIGATION",
                spoken_advice=f"Humidity is very high at {environment.humidity}%. Reduce irrigation frequency for your {crop.name}.",
                detailed_reasoning="High humidity reduces evapotranspiration. Excess watering in humid conditions increases disease risk.",
                urgency=UrgencyLevel.INFO
            )
        
        # Stage-based irrigation recommendations
        irrigation_schedule = self._get_stage_irrigation(crop, environment)
        
        return irrigation_schedule
    
    def _get_stage_irrigation(
        self,
        crop: CropContext,
        environment: EnvironmentalContext
    ) -> AdvisoryOutput:
        """
        Get irrigation schedule based on crop growth stage
        """
        stage = crop.current_stage
        temp = environment.temperature
        
        # Adjust for temperature
        temp_factor = "increased" if temp > 35 else "normal"
        
        if stage in [CropStage.SOWING, CropStage.GERMINATION]:
            return AdvisoryOutput(
                action_header="LIGHT FREQUENT WATERING",
                spoken_advice=f"Your {crop.name} is in {stage.value} stage. Water lightly every day to keep soil moist.",
                detailed_reasoning=f"Early stages require consistent moisture for seed germination and root establishment. Temperature: {temp}°C.",
                urgency=UrgencyLevel.HIGH
            )
        
        elif stage == CropStage.VEGETATIVE:
            frequency = "daily" if temp > 35 else "every 2 days"
            amount = "7-10 liters" if temp > 35 else "5-7 liters"
            
            return AdvisoryOutput(
                action_header="REGULAR IRRIGATION",
                spoken_advice=f"Water your {crop.name} {frequency}, approximately {amount} per plant.",
                detailed_reasoning=f"Vegetative growth requires consistent water supply. Current temperature {temp}°C requires {temp_factor} watering.",
                urgency=UrgencyLevel.MODERATE
            )
        
        elif stage == CropStage.FLOWERING:
            return AdvisoryOutput(
                action_header="CRITICAL IRRIGATION PERIOD",
                spoken_advice=f"Your {crop.name} is flowering. Maintain daily watering schedule - do not let soil dry out.",
                detailed_reasoning="Flowering stage is most water-sensitive. Water stress now will reduce fruit set and yield significantly.",
                urgency=UrgencyLevel.CRITICAL
            )
        
        elif stage == CropStage.FRUITING:
            return AdvisoryOutput(
                action_header="MODERATE IRRIGATION",
                spoken_advice=f"Water your {crop.name} every 2-3 days. Avoid overwatering to improve fruit quality.",
                detailed_reasoning="Fruiting stage needs balanced moisture. Slight water stress can improve fruit sweetness and shelf life.",
                urgency=UrgencyLevel.MODERATE
            )
        
        elif stage in [CropStage.MATURATION, CropStage.HARVEST_READY]:
            return AdvisoryOutput(
                action_header="REDUCE IRRIGATION",
                spoken_advice=f"Your {crop.name} is nearing harvest. Reduce watering to once every 4-5 days.",
                detailed_reasoning="Reduced irrigation before harvest improves storage quality and reduces disease risk during harvest.",
                urgency=UrgencyLevel.INFO
            )
        
        # Default
        return AdvisoryOutput(
            action_header="MONITOR SOIL MOISTURE",
            spoken_advice=f"Check soil moisture daily and water when top 2 inches feel dry.",
            detailed_reasoning="General recommendation for current stage.",
            urgency=UrgencyLevel.INFO
        )
    
    # ==================== FEATURE B: INPUT OPTIMIZER ====================
    
    def get_treatment_recommendation(
        self,
        disease_name: Optional[str] = None,
        crop_stage: Optional[CropStage] = None,
        crop_name: str = "crop"
    ) -> AdvisoryOutput:
        """
        Recommend fertilizer or pesticide treatment
        MUST include: exact dosage, safety warning, organic alternative
        
        Args:
            disease_name: Detected disease (if any)
            crop_stage: Current growth stage (for fertilizer)
            crop_name: Name of crop
            
        Returns:
            AdvisoryOutput with complete treatment plan
        """
        if disease_name and disease_name.lower() != "healthy":
            return self._get_disease_treatment(disease_name, crop_name)
        
        if crop_stage:
            return self._get_stage_fertilizer(crop_stage, crop_name)
        
        # Default general advice
        return AdvisoryOutput(
            action_header="ROUTINE MONITORING",
            spoken_advice="Continue regular crop monitoring. No immediate treatment needed.",
            detailed_reasoning="Crop appears healthy. Maintain preventive care schedule.",
            urgency=UrgencyLevel.INFO
        )
    
    def _get_disease_treatment(self, disease_name: str, crop_name: str) -> AdvisoryOutput:
        """
        Provide disease-specific treatment with all required fields
        """
        disease_treatments = {
            "Leaf Blight": {
                "chemical": "Mancozeb",
                "dosage": "Mancozeb 75% WP: 2g per liter of water. Spray 200-250mL solution per square meter of crop area.",
                "safety": "Do not spray in windy conditions (wind speed >15km/h). Wear protective gloves and mask. Avoid spraying during peak sun (10am-4pm). Wait 7 days before harvest.",
                "organic": "Neem oil solution: Mix 30mL pure neem oil + 5mL liquid soap per liter of water. Spray in early morning. Repeat every 5 days.",
                "urgency": UrgencyLevel.HIGH
            },
            "Powdery Mildew": {
                "chemical": "Sulfur",
                "dosage": "Wettable Sulfur 80% WP: 3g per liter of water. Apply 150-200mL per square meter. Repeat every 10 days.",
                "safety": "Do not apply when temperature exceeds 35°C (risk of leaf burn). Wear dust mask during mixing. Safe for harvest after 3 days.",
                "organic": "Baking soda spray: 1 tablespoon baking soda + 1 tablespoon vegetable oil + 1 drop dish soap per liter of water. Spray weekly.",
                "urgency": UrgencyLevel.MODERATE
            },
            "Bacterial Spot": {
                "chemical": "Copper Oxychloride",
                "dosage": "Copper Oxychloride 50% WP: 2.5g per liter of water. Spray thoroughly covering both leaf surfaces. 200mL per plant.",
                "safety": "Highly toxic to aquatic life - do not spray near water bodies. Wear full protective gear. Do not mix with other chemicals. 14-day pre-harvest interval.",
                "organic": "Garlic-chili spray: Blend 10 garlic cloves + 2 hot chilies in 1L water, strain, add 1 tsp soap. Spray every 3 days for 2 weeks.",
                "urgency": UrgencyLevel.CRITICAL
            },
            "Early Blight": {
                "chemical": "Chlorothalonil",
                "dosage": "Chlorothalonil 75% WP: 2g per liter of water. Apply 250mL per square meter. Start at first sign, repeat every 7-10 days.",
                "safety": "Avoid skin contact - causes irritation. Do not spray before rain. Wear waterproof gloves. 7-day waiting period before harvest.",
                "organic": "Compost tea: Steep 1kg mature compost in 5L water for 3 days, strain, dilute 1:5 with water. Spray weekly as preventive.",
                "urgency": UrgencyLevel.HIGH
            }
        }
        
        treatment = disease_treatments.get(disease_name, {
            "chemical": "Broad-spectrum fungicide",
            "dosage": "Follow manufacturer's instructions. Typically 2-3g per liter of water.",
            "safety": "Wear protective equipment. Avoid spraying in windy conditions. Maintain pre-harvest interval as per label.",
            "organic": "Neem oil solution (30mL/L) or baking soda spray (1 tbsp/L) as general organic treatment.",
            "urgency": UrgencyLevel.MODERATE
        })
        
        return AdvisoryOutput(
            action_header=f"TREAT {disease_name.upper()}",
            spoken_advice=f"Your {crop_name} has {disease_name}. Apply {treatment['chemical']} treatment immediately to prevent spread.",
            detailed_reasoning=f"{disease_name} can spread rapidly and cause significant yield loss if left untreated. Early intervention is critical.",
            urgency=treatment["urgency"],
            chemical_dosage=treatment["dosage"],
            safety_warning=treatment["safety"],
            organic_alternative=treatment["organic"]
        )
    
    def _get_stage_fertilizer(self, stage: CropStage, crop_name: str) -> AdvisoryOutput:
        """
        Provide stage-specific fertilizer recommendations
        """
        if stage in [CropStage.SOWING, CropStage.GERMINATION]:
            return AdvisoryOutput(
                action_header="STARTER FERTILIZER",
                spoken_advice=f"Apply phosphorus-rich starter fertilizer for your {crop_name} seedlings.",
                detailed_reasoning="Phosphorus promotes root development in early stages.",
                urgency=UrgencyLevel.MODERATE,
                chemical_dosage="DAP (Diammonium Phosphate): 50g per square meter, mixed into soil before sowing. Or NPK 10:26:26 at 40g per sq.m.",
                safety_warning="Avoid direct contact with seeds - maintain 2-inch gap. Over-application can burn seedlings. Water immediately after application.",
                organic_alternative="Bone meal: 100g per square meter mixed into soil. Or vermicompost: 2kg per square meter as base fertilizer."
            )
        
        elif stage == CropStage.VEGETATIVE:
            return AdvisoryOutput(
                action_header="NITROGEN BOOST",
                spoken_advice=f"Your {crop_name} needs nitrogen for leaf growth. Apply nitrogen-rich fertilizer.",
                detailed_reasoning="Vegetative stage requires high nitrogen for rapid leaf and stem development.",
                urgency=UrgencyLevel.MODERATE,
                chemical_dosage="Urea (46% N): 100g per 10 square meters, broadcast and water immediately. Or NPK 20:10:10 at 150g per 10 sq.m. Apply every 15 days.",
                safety_warning="Do not apply on wet leaves (causes burn). Apply in evening. Water within 2 hours to prevent nitrogen loss. Keep away from stem base.",
                organic_alternative="Homemade nitrogen tea: Soak 1kg fresh grass clippings in 10L water for 5 days, dilute 1:3, apply 500mL per plant weekly."
            )
        
        elif stage == CropStage.FLOWERING:
            return AdvisoryOutput(
                action_header="BLOOM BOOSTER",
                spoken_advice=f"Apply potassium and phosphorus fertilizer to support flowering in your {crop_name}.",
                detailed_reasoning="Flowering requires phosphorus for flower formation and potassium for fruit set.",
                urgency=UrgencyLevel.HIGH,
                chemical_dosage="NPK 13:40:13 or 10:52:10: 100g per 10 square meters. Dissolve in water (10g per liter) and drench soil around plants. Apply twice, 10 days apart.",
                safety_warning="Do not spray on flowers - apply to soil only. Avoid application during peak heat. Maintain soil moisture before application.",
                organic_alternative="Wood ash (potassium source): 50g per plant sprinkled around base. Banana peel tea: Soak 5 peels in 5L water for 3 days, use as drench."
            )
        
        elif stage == CropStage.FRUITING:
            return AdvisoryOutput(
                action_header="FRUIT DEVELOPMENT FEED",
                spoken_advice=f"Apply balanced fertilizer with extra potassium for fruit development in your {crop_name}.",
                detailed_reasoning="Potassium improves fruit size, quality, and disease resistance.",
                urgency=UrgencyLevel.MODERATE,
                chemical_dosage="NPK 19:19:19 or 13:0:45 (potassium-rich): 80g per 10 square meters every 2 weeks. Can also foliar spray: 5g per liter water.",
                safety_warning="For foliar spray: apply in early morning or late evening only. Do not spray on fruits directly. Avoid during fruit maturation phase.",
                organic_alternative="Compost tea: 2kg mature compost in 10L water, ferment 7 days, dilute 1:5, apply 1L per plant. Seaweed extract: 20mL per liter water as foliar spray."
            )
        
        else:  # Maturation, Harvest Ready
            return AdvisoryOutput(
                action_header="STOP FERTILIZATION",
                spoken_advice=f"Your {crop_name} is nearing harvest. Stop all fertilizer applications now.",
                detailed_reasoning="Late-stage fertilization can reduce fruit quality, delay ripening, and affect storage life.",
                urgency=UrgencyLevel.INFO,
                chemical_dosage="No chemical fertilizer needed at this stage.",
                safety_warning="Avoid any nitrogen application - it will delay harvest and reduce fruit sweetness.",
                organic_alternative="If needed, apply only light compost mulch (1-inch layer) to maintain soil health for next crop."
            )
    
    # ==================== FEATURE C: HARVEST PLANNER ====================
    
    def plan_harvest(
        self,
        environment: EnvironmentalContext,
        market: MarketContext,
        storage_available: bool,
        crop_name: str = "crop"
    ) -> AdvisoryOutput:
        """
        Decision tree for optimal harvest timing
        
        Args:
            environment: Weather conditions
            market: Market price and trends
            storage_available: Whether farmer has storage facility
            crop_name: Name of crop
            
        Returns:
            AdvisoryOutput with harvest decision
        """
        # Priority 1: Rain incoming - DELAY
        if environment.rain_forecast:
            return AdvisoryOutput(
                action_header="DELAY HARVEST - RAIN FORECAST",
                spoken_advice=f"Rain is forecast in next 24-48 hours. Delay harvesting your {crop_name} until weather clears.",
                detailed_reasoning="Harvesting during or just before rain increases moisture content, leading to faster spoilage, fungal growth during storage, and reduced market value. Wait for 2-3 dry days after rain.",
                urgency=UrgencyLevel.CRITICAL
            )
        
        # Priority 2: Price rising + has storage - DELAY for profit
        if market.price_trend == PriceTrend.RISING and storage_available:
            forecast_increase = round(market.current_price * 1.08, 2)  # Assume 8% increase
            
            return AdvisoryOutput(
                action_header="DELAY HARVEST - WAIT FOR BETTER PRICES",
                spoken_advice=f"Market prices for {crop_name} are rising. You have storage, so wait 5-7 days for better rates.",
                detailed_reasoning=f"Current price: ₹{market.current_price}/kg. Trend: {market.price_trend.value}. Expected price in 7 days: ₹{forecast_increase}/kg. Your storage facility allows you to wait for optimal pricing.",
                urgency=UrgencyLevel.MODERATE
            )
        
        # Priority 3: Price falling - SELL NOW
        if market.price_trend == PriceTrend.FALLING:
            return AdvisoryOutput(
                action_header="HARVEST & SELL IMMEDIATELY",
                spoken_advice=f"Market prices for {crop_name} are declining. Harvest and sell immediately to avoid losses.",
                detailed_reasoning=f"Current price: ₹{market.current_price}/kg. Trend: FALLING. Prices may drop 8-12% in coming week. Immediate sale recommended even if crop could mature further.",
                urgency=UrgencyLevel.HIGH
            )
        
        # Priority 4: Clear weather + high price - HARVEST NOW
        if not environment.rain_forecast and market.current_price > 30:  # Threshold for "high price"
            return AdvisoryOutput(
                action_header="HARVEST NOW - OPTIMAL CONDITIONS",
                spoken_advice=f"Weather is clear and {crop_name} prices are good at ₹{market.current_price}/kg. Harvest now.",
                detailed_reasoning=f"Ideal conditions: Clear weather (temp: {environment.temperature}°C, humidity: {environment.humidity}%), good market price, stable trend. This is the optimal harvest window.",
                urgency=UrgencyLevel.HIGH
            )
        
        # Priority 5: No storage + rising prices - HARVEST NOW (can't wait)
        if market.price_trend == PriceTrend.RISING and not storage_available:
            return AdvisoryOutput(
                action_header="HARVEST NOW - NO STORAGE",
                spoken_advice=f"Although prices are rising, harvest your {crop_name} now since you don't have storage facilities.",
                detailed_reasoning=f"Without proper storage, waiting for higher prices risks crop deterioration and total loss. Current price ₹{market.current_price}/kg is acceptable. Sell fresh for best quality.",
                urgency=UrgencyLevel.MODERATE
            )
        
        # Default: Monitor and wait
        return AdvisoryOutput(
            action_header="MONITOR CLOSELY",
            spoken_advice=f"Continue monitoring your {crop_name}. Check weather and prices daily for optimal harvest timing.",
            detailed_reasoning=f"Current conditions: Weather stable, price ₹{market.current_price}/kg (trend: {market.price_trend.value}). Wait for clearer signals before harvesting.",
            urgency=UrgencyLevel.INFO
        )
