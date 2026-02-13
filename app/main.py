from pprint import pprint
from typing import Dict
from fastapi import FastAPI
from pydantic import BaseModel
from .calendars import Nosotros, IM, WC, Velez, HolidaysCo, HolidaysAr, HolidaysUs

app = FastAPI()

nosotros = Nosotros()
im = IM()
holidays_co = HolidaysCo()
holidays_ar = HolidaysAr()
holidays_us = HolidaysUs()

class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"

@app.get("/health")
async def health_check():
    # You can add database checks here
    # db_status = check_database_connection()
    return HealthResponse(status="healthy")

@app.get("/health/detailed")
async def detailed_health():
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "available",
        "version": "1.0.0"
    }

@app.get("/holidays_co/all")
async def _holidays_co_all():
    """
    Retrieve values for riesgo pais
    """
    return {'events': holidays_co.events.all}

@app.get("/holidays_co/next")
async def _holidays_co_next():
    """
    Retrieve values for riesgo pais
    """
    return {'events': holidays_co.events.next}

@app.get("/holidays_ar/all")
async def _holidays_ar_all():
    """
    Retrieve values for riesgo pais
    """
    return {'events': holidays_ar.events.all}

@app.get("/holidays_ar/next")
async def _holidays_ar_next():
    """
    Retrieve values for riesgo pais
    """
    return {'events': holidays_ar.events.next}

@app.get("/holidays_us/all")
async def _holidays_us_all():
    """
    Retrieve values for riesgo pais
    """
    return {'events': holidays_us.events.all}

@app.get("/holidays_us/next")
async def _holidays_us_next():
    """
    Retrieve values for riesgo pais
    """
    return {'events': holidays_us.events.next}

@app.get("/nosotros/all")
async def _nosotros_all():
    """
    Retrieve values for riesgo pais
    """
    return {'events': nosotros.events.all}

@app.get("/nosotros/next")
async def _nosotros_next():
    """
    Retrieve values for riesgo pais
    """
    return {'events': nosotros.events.next}

@app.get("/nosotros/rest")
async def _nosotros_rest():
    """
    Retrieve values for riesgo pais
    """
    return {'events': nosotros.events.rest}

@app.get("/nosotros/ongoing")
async def _nosotros_ongoing():
    """
    Retrieve values for riesgo pais
    """
    return {'events': nosotros.events.ongoing}

@app.get("/nosotros/today")
async def _nosotros_today():
    """
    Retrieve values for riesgo pais
    """
    return {'events': nosotros.events.today}

@app.get("/nosotros/tomorrow")
async def _nosotros_tomorrow():
    """
    Retrieve values for riesgo pais
    """
    return {'events': nosotros.events.tomorrow}

@app.get("/im/today")
async def _im_today():
    """
    Retrieve values for riesgo pais
    """
    return {'events': im.events.today}

@app.get("/im/tomorrow")
async def _im_tomorrow():
    """
    Retrieve values for riesgo pais
    """
    return {'events': im.events.tomorrow}

@app.get("/im/next")
async def _im_next():
    """
    Retrieve values for riesgo pais
    """
    return {'events': im.events.next}
