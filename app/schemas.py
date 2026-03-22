from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class ClosedCreditResponse(BaseModel):
    issuance_date: date
    is_closed: bool = True
    actual_return_date: date
    body: Decimal
    percent: Decimal
    total_payments: Decimal


class OpenCreditResponse(BaseModel):
    issuance_date: date
    is_closed: bool = False
    return_date: date
    overdue_days: int
    body: Decimal
    percent: Decimal
    body_payments: Decimal
    percent_payments: Decimal


class PlansInsertResponse(BaseModel):
    message: str


class PlanPerformanceItem(BaseModel):
    month: date
    category: str
    plan_sum: Decimal
    fact_sum: Decimal
    performance_percent: Decimal


class PlanPerformanceResponse(BaseModel):
    items: list[PlanPerformanceItem]


class YearPerformanceItem(BaseModel):
    month: date
    issuance_count: int
    issuance_plan: Decimal
    issuance_fact: Decimal
    issuance_percent: Decimal
    payment_count: int
    collection_plan: Decimal
    collection_fact: Decimal
    collection_percent: Decimal
    issuance_year_share: Decimal
    payment_year_share: Decimal


class YearPerformanceResponse(BaseModel):
    items: list[YearPerformanceItem]
