"""
validator.py
------------
Validation Engine
Responsible for validating the cleaned dataset
before moving to Production.
"""

from typing import Dict


class DataValidator:

    @staticmethod
    def validate(cleaning_report: Dict, profile: Dict) -> Dict:

        quality_score = profile.get("quality_score", 0)

        missing_values = profile.get("missing_values", 0)

        duplicate_rows = profile.get("duplicate_rows", 0)

        rows_before = cleaning_report.get("rows_before", 0)

        rows_after = cleaning_report.get("rows_after", 0)

        status = "SUCCESS"

        reasons = []

        if quality_score < 95:
            status = "FAILED"
            reasons.append("Quality Score below threshold")

        if rows_after == 0:
            status = "FAILED"
            reasons.append("Dataset is empty")

        validation = {

            "status": status,

            "quality_score": quality_score,

            "rows_before": rows_before,

            "rows_after": rows_after,

            "missing_values": missing_values,

            "duplicate_rows": duplicate_rows,

            "sql_loaded": status == "SUCCESS",

            "reasons": reasons

        }

        return validation