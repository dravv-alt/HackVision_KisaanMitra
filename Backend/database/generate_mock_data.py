"""
Comprehensive Mock Data Generator for KisanMitra MongoDB
Generates 20-30 rows of realistic data for each collection
"""

from datetime import datetime, timedelta
import random
from bson import ObjectId

# Helper function to generate random dates
def random_date(start_days_ago=365, end_days_ago=0):
    start = datetime.now() - timedelta(days=start_days_ago)
    end = datetime.now() - timedelta(days=end_days_ago)
    return start + (end - start) * random.random()

# Helper to generate ObjectId
def generate_id():
    return str(ObjectId())

# 1. FARMERS COLLECTION (25 farmers)
farmers_data = []
farmer_names = [
    "राम कुमार शर्मा", "श्याम सिंह पटेल", "मोहन लाल वर्मा", "सोहन यादव", "रोहन गुप्ता",
    "विकास कुमार", "अमित शर्मा", "सुनील पाटिल", "राजेश ठाकुर", "दिनेश कुमार",
    "प्रकाश जाधव", "संजय देशमुख", "अजय पवार", "विजय काले", "मनोज राठौर",
    "रवि शंकर", "कृष्ण मुरारी", "गोपाल दास", "हरि प्रसाद", "बालाजी राव",
    "नरेंद्र सिंह", "सुरेश बाबू", "रमेश चंद्र", "महेश कुमार", "योगेश पांडे"
]

villages = ["रामपुर", "श्यामपुर", "सीतापुर", "गोकुलपुर", "नंदगांव", "वृंदावन", "मथुरा", "अयोध्या"]
districts = ["पुणे", "नागपुर", "औरंगाबाद", "नाशिक", "अहमदनगर", "सोलापुर", "कोल्हापुर", "सातारा"]
states = ["महाराष्ट्र", "उत्तर प्रदेश", "मध्य प्रदेश", "राजस्थान", "पंजाब"]
soil_types = ["alluvial", "black", "red", "sandy", "clay"]
crops_list = [["wheat", "rice"], ["cotton", "sugarcane"], ["maize", "potato"], ["wheat", "mustard"], ["rice", "vegetables"]]

for i in range(25):
    farmer_id = f"F{str(i+1).zfill(3)}"
    farmers_data.append({
        "farmer_id": farmer_id,
        "user_id": f"U{str(i+1).zfill(3)}",
        "name": farmer_names[i],
        "phone": f"+91{random.randint(7000000000, 9999999999)}",
        "language": random.choice(["hi", "mr", "en"]),
        "location": {
            "state": random.choice(states),
            "district": random.choice(districts),
            "village": random.choice(villages),
            "pincode": f"{random.randint(400000, 499999)}",
            "coordinates": {
                "lat": round(random.uniform(15.0, 30.0), 6),
                "lon": round(random.uniform(72.0, 85.0), 6)
            }
        },
        "soil_type": random.choice(soil_types),
        "land_size_acres": round(random.uniform(2, 50), 2),
        "crops": random.choice(crops_list),
        "onboarding_completed": True,
        "created_at": random_date(180, 0),
        "updated_at": datetime.now()
    })

