from fastapi import Depends, APIRouter, HTTPException, status, Form, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from bleach import clean
from pydantic import ValidationError
from typing import Annotated
from config.db import collection_booking
from models.register import registerUser, BookingRequest, Booking
from utils import get_current_user
from typing import List, Annotated
from bson import ObjectId
from datetime import date

import models.requestmodel as requestmodel


router = APIRouter(prefix="/v1/booking", tags=["booking"])


@router.post("/request")
async def book(
    current_user: Annotated[registerUser, Depends(get_current_user)],
    request: BookingRequest,
):
    try:
        request_dict = request.dict()
        if request_dict["chargeable_head"] == "":
            request_dict["chargeable_head"] = None

        obj = Booking(
            particulars=request_dict,
            status="Pending",
            user_id=current_user["email"],
            des=current_user["des"],
            dep=current_user["dep"],
            phone=current_user["phone"],
        )
        obj_id = str(ObjectId())
        obj_dict = obj.dict()
        obj_dict["_id"] = obj_id
        collection_booking.insert_one(obj_dict)

        return {
            "success": True,
            "message": "booking request received",
            "booking_id": obj_id,
        }

    except ValidationError as e:
        return {"success": False, "error": e.errors()}


@router.get("/status")
async def get_booking_status(
    current_user: registerUser = Depends(get_current_user),
):
    today = date.today()
    results = collection_booking.find(
        {"user_id": current_user["email"], "particulars.date": {"$gte": str(today)}}
    )
    bookings = []

    for result in results:
        bookings.append(result)
    return bookings


@router.get("/bookings")
async def get_bookings(
    current_user: registerUser = Depends(get_current_user),
):
    if current_user["role"] not in {"super_admin"}:
        raise HTTPException(status_code=403, detail="Forbidden")

    results = collection_booking.find({"status": "Pending"})
    bookings = []
    for result in results:
        bookings.append(result)
    return bookings


@router.put("/approve/{id}")
async def approve_booking(
    id: str,
    status: str = "Approved",
    current_user: registerUser = Depends(get_current_user),
):
    if current_user["role"] != "super_admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    result = collection_booking.update_one(
        {"_id": str(ObjectId(id))}, {"$set": {"status": status}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")

    return {"success": True, "message": "Booking updated successfully"}


@router.delete("/approve/{id}")
async def delete_booking(id: str, user: registerUser = Depends(get_current_user)):
    if user["role"] != "super_admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    result = collection_booking.update_one(
        {"_id": str(ObjectId(id))}, {"$set": {"status": "Rejected"}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")

    return {"success": True, "message": "Booking deleted successfully"}


@router.get("/approved")
async def approved_bookings(current_user: registerUser = Depends(get_current_user)):
    if current_user["role"] not in {"admin", "super_admin"}:
        raise HTTPException(status_code=403, detail="Forbidden")

    results = collection_booking.find({"status": "Approved", "trip_completed": False})

    bookings = []
    for result in results:
        bookings.append(result)
    return bookings


@router.put("/approved/{id}/allocate")
async def allocate_resource(
    id: str,
    req: requestmodel.AllocationRequest,
    current_user: registerUser = Depends(get_current_user),
):
    if current_user["role"] not in {"admin", "super_admin"}:
        raise HTTPException(status_code=403, detail="Forbidden")
    result = collection_booking.update_one(
        {"_id": str(ObjectId(id)), "trip_completed": False},
        {
            "$set": {
                "name_of_driver": req.name,
                "phone_of_driver": req.phone,
                "vehicle_number": req.vehicle,
            }
        },
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")

    return {"success": True, "message": "Vehicle Alloted Successfully!"}


@router.put("/approved/{id}/completed")
async def complete_trip(
    id: str,
    req: requestmodel.TripCompleteRequest,
    current_user: registerUser = Depends(get_current_user),
):
    if current_user["role"] not in {"admin", "super_admin"}:
        raise HTTPException(status_code=403, detail="Forbidden")
    result = collection_booking.update_one(
        {"_id": str(ObjectId(id)), "trip_completed": False},
        {
            "$set": {
                "meter_reading_closing": req.end,
                "meter_reading_starting": req.start,
                "total_amount": req.total,
                "trip_completed": True,
                "trip_ID": req.trip_id,
                "meter_reading_total": req.end - req.start,
                "In Date": req.inDate,
                "In Time": req.inTime,
                "Out Date": req.outDate,
                "Out Time": req.outTime,
                "rate_per_km": req.total / (req.end - req.start),
            }
        },
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Booking not found")

    return {"success": True, "message": "Vehicle Alloted Successfully!"}


@router.get("/duty-slips", response_model=List[requestmodel.DutySlip])
def get_duty_slips(current_user: registerUser = Depends(get_current_user)):
    if current_user["role"] not in {"admin", "super_admin"}:
        raise HTTPException(status_code=403, detail="Forbidden")
    approved_trips = collection_booking.find(
        {
            "status": "Approved",
            "trip_completed": False,
            "name_of_driver": {"$ne": None},
            "vehicle_number": {"$ne": None},
        }
    )

    duty_slips = []
    for trip in approved_trips:
        duty_slip = requestmodel.DutySlip(
            name_of_driver=trip["name_of_driver"],
            vehicle_number=trip["vehicle_number"],
            date=trip["particulars"]["date"],
            time=trip["particulars"]["time"],
            place_of_visit=trip["particulars"]["place_of_visit"],
            purpose=trip["particulars"]["purpose"],
            num_people=trip["particulars"]["num_people"],
            booking_name=trip["particulars"]["name"],
            phone=trip["phone"],
            dep=trip["dep"],
            des=trip["des"],
            chargeable_head=trip["particulars"]["chargeable_head"],
        )
        duty_slips.append(duty_slip)

    return duty_slips
