"""
Land Pooling Repository for Collaborative Farming
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid

from ..models import LandPoolRequest
from ..constants import PoolStatus, PoolRequestType, PoolStage


class LandPoolRepo:
    def __init__(self):
        self._pool_requests: Dict[str, LandPoolRequest] = {}
        self.seed_mock_pool_requests_if_empty()

    def create_pool_request(self, req: LandPoolRequest) -> LandPoolRequest:
        """Create a new land pooling request"""
        self._pool_requests[req.requestId] = req
        return req

    def get_request(self, request_id: str) -> Optional[LandPoolRequest]:
        """Fetch a specific pool request"""
        return self._pool_requests.get(request_id)

    def list_open_requests(self, filters: Dict) -> List[LandPoolRequest]:
        """List open pooling requests with filters"""
        results = [r for r in self._pool_requests.values() if r.status == PoolStatus.OPEN]
        
        if "district" in filters:
            results = [r for r in results if r.district == filters["district"]]
            
        return results

    def join_request(self, request_id: str, farmer_id: str):
        """Add a farmer to a pooling request"""
        if request_id in self._pool_requests:
            req = self._pool_requests[request_id]
            if farmer_id not in req.joinedFarmers:
                req.joinedFarmers.append(farmer_id)
                req.updatedAt = datetime.now()
                
                # Check if matched
                if req.expectedMembers and len(req.joinedFarmers) >= req.expectedMembers:
                    req.status = PoolStatus.MATCHED

    def seed_mock_pool_requests_if_empty(self):
        """Seed mock pool requests if repository is empty"""
        if self._pool_requests:
            return
            
        now = datetime.now()
        
        req1 = LandPoolRequest(
            requestId=str(uuid.uuid4()),
            farmerId="FARMER005",
            requestType=PoolRequestType.POOL_LAND,
            landSizeAcres=450.0,
            cropPreference="Wheat",
            season="Rabi",
            expectedMembers=15,
            joinedFarmers=["FARMER001", "FARMER002", "FARMER003"],
            district="Ludhiana",
            pincode="141001",
            currentStage=PoolStage.NEGOTIATION,
            progressPct=65,
            targetPrice=2100.0,
            highestBid=2050.0,
            sellingWindow="Nov 15-20",
            totalQuantity=450.0,
            keyBenefit="Bulk Buyer Targeted",
            status=PoolStatus.OPEN
        )
        
        req2 = LandPoolRequest(
            requestId=str(uuid.uuid4()),
            farmerId="FARMER001",
            requestType=PoolRequestType.SEEK_PARTNER,
            landSizeAcres=85.0,
            cropPreference="Rice",
            season="Kharif",
            expectedMembers=5,
            joinedFarmers=["FARMER001"],
            district="Nashik",
            pincode="422001",
            currentStage=PoolStage.FORMATION,
            progressPct=20,
            sellingWindow="Dec 1-10",
            totalQuantity=85.0,
            keyBenefit="Shared Machinery",
            status=PoolStatus.OPEN
        )
        
        self._pool_requests[req1.requestId] = req1
        self._pool_requests[req2.requestId] = req2
