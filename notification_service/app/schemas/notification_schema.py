from pydantic import BaseModel, Field
from typing import Optional, List

class NotificationEventIn(BaseModel):
    event_type: str = Field(..., examples=["ORDER_CREATED", "DELIVERED"])
    channel: str = Field(default="IN_APP", examples=["IN_APP", "EMAIL", "SMS", "PUSH"])
    recipient: Optional[str] = Field(default=None, examples=["cust_123", "test@email.com"])
    tracking_number: Optional[str] = None
    order_id: Optional[str] = None
    title: str
    message: str

class NotificationOut(BaseModel):
    id: str
    event_type: str
    channel: str
    recipient: Optional[str] = None
    tracking_number: Optional[str] = None
    order_id: Optional[str] = None
    title: str
    message: str
    status: str
    sent: bool
    created_at: str
    sent_at: Optional[str] = None

class NotificationListOut(BaseModel):
    items: List[NotificationOut]
