"""
Crop Repository - handles crop encyclopedia data
In production: connects to MongoDB
For hackathon: provides comprehensive mock crop data
"""
from typing import List
from ..models import (
    CropRecord, ClimateRange, CropRequirements, ProcurementSource
)
from ..constants import (
    Season, SoilType, IrrigationType, ProfitLevel, MarketDemand
)


class CropRepository:
    """Repository for crop encyclopedia operations"""
    
    def __init__(self):
        """Initialize with mock crop data"""
        self._crops = self._create_mock_crops()
    
    def list_crops(self) -> List[CropRecord]:
        """
        Get all available crops
        
        Returns:
            List of all crop records
        """
        return self._crops
    
    def get_crop(self, crop_key: str) -> CropRecord:
        """Get specific crop by key"""
        for crop in self._crops:
            if crop.crop_key == crop_key:
                return crop
        return None
    
    def _create_mock_crops(self) -> List[CropRecord]:
        """Create comprehensive mock crop database"""
        return [
            # RICE
            CropRecord(
                crop_key="rice",
                crop_name="Rice (Paddy)",
                crop_name_hi="चावल (धान)",
                seasons=[Season.KHARIF],
                suitable_soils=[SoilType.ALLUVIAL, SoilType.BLACK, SoilType.CLAY, SoilType.LOAMY],
                irrigation_supported=[IrrigationType.CANAL, IrrigationType.TUBE_WELL, IrrigationType.RAINFED],
                climate=ClimateRange(
                    temp_min_c=20,
                    temp_max_c=35,
                    rain_min_mm=100,
                    rain_max_mm=250
                ),
                maturity_days_min=90,
                maturity_days_max=150,
                profit_level=ProfitLevel.MEDIUM,
                market_demand=MarketDemand.VERY_HIGH,
                risks=["Heavy rainfall damage", "Blast disease", "MSP dependency"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=10,
                    fertilizers=["Urea", "DAP", "Potash"],
                    water_requirement="High (flooded conditions)"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Krishi Vigyan Kendra"),
                    ProcurementSource(source_type="private_dealer", name="Local seed dealer"),
                ]
            ),
            
            # WHEAT
            CropRecord(
                crop_key="wheat",
                crop_name="Wheat",
                crop_name_hi="गेहूं",
                seasons=[Season.RABI],
                suitable_soils=[SoilType.ALLUVIAL, SoilType.BLACK, SoilType.LOAMY],
                irrigation_supported=[IrrigationType.CANAL, IrrigationType.TUBE_WELL, IrrigationType.SPRINKLER],
                climate=ClimateRange(
                    temp_min_c=10,
                    temp_max_c=25,
                    rain_min_mm=50,
                    rain_max_mm=100
                ),
                maturity_days_min=110,
                maturity_days_max=140,
                profit_level=ProfitLevel.MEDIUM,
                market_demand=MarketDemand.VERY_HIGH,
                risks=["Terminal heat stress", "Yellow rust", "Aphid attack"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=40,
                    fertilizers=["Urea", "DAP", "MOP"],
                    water_requirement="Moderate (4-6 irrigations)"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Govt. Seed Store"),
                    ProcurementSource(source_type="private_dealer", name="Certified dealers"),
                ]
            ),
            
            # COTTON
            CropRecord(
                crop_key="cotton",
                crop_name="Cotton",
                crop_name_hi="कपास",
                seasons=[Season.KHARIF],
                suitable_soils=[SoilType.BLACK, SoilType.ALLUVIAL, SoilType.RED],
                irrigation_supported=[IrrigationType.DRIP, IrrigationType.CANAL, IrrigationType.RAINFED],
                climate=ClimateRange(
                    temp_min_c=21,
                    temp_max_c=35,
                    rain_min_mm=50,
                    rain_max_mm=150
                ),
                maturity_days_min=150,
                maturity_days_max=180,
                profit_level=ProfitLevel.HIGH,
                market_demand=MarketDemand.HIGH,
                risks=["Pink bollworm", "Whitefly", "Price volatility"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=1.5,
                    fertilizers=["Urea", "DAP", "Potash", "Micronutrients"],
                    water_requirement="Moderate to high"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Agricultural University"),
                    ProcurementSource(source_type="private_dealer", name="Bt Cotton dealers"),
                ]
            ),
            
            # SUGARCANE
            CropRecord(
                crop_key="sugarcane",
                crop_name="Sugarcane",
                crop_name_hi="गन्ना",
                seasons=[Season.YEAR_ROUND],
                suitable_soils=[SoilType.ALLUVIAL, SoilType.BLACK, SoilType.LOAMY],
                irrigation_supported=[IrrigationType.CANAL, IrrigationType.TUBE_WELL, IrrigationType.DRIP],
                climate=ClimateRange(
                    temp_min_c=20,
                    temp_max_c=35,
                    rain_min_mm=150,
                    rain_max_mm=250
                ),
                maturity_days_min=300,
                maturity_days_max=365,
                profit_level=ProfitLevel.HIGH,
                market_demand=MarketDemand.HIGH,
                risks=["Payment delays from mills", "Red rot disease", "High input cost"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=6000,
                    fertilizers=["Urea", "SSP", "MOP", "FYM"],
                    water_requirement="Very high (regular irrigation)"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Cane Research Station"),
                    ProcurementSource(source_type="private_dealer", name="Sugar mill outlets"),
                ]
            ),
            
            # SOYBEAN
            CropRecord(
                crop_key="soybean",
                crop_name="Soybean",
                crop_name_hi="सोयाबीन",
                seasons=[Season.KHARIF],
                suitable_soils=[SoilType.BLACK, SoilType.RED, SoilType.ALLUVIAL],
                irrigation_supported=[IrrigationType.RAINFED, IrrigationType.SPRINKLER],
                climate=ClimateRange(
                    temp_min_c=20,
                    temp_max_c=32,
                    rain_min_mm=50,
                    rain_max_mm=125
                ),
                maturity_days_min=90,
                maturity_days_max=110,
                profit_level=ProfitLevel.MEDIUM,
                market_demand=MarketDemand.HIGH,
                risks=["Yellow mosaic virus", "Girdle beetle", "Price fluctuation"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=30,
                    fertilizers=["DAP", "Potash", "Rhizobium"],
                    water_requirement="Low to moderate"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="ICAR Research Station"),
                    ProcurementSource(source_type="private_dealer", name="Local dealers"),
                ]
            ),
            
            # TOMATO
            CropRecord(
                crop_key="tomato",
                crop_name="Tomato",
                crop_name_hi="टमाटर",
                seasons=[Season.RABI, Season.ZAID],
                suitable_soils=[SoilType.LOAMY, SoilType.SANDY, SoilType.RED],
                irrigation_supported=[IrrigationType.DRIP, IrrigationType.SPRINKLER, IrrigationType.TUBE_WELL],
                climate=ClimateRange(
                    temp_min_c=15,
                    temp_max_c=30,
                    rain_min_mm=20,
                    rain_max_mm=80
                ),
                maturity_days_min=60,
                maturity_days_max=90,
                profit_level=ProfitLevel.VERY_HIGH,
                market_demand=MarketDemand.VERY_HIGH,
                risks=["Price crash during glut", "Tomato leaf curl virus", "Fruit borer"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=0.15,
                    fertilizers=["Urea", "DAP", "Potash", "Organic manure"],
                    water_requirement="Moderate (frequent light irrigation)"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Horticulture Dept"),
                    ProcurementSource(source_type="online", name="AgroStar, BigHaat"),
                ]
            ),
            
            # ONION
            CropRecord(
                crop_key="onion",
                crop_name="Onion",
                crop_name_hi="प्याज",
                seasons=[Season.RABI, Season.KHARIF],
                suitable_soils=[SoilType.LOAMY, SoilType.SANDY, SoilType.BLACK],
                irrigation_supported=[IrrigationType.DRIP, IrrigationType.SPRINKLER, IrrigationType.TUBE_WELL],
                climate=ClimateRange(
                    temp_min_c=13,
                    temp_max_c=28,
                    rain_min_mm=30,
                    rain_max_mm=100
                ),
                maturity_days_min=90,
                maturity_days_max=150,
                profit_level=ProfitLevel.HIGH,
                market_demand=MarketDemand.VERY_HIGH,
                risks=["Export ban risk", "Purple blotch", "Storage losses"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=4,
                    fertilizers=["Urea", "SSP", "MOP"],
                    water_requirement="Moderate (critical at bulb formation)"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Vegetable Research Station"),
                    ProcurementSource(source_type="private_dealer", name="Hybrid seed companies"),
                ]
            ),
            
            # POTATO
            CropRecord(
                crop_key="potato",
                crop_name="Potato",
                crop_name_hi="आलू",
                seasons=[Season.RABI],
                suitable_soils=[SoilType.LOAMY, SoilType.SANDY, SoilType.ALLUVIAL],
                irrigation_supported=[IrrigationType.SPRINKLER, IrrigationType.TUBE_WELL, IrrigationType.DRIP],
                climate=ClimateRange(
                    temp_min_c=15,
                    temp_max_c=25,
                    rain_min_mm=50,
                    rain_max_mm=100
                ),
                maturity_days_min=80,
                maturity_days_max=120,
                profit_level=ProfitLevel.HIGH,
                market_demand=MarketDemand.VERY_HIGH,
                risks=["Late blight disease", "Cold storage costs", "Market glut"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=600,
                    fertilizers=["Urea", "DAP", "MOP", "Organic compost"],
                    water_requirement="Moderate (regular light irrigation)"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Potato Research Station"),
                    ProcurementSource(source_type="private_dealer", name="Certified seed tuber dealers"),
                ]
            ),
            
            # MUSTARD
            CropRecord(
                crop_key="mustard",
                crop_name="Mustard",
                crop_name_hi="सरसों",
                seasons=[Season.RABI],
                suitable_soils=[SoilType.LOAMY, SoilType.SANDY, SoilType.ALLUVIAL],
                irrigation_supported=[IrrigationType.RAINFED, IrrigationType.TUBE_WELL, IrrigationType.CANAL],
                climate=ClimateRange(
                    temp_min_c=10,
                    temp_max_c=25,
                    rain_min_mm=25,
                    rain_max_mm=60
                ),
                maturity_days_min=90,
                maturity_days_max=120,
                profit_level=ProfitLevel.MEDIUM,
                market_demand=MarketDemand.MEDIUM,
                risks=["Aphid infestation", "Alternaria blight", "Bird damage"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=2,
                    fertilizers=["Urea", "DAP", "Sulfur"],
                    water_requirement="Low (1-2 irrigations)"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Oilseed Research Station"),
                    ProcurementSource(source_type="private_dealer", name="Local seed shops"),
                ]
            ),
            
            # GROUNDNUT
            CropRecord(
                crop_key="groundnut",
                crop_name="Groundnut (Peanut)",
                crop_name_hi="मूंगफली",
                seasons=[Season.KHARIF, Season.ZAID],
                suitable_soils=[SoilType.SANDY, SoilType.LOAMY, SoilType.RED],
                irrigation_supported=[IrrigationType.RAINFED, IrrigationType.SPRINKLER, IrrigationType.DRIP],
                climate=ClimateRange(
                    temp_min_c=20,
                    temp_max_c=30,
                    rain_min_mm=50,
                    rain_max_mm=125
                ),
                maturity_days_min=100,
                maturity_days_max=140,
                profit_level=ProfitLevel.MEDIUM,
                market_demand=MarketDemand.HIGH,
                risks=["Aflatoxin contamination", "Tikka disease", "Pod borer"],
                requirements=CropRequirements(
                    seed_rate_kg_per_acre=40,
                    fertilizers=["DAP", "Gypsum", "Rhizobium"],
                    water_requirement="Moderate"
                ),
                procurement_sources=[
                    ProcurementSource(source_type="govt_store", name="Groundnut Research Station"),
                    ProcurementSource(source_type="private_dealer", name="Certified dealers"),
                ]
            ),
        ]
