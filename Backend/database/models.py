from datetime import datetime
from typing import List, Optional, Any, Dict
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

# Custom Pydantic type for ObjectId
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class Location(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

# ==========================================
# STANDARD COLLECTIONS
# ==========================================

# 1. Users Collection
class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    phone: str
    passwordHash: str
    role: str = "farmer"  # "farmer", "admin"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    lastActive: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 2. Farmers Collection
class Farmer(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    userId: PyObjectId  # FK to users
    language: str = "en" # "hi", "mr", "en"
    location: Location
    soilType: Optional[str] = None
    landSizeAcres: Optional[float] = None
    setupCompleted: bool = False
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 3. Crops Master Collection
class Requirements(BaseModel):
    avgRainfallMm: Optional[float] = None
    temperatureRange: Optional[Dict[str, float]] = None # {min, max}
    fertilizer: Optional[str] = None

class CropMaster(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    cropKey: str
    localNames: Dict[str, str] # {hi, mr, en}
    suitableSoils: List[str]
    season: str
    maturityDays: int
    waterRequirement: str
    requirements: Requirements
    avgYieldPerAcre: Optional[float] = None
    marketDemandTrend: Optional[str] = None
    commonDiseases: List[str] = []

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 4. Schemes Master Collection
class EligibilityRules(BaseModel):
    minLandSizeAcres: Optional[float] = None
    maxLandSizeAcres: Optional[float] = None
    soilTypes: List[str] = []
    crops: List[str] = []
    states: List[str] = []

class SchemeMaster(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    schemeKey: str
    schemeName: str
    localizedNames: Dict[str, str]
    description: str
    benefits: str
    eligibilityRules: EligibilityRules
    requiredDocuments: List[str]
    deadline: Optional[datetime] = None
    applicationUrl: Optional[str] = None
    category: str
    isActive: bool = True

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 5. Disease Master Collection
class DiseaseRemedy(BaseModel):
    treatment: str
    dosage: str
    applicationMethod: str
    preventionTips: List[str]

class DiseaseMaster(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    diseaseKey: str
    diseaseName: str
    localizedNames: Dict[str, str]
    affectedCrops: List[str]
    symptoms: List[str]
    severity: str
    remedy: DiseaseRemedy
    spreadRisk: str
    imageUrls: List[str] = []

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 6. Mandi Masters Collection
class MandiMaster(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    mandiName: str
    state: str
    district: str
    location: Dict[str, float]
    operatingDays: List[str]
    facilities: List[str]
    avgTransportCost: Optional[float] = None
    contactInfo: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 7. Farmer Crops Collection
class FarmerCrop(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    farmerId: PyObjectId
    cropKey: str
    season: str
    stage: str # "pre_seeding", "during_farming", "post_harvest"
    sowingDate: Optional[datetime] = None
    expectedHarvestDate: Optional[datetime] = None
    areaAllocatedAcres: Optional[float] = None
    status: str = "active"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: Optional[datetime] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 8. Inventory Items Collection
class InventoryItem(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    farmerId: PyObjectId
    cropKey: str
    quantityKg: float
    unit: str
    storageDate: datetime
    storageLocation: str
    shelfLifeDays: int
    healthStatus: str
    estimatedValueRs: float
    lastUpdated: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# ==========================================
# TIME-SERIES COLLECTIONS
# ==========================================

# 12. Sessions Collection
class ConversationMeta(BaseModel):
    farmerId: PyObjectId
    language: str
    isActive: bool

class Session(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sessionStartTime: datetime
    conversationMeta: ConversationMeta

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 13. Cards Collection
class CardMeta(BaseModel):
    farmerId: PyObjectId
    sessionId: PyObjectId
    cardType: str
    priority: str

class Card(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    createdAt: datetime
    cardMeta: CardMeta
    content: Dict[str, Any]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 14. Crop Stage Logs
class EventMeta(BaseModel):
    farmerId: PyObjectId
    farmerCropId: PyObjectId
    cropKey: str
    eventType: str

class CropStageLog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    performedAt: datetime
    eventMeta: EventMeta
    details: Dict[str, Any]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 15. Tasks Calendar
class TaskMeta(BaseModel):
    farmerId: PyObjectId
    farmerCropId: Optional[PyObjectId] = None
    taskType: str
    isSystemGenerated: bool = False

class Task(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    dueAt: datetime
    taskMeta: TaskMeta
    title: Optional[str] = None
    description: Optional[str] = None
    status: str = "pending"

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 16. Inventory Logs
class InventoryMeta(BaseModel):
    farmerId: PyObjectId
    inventoryItemId: PyObjectId
    action: str

class InventoryLog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    ts: datetime
    inventoryMeta: InventoryMeta
    quantityChange: float
    notes: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 17. Finance Transactions
class TransactionMeta(BaseModel):
    farmerId: PyObjectId
    farmerCropId: Optional[PyObjectId] = None
    season: Optional[str] = None
    type: str # "income", "expense"
    category: str

class FinanceTransaction(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    ts: datetime
    transactionMeta: TransactionMeta
    amount: float
    description: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 19. Mandi Prices Cache
class MarketMeta(BaseModel):
    cropKey: str
    mandiId: PyObjectId
    mandi: str
    district: str
    state: str

class MandiPrice(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    date: datetime
    marketMeta: MarketMeta
    price: float
    unit: str

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 20. Weather Data
class LocationMeta(BaseModel):
    district: str
    village: Optional[str] = None
    location: Dict[str, float]

class WeatherData(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    ts: datetime
    locationMeta: LocationMeta
    tempC: float
    humidity: float
    condition: str
    windSpeedKmph: Optional[float] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 21. Alerts Notifications
class AlertMeta(BaseModel):
    farmerId: PyObjectId
    alertType: str
    priority: str

class Alert(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sentAt: datetime
    alertMeta: AlertMeta
    title: str
    message: str
    isRead: bool = False

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 22. Crop Doctor Reports
class ScanMeta(BaseModel):
    farmerId: PyObjectId
    farmerCropId: Optional[PyObjectId] = None
    cropKey: Optional[str] = None

class CropDoctorReport(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    createdAt: datetime
    scanMeta: ScanMeta
    diagnosis: str
    confidence: float
    imageUrl: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 23. Equipment Rentals
class RentalMeta(BaseModel):
    renterFarmerId: PyObjectId
    ownerFarmerId: PyObjectId
    listingId: PyObjectId
    equipmentType: str

class EquipmentRental(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    startDate: datetime
    rentalMeta: RentalMeta
    endDate: datetime
    totalCost: float
    status: str

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 24. Scheme Applications
class SchemeMeta(BaseModel):
    farmerId: PyObjectId
    schemeKey: str
    status: str

class SchemeApplication(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    applicationDate: datetime
    schemeMeta: SchemeMeta
    notes: Optional[str] = None

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}

# 25. Audit Logs
class AuditMeta(BaseModel):
    farmerId: Optional[PyObjectId] = None
    userId: Optional[PyObjectId] = None
    action: str
    entityType: Optional[str] = None

class AuditLog(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    ts: datetime
    auditMeta: AuditMeta
    details: Dict[str, Any]

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