# 2. CROPS MASTER COLLECTION (30 crops)
crops_master_data = [
    {"crop_id": "C001", "name_en": "Wheat", "name_hi": "गेहूँ", "category": "Rabi", "season": "Winter", "duration_days": 120, "water_requirement": "Medium"},
    {"crop_id": "C002", "name_en": "Rice", "name_hi": "चावल", "category": "Kharif", "season": "Monsoon", "duration_days": 150, "water_requirement": "High"},
    {"crop_id": "C003", "name_en": "Cotton", "name_hi": "कपास", "category": "Kharif", "season": "Monsoon", "duration_days": 180, "water_requirement": "Medium"},
    {"crop_id": "C004", "name_en": "Sugarcane", "name_hi": "गन्ना", "category": "Annual", "season": "Year-round", "duration_days": 365, "water_requirement": "High"},
    {"crop_id": "C005", "name_en": "Maize", "name_hi": "मक्का", "category": "Kharif", "season": "Monsoon", "duration_days": 90, "water_requirement": "Medium"},
    {"crop_id": "C006", "name_en": "Potato", "name_hi": "आलू", "category": "Rabi", "season": "Winter", "duration_days": 100, "water_requirement": "Medium"},
    {"crop_id": "C007", "name_en": "Tomato", "name_hi": "टमाटर", "category": "All Season", "season": "Year-round", "duration_days": 75, "water_requirement": "Medium"},
    {"crop_id": "C008", "name_en": "Onion", "name_hi": "प्याज", "category": "Rabi", "season": "Winter", "duration_days": 120, "water_requirement": "Low"},
    {"crop_id": "C009", "name_en": "Mustard", "name_hi": "सरसों", "category": "Rabi", "season": "Winter", "duration_days": 110, "water_requirement": "Low"},
    {"crop_id": "C010", "name_en": "Chickpea", "name_hi": "चना", "category": "Rabi", "season": "Winter", "duration_days": 130, "water_requirement": "Low"},
    {"crop_id": "C011", "name_en": "Soybean", "name_hi": "सोयाबीन", "category": "Kharif", "season": "Monsoon", "duration_days": 100, "water_requirement": "Medium"},
    {"crop_id": "C012", "name_en": "Groundnut", "name_hi": "मूंगफली", "category": "Kharif", "season": "Monsoon", "duration_days": 120, "water_requirement": "Low"},
    {"crop_id": "C013", "name_en": "Sunflower", "name_hi": "सूरजमुखी", "category": "Rabi", "season": "Winter", "duration_days": 90, "water_requirement": "Medium"},
    {"crop_id": "C014", "name_en": "Bajra", "name_hi": "बाजरा", "category": "Kharif", "season": "Monsoon", "duration_days": 75, "water_requirement": "Low"},
    {"crop_id": "C015", "name_en": "Jowar", "name_hi": "ज्वार", "category": "Kharif", "season": "Monsoon", "duration_days": 100, "water_requirement": "Low"},
    {"crop_id": "C016", "name_en": "Barley", "name_hi": "जौ", "category": "Rabi", "season": "Winter", "duration_days": 120, "water_requirement": "Low"},
    {"crop_id": "C017", "name_en": "Lentil", "name_hi": "मसूर", "category": "Rabi", "season": "Winter", "duration_days": 110, "water_requirement": "Low"},
    {"crop_id": "C018", "name_en": "Peas", "name_hi": "मटर", "category": "Rabi", "season": "Winter", "duration_days": 90, "water_requirement": "Medium"},
    {"crop_id": "C019", "name_en": "Cabbage", "name_hi": "पत्तागोभी", "category": "Rabi", "season": "Winter", "duration_days": 80, "water_requirement": "Medium"},
    {"crop_id": "C020", "name_en": "Cauliflower", "name_hi": "फूलगोभी", "category": "Rabi", "season": "Winter", "duration_days": 85, "water_requirement": "Medium"},
    {"crop_id": "C021", "name_en": "Brinjal", "name_hi": "बैंगन", "category": "All Season", "season": "Year-round", "duration_days": 120, "water_requirement": "Medium"},
    {"crop_id": "C022", "name_en": "Chilli", "name_hi": "मिर्च", "category": "Kharif", "season": "Monsoon", "duration_days": 150, "water_requirement": "Medium"},
    {"crop_id": "C023", "name_en": "Coriander", "name_hi": "धनिया", "category": "Rabi", "season": "Winter", "duration_days": 45, "water_requirement": "Low"},
    {"crop_id": "C024", "name_en": "Turmeric", "name_hi": "हल्दी", "category": "Annual", "season": "Year-round", "duration_days": 270, "water_requirement": "Medium"},
    {"crop_id": "C025", "name_en": "Ginger", "name_hi": "अदरक", "category": "Kharif", "season": "Monsoon", "duration_days": 240, "water_requirement": "High"},
    {"crop_id": "C026", "name_en": "Garlic", "name_hi": "लहसुन", "category": "Rabi", "season": "Winter", "duration_days": 150, "water_requirement": "Low"},
    {"crop_id": "C027", "name_en": "Carrot", "name_hi": "गाजर", "category": "Rabi", "season": "Winter", "duration_days": 90, "water_requirement": "Medium"},
    {"crop_id": "C028", "name_en": "Radish", "name_hi": "मूली", "category": "Rabi", "season": "Winter", "duration_days": 40, "water_requirement": "Low"},
    {"crop_id": "C029", "name_en": "Spinach", "name_hi": "पालक", "category": "Rabi", "season": "Winter", "duration_days": 45, "water_requirement": "Medium"},
    {"crop_id": "C030", "name_en": "Fenugreek", "name_hi": "मेथी", "category": "Rabi", "season": "Winter", "duration_days": 30, "water_requirement": "Low"}
]

