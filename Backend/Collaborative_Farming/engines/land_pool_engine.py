"""
Land Pooling Engine for Collaborative Farming
"""

from typing import List, Optional, Dict
from datetime import datetime
import uuid

from ..models import LandPoolRequest, FarmerProfile
from ..constants import PoolStatus, PoolRequestType
from ..repositories import LandPoolRepo


class LandPoolEngine:
    """Engine for land pooling requests and matchmaking"""
    
    def __init__(self, pool_repo: LandPoolRepo):
        self.repo = pool_repo

    def create_pool_request(
        self,
        farmer_id: str,
        request_type: PoolRequestType,
        land_size: float,
        district: str,
        pincode: str,
        crop_preference: Optional[str] = None,
        expected_members: Optional[int] = None
    ) -> LandPoolRequest:
        """Create a new land pooling or partner search request"""
        req = LandPoolRequest(
            requestId=str(uuid.uuid4()),
            farmerId=farmer_id,
            requestType=request_type,
            landSizeAcres=land_size,
            cropPreference=crop_preference,
            expectedMembers=expected_members,
            joinedFarmers=[farmer_id],
            district=district,
            pincode=pincode,
            status=PoolStatus.OPEN
        )
        return self.repo.create_pool_request(req)

    def find_matching_requests(self, farmer: FarmerProfile) -> List[LandPoolRequest]:
        """Find land pooling requests matching farmer's location"""
        # Match primarily by district
        return self.repo.list_open_requests({"district": farmer.district})

    def join_pool(self, request_id: str, farmer_id: str) -> LandPoolRequest:
        """Join an existing land pool"""
        self.repo.join_request(request_id, farmer_id)
        return self.repo.get_request(request_id)
