from pydantic import BaseModel, validator, ValidationError
from fastapi import Form
from datetime import date
from typing import Optional


class registerUser(BaseModel):
    des: str = Form(...)
    first_name: str = Form(...)
    last_name: str = Form(...)
    email: str = Form(...)
    empno: str = Form(...)
    phone: int = Form(...)
    dep: str = Form(...)
    password: str = Form(...)
    role: str


class BookingRequest(BaseModel):
    name: str
    startDate: str
    endDate: str
    time: str
    place_of_visit: str
    purpose: str
    num_people: str
    reason: str
    chargeable_head: Optional[str] = None


class Booking(BaseModel):
    status: str
    particulars: BookingRequest

    user_id: str
    des: Optional[str]
    dep: Optional[str]
    phone: Optional[int]

    name_of_driver: Optional[str] = None
    phone_of_driver: Optional[int] = None
    vehicle_number: Optional[str] = None

    meter_reading_closing: Optional[float] = None
    meter_reading_starting: Optional[float] = None

    total_amount: Optional[float] = None
    trip_completed: Optional[bool] = False
    trip_ID: Optional[str] = None

    meter_reading_total: Optional[float] = None
    rate_per_km: Optional[float] = None
    inTime: Optional[str] = None
    inDate: Optional[str] = None
    outTime: Optional[str] = None
    outDate: Optional[str] = None
