"""
Scheme API Client with Mock Fallback
Fetches schemes from external API or returns mock data
"""

import requests
from typing import List, Dict, Any
import logging
from datetime import datetime, timedelta
import uuid

from ..models import SchemeRecord
from ..constants import SchemeCategory
from ..config import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SchemeAPIClient:
    """
    API client for fetching government schemes
    Integrated with data.gov.in for real-time data
    """
    
    def __init__(self):
        self.settings = get_settings()
    
    def fetch_schemes(self) -> List[SchemeRecord]:
        """
        Fetch schemes from API or return mock data based on configuration.
        Ensures the demo never fails by falling back to mock data.
        """
        # Forced override for demo purposes if keys aren't loaded properly
        # But here we assume they are loaded via settings.
        
        if self.settings.is_mock_mode():
            logger.info("Running in MOCK_MODE: Fetching mock schemes.")
            return self._get_mock_schemes()
        
        try:
            logger.info(f"Attempting to fetch schemes from Data.gov.in")
            schemes = self._fetch_from_real_api()
            if not schemes:
                logger.warning("API returned empty list, falling back to mock schemes.")
                return self._get_mock_schemes()
            return schemes
        except Exception as e:
            logger.error(f"API fetch failed: {str(e)}. Falling back to mock schemes.")
            return self._get_mock_schemes()

    def _fetch_from_real_api(self) -> List[SchemeRecord]:
        """
        Real API integration for data.gov.in
        """
        # Get credentials from settings
        api_key = self.settings.schemes_api_key
        resource_id = self.settings.schemes_resource_id
        
        if not api_key or not resource_id:
             logger.warning("Missing API Key or Resource ID for data.gov.in")
             return []

        # Construct URL for data.gov.in
        # typical format: https://api.data.gov.in/resource/{resource_id}?api-key={key}&format=json
        base_url = "https://api.data.gov.in/resource/" + resource_id
        params = {
            "api-key": api_key,
            "format": "json",
            "limit": 10  # Limit to 10 for safety/speed
        }

        response = requests.get(
            base_url,
            params=params,
            timeout=self.settings.api_timeout
        )
        
        response.raise_for_status()
        data = response.json()
        
        # data.gov.in responses usually have a "records" list inside
        records = data.get("records", [])
        
        # We need to map these dynamic records to our SchemeRecord model
        # The field names from data.gov.in vary by dataset. 
        # We'll do a best-effort mapping or partial logic.
        
        mapped_schemes = []
        for item in records:
            # Fallback logic to find 'title' or 'name' fields
            scheme_name = item.get("scheme_name") or item.get("title") or item.get("name") or "Unknown Scheme"
            desc = item.get("description") or item.get("details") or "No description available"
            # Using defaults for other fields not guaranteed in dataset
            
            scheme = SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName=scheme_name,
                category=SchemeCategory.SUBSIDY, # Defaulting category as inference is hard
                description=desc,
                state=item.get("state_name"),
                benefits="Check official details",
                officialLink=item.get("url") or item.get("link") or "https://mylibrary.data.gov.in",
                isActive=True
            )
            mapped_schemes.append(scheme)

        return mapped_schemes
    
    def _get_mock_schemes(self) -> List[SchemeRecord]:
        """
        Generate comprehensive mock scheme data
        Covers various categories, states, and scenarios
        """
        now = datetime.now()
        
        mock_schemes = [
            # All-India Schemes
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                schemeNameHindi="प्रधानमंत्री किसान सम्मान निधि",
                category=SchemeCategory.SUBSIDY,
                description="Income support of ₹6000 per year to all farmer families",
                descriptionHindi="सभी किसान परिवारों को प्रति वर्ष ₹6000 की आय सहायता",
                state=None,  # All India
                district=None,
                benefits="₹2000 every 4 months directly to bank account",
                benefitsHindi="हर 4 महीने में ₹2000 सीधे बैंक खाते में",
                eligibility="All landholding farmer families",
                eligibilityHindi="सभी भूमिधारक किसान परिवार",
                howToApply="Register at PM-KISAN portal or CSC",
                howToApplyHindi="PM-KISAN पोर्टल या CSC पर पंजीकरण करें",
                officialLink="https://pmkisan.gov.in",
                contactNumber="155261",
                startDate=now - timedelta(days=365),
                endDate=None,  # Ongoing
                isActive=True,
                createdAt=now - timedelta(days=365)
            ),
            
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                schemeNameHindi="प्रधानमंत्री फसल बीमा योजना",
                category=SchemeCategory.INSURANCE,
                description="Crop insurance scheme providing financial support to farmers",
                descriptionHindi="किसानों को वित्तीय सहायता प्रदान करने वाली फसल बीमा योजना",
                state=None,
                district=None,
                benefits="Comprehensive risk insurance at low premium",
                benefitsHindi="कम प्रीमियम पर व्यापक जोखिम बीमा",
                eligibility="All farmers growing notified crops",
                eligibilityHindi="अधिसूचित फसलें उगाने वाले सभी किसान",
                howToApply="Through banks, CSCs, or insurance companies",
                howToApplyHindi="बैंकों, CSC, या बीमा कंपनियों के माध्यम से",
                officialLink="https://pmfby.gov.in",
                contactNumber="1800-180-1551",
                isActive=True,
                createdAt=now - timedelta(days=300)
            ),
            
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Soil Health Card Scheme",
                schemeNameHindi="मृदा स्वास्थ्य कार्ड योजना",
                category=SchemeCategory.SOIL,
                description="Free soil testing and health cards for farmers",
                descriptionHindi="किसानों के लिए मुफ्त मिट्टी परीक्षण और स्वास्थ्य कार्ड",
                state=None,
                district=None,
                benefits="Know soil nutrients and get fertilizer recommendations",
                benefitsHindi="मिट्टी के पोषक तत्व जानें और उर्वरक सिफारिशें प्राप्त करें",
                eligibility="All farmers",
                eligibilityHindi="सभी किसान",
                howToApply="Contact nearest soil testing lab or agriculture office",
                howToApplyHindi="निकटतम मिट्टी परीक्षण प्रयोगशाला या कृषि कार्यालय से संपर्क करें",
                officialLink="https://soilhealth.dac.gov.in",
                isActive=True,
                createdAt=now - timedelta(days=200)
            ),
            
            # Maharashtra-specific schemes
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Maharashtra Krishi Samruddhi Yojana",
                schemeNameHindi="महाराष्ट्र कृषि समृद्धि योजना",
                category=SchemeCategory.SUBSIDY,
                description="State subsidy for agricultural equipment and infrastructure",
                descriptionHindi="कृषि उपकरण और बुनियादी ढांचे के लिए राज्य सब्सिडी",
                state="Maharashtra",
                district=None,
                benefits="50% subsidy on farm equipment up to ₹1 lakh",
                benefitsHindi="₹1 लाख तक कृषि उपकरण पर 50% सब्सिडी",
                eligibility="Maharashtra farmers with valid documents",
                eligibilityHindi="वैध दस्तावेजों वाले महाराष्ट्र के किसान",
                howToApply="Apply through Maharashtra agriculture portal",
                howToApplyHindi="महाराष्ट्र कृषि पोर्टल के माध्यम से आवेदन करें",
                officialLink="https://krishi.maharashtra.gov.in",
                isActive=True,
                createdAt=now - timedelta(days=150)
            ),
            
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Nashik Drip Irrigation Subsidy",
                schemeNameHindi="नासिक ड्रिप सिंचाई सब्सिडी",
                category=SchemeCategory.SUBSIDY,
                description="District-level subsidy for drip irrigation systems",
                descriptionHindi="ड्रिप सिंचाई प्रणाली के लिए जिला स्तरीय सब्सिडी",
                state="Maharashtra",
                district="Nashik",
                benefits="60% subsidy on drip irrigation installation",
                benefitsHindi="ड्रिप सिंचाई स्थापना पर 60% सब्सिडी",
                eligibility="Nashik district farmers with minimum 1 acre land",
                eligibilityHindi="न्यूनतम 1 एकड़ भूमि वाले नासिक जिले के किसान",
                howToApply="Apply at district agriculture office",
                howToApplyHindi="जिला कृषि कार्यालय में आवेदन करें",
                contactNumber="0253-2506000",
                startDate=now - timedelta(days=60),
                endDate=now + timedelta(days=120),
                isActive=True,
                createdAt=now - timedelta(days=10)  # New scheme!
            ),
            
            # Punjab-specific schemes
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Punjab Crop Diversification Scheme",
                schemeNameHindi="पंजाब फसल विविधीकरण योजना",
                category=SchemeCategory.TRAINING,
                description="Incentives for shifting from paddy to alternative crops",
                descriptionHindi="धान से वैकल्पिक फसलों में स्थानांतरण के लिए प्रोत्साहन",
                state="Punjab",
                district=None,
                benefits="₹1500 per acre for crop diversification",
                benefitsHindi="फसल विविधीकरण के लिए ₹1500 प्रति एकड़",
                eligibility="Punjab farmers willing to diversify crops",
                eligibilityHindi="फसल विविधीकरण के इच्छुक पंजाब के किसान",
                howToApply="Register at Punjab agriculture department",
                howToApplyHindi="पंजाब कृषि विभाग में पंजीकरण करें",
                isActive=True,
                createdAt=now - timedelta(days=100)
            ),
            
            # Loan schemes
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Kisan Credit Card (KCC)",
                schemeNameHindi="किसान क्रेडिट कार्ड",
                category=SchemeCategory.LOAN,
                description="Credit facility for farmers at subsidized interest rates",
                descriptionHindi="रियायती ब्याज दरों पर किसानों के लिए ऋण सुविधा",
                state=None,
                district=None,
                benefits="Loan up to ₹3 lakh at 4% interest (with subsidy)",
                benefitsHindi="4% ब्याज पर ₹3 लाख तक का ऋण (सब्सिडी के साथ)",
                eligibility="Farmers with land ownership or tenancy",
                eligibilityHindi="भूमि स्वामित्व या किरायेदारी वाले किसान",
                howToApply="Apply at any bank branch",
                howToApplyHindi="किसी भी बैंक शाखा में आवेदन करें",
                officialLink="https://www.nabard.org/kcc",
                isActive=True,
                createdAt=now - timedelta(days=400)
            ),
            
            # Fertilizer schemes
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Nutrient Based Subsidy (NBS)",
                schemeNameHindi="पोषक तत्व आधारित सब्सिडी",
                category=SchemeCategory.FERTILIZER,
                description="Subsidy on fertilizers based on nutrient content",
                descriptionHindi="पोषक तत्व सामग्री के आधार पर उर्वरकों पर सब्सिडी",
                state=None,
                district=None,
                benefits="Reduced fertilizer prices at retail outlets",
                benefitsHindi="खुदरा दुकानों पर कम उर्वरक कीमतें",
                eligibility="All farmers purchasing fertilizers",
                eligibilityHindi="उर्वरक खरीदने वाले सभी किसान",
                howToApply="Buy from authorized dealers with Aadhaar",
                howToApplyHindi="आधार के साथ अधिकृत डीलरों से खरीदें",
                isActive=True,
                createdAt=now - timedelta(days=250)
            ),
            
            # Recently added scheme (for alert testing)
            SchemeRecord(
                schemeId=str(uuid.uuid4()),
                schemeName="Digital Agriculture Mission 2024",
                schemeNameHindi="डिजिटल कृषि मिशन 2024",
                category=SchemeCategory.TRAINING,
                description="Training on digital farming tools and technologies",
                descriptionHindi="डिजिटल कृषि उपकरण और प्रौद्योगिकियों पर प्रशिक्षण",
                state=None,
                district=None,
                benefits="Free training and digital tools worth ₹5000",
                benefitsHindi="मुफ्त प्रशिक्षण और ₹5000 मूल्य के डिजिटल उपकरण",
                eligibility="Farmers interested in digital agriculture",
                eligibilityHindi="डिजिटल कृषि में रुचि रखने वाले किसान",
                howToApply="Register online at digital agriculture portal",
                howToApplyHindi="डिजिटल कृषि पोर्टल पर ऑनलाइन पंजीकरण करें",
                startDate=now - timedelta(days=5),
                endDate=now + timedelta(days=90),
                isActive=True,
                createdAt=now - timedelta(days=2)  # Very new!
            ),
        ]
        
        return mock_schemes
