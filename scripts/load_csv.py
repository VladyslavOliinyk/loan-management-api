"""Load CSV test data into the database."""

import csv
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database import Base, SessionLocal, engine
from app.models import Credit, Dictionary, Payment, Plan, User


def parse_date(value: str):
    if not value or not value.strip():
        return None
    return datetime.strptime(value.strip(), "%d.%m.%Y").date()


def load_csv(filepath: str, delimiter: str = "\t"):
    with open(filepath, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return list(reader)


def main():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Dictionary
        rows = load_csv(os.path.join(data_dir, "dictionary.csv"))
        for row in rows:
            db.add(Dictionary(id=int(row["id"]), name=row["name"].strip()))
        db.commit()
        print(f"Dictionary: {len(rows)} rows loaded")

        # Users
        rows = load_csv(os.path.join(data_dir, "users.csv"))
        for row in rows:
            db.add(
                User(
                    id=int(row["id"]),
                    login=row["login"].strip(),
                    registration_date=parse_date(row["registration_date"]),
                )
            )
        db.commit()
        print(f"Users: {len(rows)} rows loaded")

        # Credits
        rows = load_csv(os.path.join(data_dir, "credits.csv"))
        for row in rows:
            db.add(
                Credit(
                    id=int(row["id"]),
                    user_id=int(row["user_id"]),
                    issuance_date=parse_date(row["issuance_date"]),
                    return_date=parse_date(row["return_date"]),
                    actual_return_date=parse_date(row.get("actual_return_date", "")),
                    body=float(row["body"]),
                    percent=float(row["percent"].strip()),
                )
            )
        db.commit()
        print(f"Credits: {len(rows)} rows loaded")

        # Payments
        rows = load_csv(os.path.join(data_dir, "payments.csv"))
        for row in rows:
            db.add(
                Payment(
                    id=int(row["id"]),
                    sum=float(row["sum"].strip()),
                    payment_date=parse_date(row["payment_date"]),
                    credit_id=int(row["credit_id"]),
                    type_id=int(row["type_id"]),
                )
            )
        db.commit()
        print(f"Payments: {len(rows)} rows loaded")

        # Plans
        rows = load_csv(os.path.join(data_dir, "plans.csv"))
        for row in rows:
            db.add(
                Plan(
                    id=int(row["id"]),
                    period=parse_date(row["period"]),
                    sum=float(row["sum"]),
                    category_id=int(row["category_id"]),
                )
            )
        db.commit()
        print(f"Plans: {len(rows)} rows loaded")

        print("\nAll data loaded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
