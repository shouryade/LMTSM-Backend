from pydantic import BaseModel, validator, ValidationError
from fastapi import Form
from datetime import date
from typing import Optional


class AllocationRequest(BaseModel):
    name: str
    phone: int
    vehicle: str

    class Config:
        orm_mode = True


class TripCompleteRequest(BaseModel):
    total: int
    trip_id: Optional[str] = None
    start: int
    end: int
    inTime: str
    inDate: str
    outTime: str
    outDate: str

    class Config:
        orm_mode = True


class DutySlip(BaseModel):
    name_of_driver: str
    vehicle_number: str
    date: str
    time: str
    place_of_visit: str
    purpose: str
    num_people: str
    booking_name: str
    phone: int
    dep: str
    des: str
    chargeable_head: Optional[str]

    class Config:
        orm_mode = True