# 3. ACTIVE CROPS COLLECTION (30 active crop instances)
active_crops_data = []
for i in range(30):
    farmer_id = f"F{str(random.randint(1, 25)).zfill(3)}"
    crop = random.choice(crops_master_data)
    planting_date = random_date(120, 10)
    
    active_crops_data.append({
        "active_crop_id": f"AC{str(i+1).zfill(3)}",
        "farmer_id": farmer_id,
        "crop_id": crop["crop_id"],
        "crop_name": crop["name_hi"],
        "area_acres": round(random.uniform(1, 10), 2),
        "planting_date": planting_date,
        "expected_harvest_date": planting_date + timedelta(days=crop["duration_days"]),
        "current_stage": random.choice(["सीडिंग", "अंकुरण", "वृद्धि", "फूल आना", "फल लगना", "परिपक्वता"]),
        "health_status": random.choice(["स्वस्थ", "ध्यान चाहिए", "बीमार"]),
        "health_score": random.randint(60, 100),
        "last_watered": random_date(7, 0),
        "last_fertilized": random_date(30, 0),
        "notes": "फसल अच्छी स्थिति में है",
        "created_at": planting_date,
        "updated_at": datetime.now()
    })

# 4. EQUIPMENT LISTINGS (25 equipment)
equipment_types = ["ट्रैक्टर", "हार्वेस्टर", "थ्रेशर", "सीड ड्रिल", "स्प्रेयर", "टिलर", "पंप सेट"]
equipment_brands = ["महिंद्रा", "जॉन डियर", "सोनालिका", "न्यू हॉलैंड", "स्वराज"]

equipment_data = []
for i in range(25):
    equipment_type = random.choice(equipment_types)
    equipment_data.append({
        "listing_id": f"EQ{str(i+1).zfill(3)}",
        "farmer_id": f"F{str(random.randint(1, 25)).zfill(3)}",
        "equipment_type": equipment_type,
        "brand": random.choice(equipment_brands),
        "model": f"Model {random.randint(100, 999)}",
        "year": random.randint(2015, 2024),
        "condition": random.choice(["उत्कृष्ट", "अच्छा", "औसत"]),
        "rental_price_per_day": random.randint(500, 3000),
        "availability": random.choice(["उपलब्ध", "किराए पर", "रखरखाव में"]),
        "location": {
            "village": random.choice(villages),
            "district": random.choice(districts)
        },
        "description": f"{equipment_type} अच्छी स्थिति में, किराए के लिए उपलब्ध",
        "created_at": random_date(90, 0),
        "updated_at": datetime.now()
    })

