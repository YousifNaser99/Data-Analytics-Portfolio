import sys
import json
import traceback

from python.cleaning.loader import DataLoader
from python.cleaning.cleaner import DataCleaner
from python.cleaning.profiler import DataProfiler
from python.cleaning.reporter import DataReporter
from python.database.sql_loader import SQLLoader
from python.validation.validator import DataValidator


# ==========================================
# Get Input File From FastAPI
# ==========================================

if len(sys.argv) < 2:
    raise Exception("No input file provided.")

INPUT_FILE = sys.argv[1]


def main():

    try:

        # ============================
        # Load Dataset
        # ============================
        df = DataLoader.load(INPUT_FILE)

        # ============================
        # Cleaning
        # ============================
        cleaned_df, report = DataCleaner.clean(df)

        # ============================
        # Profiling
        # ============================
        profile = DataProfiler.profile(cleaned_df)

        # ============================
        # Save Reports
        # ============================
        DataReporter.save(
            cleaned_df,
            report,
            profile
        )

        # ============================
        # SQL Staging
        # ============================
        SQLLoader.load_dataframe(
            cleaned_df,
            "stg_coffee_sales"
        )

        # ============================
        # Validation
        # ============================
        validation = DataValidator.validate(
            report,
            profile
        )

        # ============================
        # Console Output
        # ============================
        print("=" * 60)
        print("Cleaning Finished")
        print("=" * 60)

        print("\nCleaning Report")
        print(report)

        print("\nData Profile")
        print(profile)

        print("\nValidation")
        print(validation)

        print("\nPreview")
        print(cleaned_df.head())

        # ============================
        # JSON Output For n8n
        # ============================
        print("\nVALIDATION_JSON_START")
        print(json.dumps(validation))
        print("VALIDATION_JSON_END")

        return validation


    except Exception as e:

        error_response = {
            "success": False,
            "stage": "Python Cleaning Pipeline",
            "file": INPUT_FILE,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

        print("\nPYTHON_ERROR_START")
        print(json.dumps(error_response))
        print("PYTHON_ERROR_END")

        raise


if __name__ == "__main__":
    main()