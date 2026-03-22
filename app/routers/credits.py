from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Credit, Payment
from app.schemas import ClosedCreditResponse, OpenCreditResponse

router = APIRouter()


@router.get("/user_credits/{user_id}")
def get_user_credits(
    user_id: int, db: Session = Depends(get_db)
) -> list[ClosedCreditResponse | OpenCreditResponse]:
    credits = db.query(Credit).filter(Credit.user_id == user_id).all()

    if not credits:
        raise HTTPException(status_code=404, detail="No credits found for this user")

    result = []
    for credit in credits:
        if credit.actual_return_date is not None:
            total_payments = (
                db.query(func.coalesce(func.sum(Payment.sum), 0))
                .filter(Payment.credit_id == credit.id)
                .scalar()
            )
            result.append(
                ClosedCreditResponse(
                    issuance_date=credit.issuance_date,
                    actual_return_date=credit.actual_return_date,
                    body=credit.body,
                    percent=credit.percent,
                    total_payments=float(total_payments),
                )
            )
        else:
            overdue_days = max((date.today() - credit.return_date).days, 0)
            body_payments = (
                db.query(func.coalesce(func.sum(Payment.sum), 0))
                .filter(Payment.credit_id == credit.id, Payment.type_id == 1)
                .scalar()
            )
            percent_payments = (
                db.query(func.coalesce(func.sum(Payment.sum), 0))
                .filter(Payment.credit_id == credit.id, Payment.type_id == 2)
                .scalar()
            )
            result.append(
                OpenCreditResponse(
                    issuance_date=credit.issuance_date,
                    return_date=credit.return_date,
                    overdue_days=overdue_days,
                    body=credit.body,
                    percent=credit.percent,
                    body_payments=float(body_payments),
                    percent_payments=float(percent_payments),
                )
            )

    return result