# 5. GOVERNMENT SCHEMES (20 schemes)
schemes_data = [
    {
        "scheme_id": "SCH001",
        "name_hi": "प्रधानमंत्री फसल बीमा योजना",
        "name_en": "Pradhan Mantri Fasal Bima Yojana",
        "category": "बीमा",
        "benefit_amount": "₹50,000 प्रति हेक्टेयर तक",
        "eligibility": "सभी किसान",
        "description": "फसल नुकसान के खिलाफ व्यापक बीमा कवरेज",
        "how_to_apply": "नजदीकी बैंक या CSC केंद्र पर जाएं",
        "documents_required": ["आधार कार्ड", "भूमि रिकॉर्ड", "बैंक खाता"],
        "active": True
    },
    {
        "scheme_id": "SCH002",
        "name_hi": "किसान क्रेडिट कार्ड",
        "name_en": "Kisan Credit Card",
        "category": "ऋण",
        "benefit_amount": "₹3 लाख तक",
        "eligibility": "भूमि स्वामी किसान",
        "description": "कम ब्याज दर पर कृषि ऋण",
        "how_to_apply": "बैंक शाखा में आवेदन करें",
        "documents_required": ["आधार", "भूमि दस्तावेज", "पासपोर्ट फोटो"],
        "active": True
    },
    {
        "scheme_id": "SCH003",
        "name_hi": "पीएम किसान सम्मान निधि",
        "name_en": "PM-KISAN",
        "category": "प्रत्यक्ष लाभ",
        "benefit_amount": "₹6,000 प्रति वर्ष",
        "eligibility": "सभी भूमिधारक किसान परिवार",
        "description": "तीन किस्तों में सीधे बैंक खाते में ₹2000",
        "how_to_apply": "ऑनलाइन या CSC केंद्र",
        "documents_required": ["आधार", "बैंक खाता", "भूमि रिकॉर्ड"],
        "active": True
    },
    {
        "scheme_id": "SCH004",
        "name_hi": "मृदा स्वास्थ्य कार्ड योजना",
        "name_en": "Soil Health Card Scheme",
        "category": "मृदा परीक्षण",
        "benefit_amount": "मुफ्त मृदा परीक्षण",
        "eligibility": "सभी किसान",
        "description": "मृदा स्वास्थ्य और पोषक तत्व स्थिति का विश्लेषण",
        "how_to_apply": "कृषि विभाग कार्यालय",
        "documents_required": ["आधार", "भूमि विवरण"],
        "active": True
    },
    {
        "scheme_id": "SCH005",
        "name_hi": "प्रधानमंत्री कृषि सिंचाई योजना",
        "name_en": "PM Krishi Sinchayee Yojana",
        "category": "सिंचाई",
        "benefit_amount": "90% सब्सिडी",
        "eligibility": "सभी किसान",
        "description": "ड्रिप और स्प्रिंकलर सिंचाई पर सब्सिडी",
        "how_to_apply": "कृषि विभाग",
        "documents_required": ["आधार", "भूमि दस्तावेज"],
        "active": True
    },
    # Add 15 more schemes...
    {
        "scheme_id": f"SCH{str(i+6).zfill(3)}",
        "name_hi": f"योजना {i+6}",
        "name_en": f"Scheme {i+6}",
        "category": random.choice(["बीमा", "ऋण", "सब्सिडी", "प्रशिक्षण"]),
        "benefit_amount": f"₹{random.randint(10, 100)},000",
        "eligibility": "सभी किसान",
        "description": "किसानों के लिए लाभकारी योजना",
        "how_to_apply": "नजदीकी कार्यालय",
        "documents_required": ["आधार", "भूमि दस्तावेज"],
        "active": True
    } for i in range(15)
]

# 6. FINANCIAL TRANSACTIONS (30 transactions)
transaction_types = ["खर्च", "आय"]
expense_categories = ["बीज", "उर्वरक", "कीटनाशक", "श्रम", "सिंचाई", "मशीनरी", "परिवहन"]
income_categories = ["फसल बिक्री", "सब्सिडी", "अन्य"]

financial_data = []
for i in range(30):
    trans_type = random.choice(transaction_types)
    amount = random.randint(500, 50000)
    
    financial_data.append({
        "transaction_id": f"TXN{str(i+1).zfill(3)}",
        "farmer_id": f"F{str(random.randint(1, 25)).zfill(3)}",
        "type": trans_type,
        "category": random.choice(expense_categories if trans_type == "खर्च" else income_categories),
        "amount": amount,
        "description": f"{trans_type} - {random.choice(['गेहूँ', 'चावल', 'कपास'])} के लिए",
        "date": random_date(90, 0),
        "payment_method": random.choice(["नकद", "UPI", "बैंक ट्रांसफर", "चेक"]),
        "created_at": random_date(90, 0)
    })

# 7. MARKET PRICES (25 entries)
market_prices_data = []
crops_for_market = ["गेहूँ", "चावल", "कपास", "गन्ना", "मक्का", "आलू", "टमाटर", "प्याज"]
mandis = ["पुणे मंडी", "नागपुर मंडी", "औरंगाबाद मंडी", "नाशिक मंडी", "अहमदनगर मंडी"]

