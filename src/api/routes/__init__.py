from fastapi import APIRouter

# Names exported for app.include_router calls
from . import generate, speak, render, provenance  # noqa: F401

router = APIRouter()

