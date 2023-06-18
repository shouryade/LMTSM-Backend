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
    date: str
    time: str
    place_of_visit: str
    purpose: str
    num_people: str
    chargeable_head: Optional[str] = None

    @validator("date")
    def date_not_past(cls, v):
        if v < str(date.today()):
            raise ValidationError("Date must not be a past date")
        return v

    @validator("num_people")
    def num_people_validator(cls, value):
        if int(value) <= 0:
            raise ValidationError("number of people must be greater than 0")
        return value


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