for i in range(25):
    crop = random.choice(crops_for_market)
    base_price = random.randint(2000, 5000)
    
    market_prices_data.append({
        "price_id": f"MP{str(i+1).zfill(3)}",
        "crop_name": crop,
        "mandi_name": random.choice(mandis),
        "price_per_quintal": base_price,
        "min_price": base_price - random.randint(100, 500),
        "max_price": base_price + random.randint(100, 500),
        "trend": random.choice(["बढ़ रहा", "घट रहा", "स्थिर"]),
        "change_percent": round(random.uniform(-5, 5), 2),
        "date": random_date(7, 0),
        "updated_at": datetime.now()
    })

# 8. WEATHER DATA (20 entries)
weather_data = []
for i in range(20):
    weather_data.append({
        "weather_id": f"WTH{str(i+1).zfill(3)}",
        "location": {
            "district": random.choice(districts),
            "pincode": f"{random.randint(400000, 499999)}"
        },
        "temperature": {
            "current": random.randint(20, 40),
            "min": random.randint(15, 25),
            "max": random.randint(30, 45)
        },
        "humidity": random.randint(40, 90),
        "rainfall": round(random.uniform(0, 50), 2),
        "wind_speed": random.randint(5, 30),
        "condition": random.choice(["साफ", "बादल", "बारिश", "धूप"]),
        "forecast_7day": [
            {
                "date": (datetime.now() + timedelta(days=j)).strftime("%Y-%m-%d"),
                "temp_max": random.randint(30, 40),
                "temp_min": random.randint(20, 30),
                "condition": random.choice(["साफ", "बादल", "बारिश"])
            } for j in range(7)
        ],
        "updated_at": datetime.now()
    })

# 9. ALERTS (25 alerts)
alert_types = ["मौसम चेतावनी", "कीट चेतावनी", "बीमारी चेतावनी", "सिंचाई अनुस्मारक", "उर्वरक अनुस्मारक"]
alert_priorities = ["उच्च", "मध्यम", "निम्न"]

alerts_data = []
for i in range(25):
    alerts_data.append({
        "alert_id": f"ALT{str(i+1).zfill(3)}",
        "farmer_id": f"F{str(random.randint(1, 25)).zfill(3)}",
        "type": random.choice(alert_types),
        "priority": random.choice(alert_priorities),
        "title": "महत्वपूर्ण सूचना",
        "message": "कृपया तुरंत ध्यान दें",
        "is_read": random.choice([True, False]),
        "created_at": random_date(30, 0),
        "expires_at": datetime.now() + timedelta(days=random.randint(1, 30))
    })

# 10. CALENDAR EVENTS (30 events)
event_types = ["बुवाई", "सिंचाई", "उर्वरक", "कीटनाशक", "कटाई", "बाजार दिवस"]

calendar_events_data = []
for i in range(30):
    event_date = datetime.now() + timedelta(days=random.randint(-30, 60))
    
    calendar_events_data.append({
        "event_id": f"EVT{str(i+1).zfill(3)}",
        "farmer_id": f"F{str(random.randint(1, 25)).zfill(3)}",
        "title": random.choice(event_types),
        "description": "कृषि गतिविधि",
        "event_type": random.choice(event_types),
        "date": event_date,
        "time": f"{random.randint(6, 18)}:00",
        "duration_hours": random.randint(1, 8),
        "status": random.choice(["नियोजित", "पूर्ण", "रद्द"]),
        "reminder_sent": random.choice([True, False]),
        "created_at": random_date(60, 0)
    })

print("Mock data generated successfully!")
print(f"Farmers: {len(farmers_data)}")
print(f"Crops Master: {len(crops_master_data)}")
print(f"Active Crops: {len(active_crops_data)}")
print(f"Equipment: {len(equipment_data)}")
print(f"Schemes: {len(schemes_data)}")
print(f"Transactions: {len(financial_data)}")
print(f"Market Prices: {len(market_prices_data)}")
print(f"Weather: {len(weather_data)}")
print(f"Alerts: {len(alerts_data)}")
print(f"Calendar Events: {len(calendar_events_data)}")
