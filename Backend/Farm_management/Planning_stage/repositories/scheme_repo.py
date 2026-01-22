"""
Scheme Repository - handles government scheme data
In production: connects to MongoDB
For hackathon: provides comprehensive mock scheme data
"""
from typing import List
from datetime import datetime, timedelta
from ..models import SchemeRecord


class SchemeRepository:
    """Repository for government scheme operations"""
    
    def __init__(self):
        """Initialize with mock scheme data"""
        self._schemes = self._create_mock_schemes()
    
    def list_schemes(self) -> List[SchemeRecord]:
        """
        Get all available government schemes
        
        Returns:
            List of all scheme records
        """
        return self._schemes
    
    def get_scheme(self, scheme_key: str) -> SchemeRecord:
        """Get specific scheme by key"""
        for scheme in self._schemes:
            if scheme.scheme_key == scheme_key:
                return scheme
        return None
    
    def _create_mock_schemes(self) -> List[SchemeRecord]:
        """Create comprehensive mock scheme database"""
        # Create realistic deadlines (some urgent, some not)
        today = datetime.now()
        
        return [
            # PM-KISAN
            SchemeRecord(
                scheme_key="pm_kisan",
                scheme_name="PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
                scheme_name_hi="प्रधानमंत्री किसान सम्मान निधि",
                description="Direct income support of Rs 6,000/year in 3 installments to all landholding farmers",
                description_hi="सभी भूमिधारक किसानों को 3 किश्तों में 6,000 रुपये प्रति वर्ष की प्रत्यक्ष आय सहायता",
                benefits=[
                    "Rs 2,000 every 4 months",
                    "Direct bank transfer (DBT)",
                    "No cost involved"
                ],
                benefits_hi=[
                    "हर 4 महीने में 2,000 रुपये",
                    "सीधे बैंक खाते में",
                    "कोई लागत नहीं"
                ],
                deadline=None,  # Always open
                docs_required=[
                    "Aadhaar card",
                    "Bank account passbook",
                    "Land ownership documents"
                ],
                eligibility_rules={
                    "land_holder": True,
                    "min_land_acres": 0,
                    "farmer_types": ["marginal", "small", "medium", "large"],
                },
                states_eligible=None,  # All India
                crops_eligible=None,  # All crops
                apply_url="https://pmkisan.gov.in/",
                csc_applicable=True
            ),
            
            # Kisan Credit Card
            SchemeRecord(
                scheme_key="kcc",
                scheme_name="Kisan Credit Card (KCC)",
                scheme_name_hi="किसान क्रेडिट कार्ड",
                description="Short-term credit facility for cultivation and post-harvest expenses with low interest",
                description_hi="कम ब्याज दर पर खेती और कटाई के बाद के खर्चों के लिए अल्पकालिक ऋण सुविधा",
                benefits=[
                    "Credit up to Rs 3 lakh at 7% interest",
                    "Additional 3% interest subvention on timely payment",
                    "Insurance coverage included"
                ],
                benefits_hi=[
                    "7% ब्याज पर 3 लाख रुपये तक ऋण",
                    "समय पर भुगतान पर अतिरिक्त 3% छूट",
                    "बीमा कवरेज शामिल"
                ],
                deadline=None,  # Always open
                docs_required=[
                    "Aadhaar card",
                    "Land documents",
                    "Bank account",
                    "Passport size photos"
                ],
                eligibility_rules={
                    "min_land_acres": 0,
                    "farmer_types": ["marginal", "small", "medium", "large"],
                },
                states_eligible=None,
                crops_eligible=None,
                apply_url="https://www.nabard.org/kcc.aspx",
                csc_applicable=True
            ),
            
            # PM Fasal Bima Yojana
            SchemeRecord(
                scheme_key="pmfby",
                scheme_name="Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                scheme_name_hi="प्रधानमंत्री फसल बीमा योजना",
                description="Crop insurance scheme covering yield losses due to natural calamities",
                description_hi="प्राकृतिक आपदाओं के कारण फसल नुकसान के लिए बीमा योजना",
                benefits=[
                    "Only 2% premium for Kharif, 1.5% for Rabi crops",
                    "Coverage for natural calamities, pests, diseases",
                    "Sum insured is full crop value"
                ],
                benefits_hi=[
                    "खरीफ के लिए केवल 2%, रबी के लिए 1.5% प्रीमियम",
                    "प्राकृतिक आपदा, कीट, रोग के लिए कवरेज",
                    "पूर्ण फसल मूल्य का बीमा"
                ],
                deadline=today + timedelta(days=10),  # Urgent deadline
                docs_required=[
                    "Aadhaar card",
                    "Land records (7/12, 8A)",
                    "Bank account details",
                    "Sowing certificate"
                ],
                eligibility_rules={
                    "min_land_acres": 0,
                    "farmer_types": ["marginal", "small", "medium", "large"],
                    "crop_enrollment": True
                },
                states_eligible=None,
                crops_eligible=["rice", "wheat", "cotton", "soybean", "groundnut"],
                apply_url="https://pmfby.gov.in/",
                csc_applicable=True
            ),
            
            # Soil Health Card Scheme
            SchemeRecord(
                scheme_key="shc",
                scheme_name="Soil Health Card Scheme",
                scheme_name_hi="मृदा स्वास्थ्य कार्ड योजना",
                description="Free soil testing and health card with fertilizer recommendations",
                description_hi="निःशुल्क मिट्टी परीक्षण और उर्वरक सिफारिशों के साथ स्वास्थ्य कार्ड",
                benefits=[
                    "Free soil nutrient analysis",
                    "Customized fertilizer recommendations",
                    "Reduce fertilizer cost by 10-15%"
                ],
                benefits_hi=[
                    "निःशुल्क मिट्टी पोषक तत्व विश्लेषण",
                    "अनुकूलित उर्वरक सिफारिशें",
                    "उर्वरक लागत में 10-15% की कमी"
                ],
                deadline=None,
                docs_required=[
                    "Aadhaar card",
                    "Soil sample from field"
                ],
                eligibility_rules={
                    "min_land_acres": 0,
                    "farmer_types": ["marginal", "small", "medium", "large"],
                },
                states_eligible=None,
                crops_eligible=None,
                apply_url="https://soilhealth.dac.gov.in/",
                csc_applicable=True
            ),
            
            # PM Krishi Sinchai Yojana - Drip irrigation subsidy
            SchemeRecord(
                scheme_key="pmksy_drip",
                scheme_name="PM Krishi Sinchai Yojana - Micro Irrigation",
                scheme_name_hi="प्रधानमंत्री कृषि सिंचाई योजना - सूक्ष्म सिंचाई",
                description="Subsidy for drip and sprinkler irrigation systems to improve water efficiency",
                description_hi="जल दक्षता में सुधार के लिए ड्रिप और स्प्रिंकलर सिंचाई प्रणाली पर सब्सिडी",
                benefits=[
                    "55% subsidy for small/marginal farmers",
                    "45% subsidy for other farmers",
                    "Save 40-50% water, increase yield 20-30%"
                ],
                benefits_hi=[
                    "छोटे/सीमांत किसानों के लिए 55% सब्सिडी",
                    "अन्य किसानों के लिए 45% सब्सिडी",
                    "40-50% पानी बचाएं, उपज में 20-30% वृद्धि"
                ],
                deadline=today + timedelta(days=25),
                docs_required=[
                    "Aadhaar card",
                    "Land ownership proof",
                    "Bank account",
                    "Quotation from approved vendors"
                ],
                eligibility_rules={
                    "min_land_acres": 1.0,
                    "farmer_types": ["marginal", "small", "medium", "large"],
                },
                states_eligible=None,
                crops_eligible=["cotton", "tomato", "onion", "sugarcane"],
                apply_url="https://pmksy.gov.in/",
                csc_applicable=True
            ),
            
            # National Food Security Mission subsidy
            SchemeRecord(
                scheme_key="nfsm_wheat",
                scheme_name="National Food Security Mission - Wheat Subsidy",
                scheme_name_hi="राष्ट्रीय खाद्य सुरक्षा मिशन - गेहूं सब्सिडी",
                description="Subsidized certified seeds and technical support for wheat cultivation",
                description_hi="गेहूं की खेती के लिए सब्सिडी युक्त प्रमाणित बीज और तकनीकी सहायता",
                benefits=[
                    "50% subsidy on certified wheat seeds",
                    "Free technical training",
                    "Cluster demonstration support"
                ],
                benefits_hi=[
                    "प्रमाणित गेहूं के बीज पर 50% सब्सिडी",
                    "निःशुल्क तकनीकी प्रशिक्षण",
                    "समूह प्रदर्शन समर्थन"
                ],
                deadline=today + timedelta(days=5),  # Very urgent
                docs_required=[
                    "Aadhaar card",
                    "Land records",
                    "Registration with agriculture dept"
                ],
                eligibility_rules={
                    "min_land_acres": 0.5,
                    "farmer_types": ["marginal", "small", "medium"],
                },
                states_eligible=["Punjab", "Haryana", "Uttar Pradesh", "Madhya Pradesh", "Rajasthan"],
                crops_eligible=["wheat"],
                apply_url="https://nfsm.gov.in/",
                csc_applicable=True
            ),
            
            # Horticulture subsidy
            SchemeRecord(
                scheme_key="midh_vegetables",
                scheme_name="Mission for Integrated Development of Horticulture (MIDH)",
                scheme_name_hi="बागवानी के एकीकृत विकास के लिए मिशन",
                description="Financial assistance for vegetable cultivation, seeds, and protected cultivation",
                description_hi="सब्जी की खेती, बीज और संरक्षित खेती के लिए वित्तीय सहायता",
                benefits=[
                    "40% subsidy for open cultivation",
                    "50% subsidy for small/marginal farmers",
                    "Protected cultivation subsidy up to Rs 35/sq.m"
                ],
                benefits_hi=[
                    "खुली खेती के लिए 40% सब्सिडी",
                    "छोटे/सीमांत किसानों के लिए 50% सब्सिडी",
                    "संरक्षित खेती के लिए 35 रुपये/वर्ग मीटर तक की सब्सिडी"
                ],
                deadline=today + timedelta(days=18),
                docs_required=[
                    "Aadhaar card",
                    "Land documents",
                    "Bank account",
                    "Approved technical plan"
                ],
                eligibility_rules={
                    "min_land_acres": 0.5,
                    "farmer_types": ["marginal", "small", "medium", "large"],
                },
                states_eligible=None,
                crops_eligible=["tomato", "onion", "potato"],
                apply_url="https://midh.gov.in/",
                csc_applicable=True
            ),
            
            # Interest subvention for short term loans
            SchemeRecord(
                scheme_key="interest_subvention",
                scheme_name="Interest Subvention Scheme for Short-term Crop Loans",
                scheme_name_hi="अल्पकालिक फसल ऋण के लिए ब्याज सहायता योजना",
                description="Interest rate reduction on crop loans for timely repayment",
                description_hi="समय पर चुकौती पर फसल ऋण पर ब्याज दर में कमी",
                benefits=[
                    "Effective 4% interest rate on crop loans",
                    "Additional 3% interest subvention on timely payment",
                    "Available through KCC"
                ],
                benefits_hi=[
                    "फसल ऋण पर प्रभावी 4% ब्याज दर",
                    "समय पर भुगतान पर अतिरिक्त 3% ब्याज सहायता",
                    "KCC के माध्यम से उपलब्ध"
                ],
                deadline=None,
                docs_required=[
                    "Kisan Credit Card",
                    "Bank account",
                    "Loan sanction letter"
                ],
                eligibility_rules={
                    "min_land_acres": 0,
                    "farmer_types": ["marginal", "small", "medium", "large"],
                    "kcc_holder": True
                },
                states_eligible=None,
                crops_eligible=None,
                apply_url="https://agricoop.nic.in/",
                csc_applicable=True
            ),
        ]
