from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, extract, func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Credit, Payment, Plan
from app.schemas import YearPerformanceItem, YearPerformanceResponse

router = APIRouter()

ISSUANCE_CATEGORY_ID = 3
COLLECTION_CATEGORY_ID = 4


@router.get("/year_performance", response_model=YearPerformanceResponse)
def get_year_performance(year: int = Query(...), db: Session = Depends(get_db)):
    year_total_issuance = float(
        db.query(func.coalesce(func.sum(Credit.body), 0))
        .filter(extract("year", Credit.issuance_date) == year)
        .scalar()
    )
    year_total_payments = float(
        db.query(func.coalesce(func.sum(Payment.sum), 0))
        .filter(extract("year", Payment.payment_date) == year)
        .scalar()
    )

    items = []
    for month in range(1, 13):
        month_start = date(year, month, 1)
        if month == 12:
            month_end = date(year, 12, 31)
        else:
            month_end = date(year, month + 1, 1)

        issuance_count = (
            db.query(func.count(Credit.id))
            .filter(
                and_(
                    Credit.issuance_date >= month_start,
                    Credit.issuance_date < month_end,
                )
            )
            .scalar()
        )

        issuance_fact = float(
            db.query(func.coalesce(func.sum(Credit.body), 0))
            .filter(
                and_(
                    Credit.issuance_date >= month_start,
                    Credit.issuance_date < month_end,
                )
            )
            .scalar()
        )

        issuance_plan = float(
            db.query(func.coalesce(func.sum(Plan.sum), 0))
            .filter(Plan.period == month_start, Plan.category_id == ISSUANCE_CATEGORY_ID)
            .scalar()
        )

        payment_count = (
            db.query(func.count(Payment.id))
            .filter(
                and_(
                    Payment.payment_date >= month_start,
                    Payment.payment_date < month_end,
                )
            )
            .scalar()
        )

        collection_fact = float(
            db.query(func.coalesce(func.sum(Payment.sum), 0))
            .filter(
                and_(
                    Payment.payment_date >= month_start,
                    Payment.payment_date < month_end,
                )
            )
            .scalar()
        )

        collection_plan = float(
            db.query(func.coalesce(func.sum(Plan.sum), 0))
            .filter(Plan.period == month_start, Plan.category_id == COLLECTION_CATEGORY_ID)
            .scalar()
        )

        issuance_percent = (
            (issuance_fact / issuance_plan * 100) if issuance_plan else 0
        )
        collection_percent = (
            (collection_fact / collection_plan * 100) if collection_plan else 0
        )
        issuance_year_share = (
            (issuance_fact / year_total_issuance * 100)
            if year_total_issuance
            else 0
        )
        payment_year_share = (
            (collection_fact / year_total_payments * 100)
            if year_total_payments
            else 0
        )

        items.append(
            YearPerformanceItem(
                month=month_start,
                issuance_count=issuance_count,
                issuance_plan=issuance_plan,
                issuance_fact=issuance_fact,
                issuance_percent=round(issuance_percent, 2),
                payment_count=payment_count,
                collection_plan=collection_plan,
                collection_fact=collection_fact,
                collection_percent=round(collection_percent, 2),
                issuance_year_share=round(issuance_year_share, 2),
                payment_year_share=round(payment_year_share, 2),
            )
        )

    return YearPerformanceResponse(items=items)
