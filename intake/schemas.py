from enum import Enum
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class ChannelType(str, Enum):
    OPEN_DRAIN = "open_concrete_drain"
    CONCRETE_CANAL = "concrete_channel"
    NATURAL_STREAM = "natural_stream"
    LAGOON_ADJACENT = "lagoon_adjacent"

class LarvaeDensity(str, Enum):
    NONE = "none"
    LOW = "low_1_10_per_dip"
    HIGH = "high_over_10_per_dip"

class WasteSeverity(str, Enum):
    CLEAN = "none"
    MODERATE = "moderate_bank_litter"
    CHOKED = "choked_flow_obstructed"

class FieldObservationInput(BaseModel):
    site_id: str = Field(..., example="lagos-makoko-canal-01")
    site_name: str = Field(..., example="Makoko Canal Footbridge")
    latitude: float = Field(..., ge=-90, le=90, example=6.4969)
    longitude: float = Field(..., ge=-180, le=180, example=3.3892)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    water_temp_celsius: Optional[float] = Field(None, example=29.4)
    ph: Optional[float] = Field(None, ge=0, le=14, example=7.2)
    dissolved_oxygen_mg_l: Optional[float] = Field(None, ge=0, example=2.1)
    turbidity_ntu: Optional[float] = Field(None, ge=0, example=45.0)
    
    channel_type: ChannelType
    mosquito_larvae: LarvaeDensity
    waste_severity: WasteSeverity
    photo_urls: List[str] = Field(default_factory=list)
