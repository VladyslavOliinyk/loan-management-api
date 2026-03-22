from datetime import date

from pydantic import BaseModel


class ClosedCreditResponse(BaseModel):
    issuance_date: date
    is_closed: bool = True
    actual_return_date: date
    body: float
    percent: float
    total_payments: float


class OpenCreditResponse(BaseModel):
    issuance_date: date
    is_closed: bool = False
    return_date: date
    overdue_days: int
    body: float
    percent: float
    body_payments: float
    percent_payments: float


class PlansInsertResponse(BaseModel):
    message: str


class PlanPerformanceItem(BaseModel):
    month: date
    category: str
    plan_sum: float
    fact_sum: float
    performance_percent: float


class PlanPerformanceResponse(BaseModel):
    items: list[PlanPerformanceItem]


class YearPerformanceItem(BaseModel):
    month: date
    issuance_count: int
    issuance_plan: float
    issuance_fact: float
    issuance_percent: float
    payment_count: int
    collection_plan: float
    collection_fact: float
    collection_percent: float
    issuance_year_share: float
    payment_year_share: float


class YearPerformanceResponse(BaseModel):
    items: list[YearPerformanceItem]
