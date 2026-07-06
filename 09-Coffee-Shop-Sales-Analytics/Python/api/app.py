from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import subprocess
import traceback
import zipfile

app = FastAPI()

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FOLDER = PROJECT_ROOT / "data" / "input"
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "output"

INPUT_FOLDER.mkdir(parents=True, exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# ==========================================================
# Home
# ==========================================================

@app.get("/")
def home():
    return {
        "status": "running",
        "service": "AI Data Analysis Platform"
    }


# ==========================================================
# Run Cleaning Pipeline
# ==========================================================

@app.post("/run-cleaning")
async def run_cleaning(file: UploadFile = File(...)):

    try:

        # Save uploaded file
        file_path = INPUT_FOLDER / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run cleaning pipeline
        result = subprocess.run(
            [
                "python",
                "-m",
                "python.cleaning.clean_data",
                str(file_path)
            ],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {
                "success": False,
                "stage": "FastAPI",
                "message": "Python Cleaning Pipeline Failed",
                "return_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "saved_file": str(file_path)
            }

        return {
            "success": True,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "saved_file": str(file_path)
        }

    except Exception as e:
        return {
            "success": False,
            "stage": "FastAPI",
            "message": str(e),
            "traceback": traceback.format_exc()
        }


# ==========================================================
# Download Cleaned CSV
# ==========================================================

@app.get("/reports/cleaned-data")
def cleaned_data():

    file_path = OUTPUT_FOLDER / "cleaned_data.csv"

    return FileResponse(
        path=file_path,
        filename="cleaned_data.csv",
        media_type="text/csv"
    )


# ==========================================================
# Download Quality Report
# ==========================================================

@app.get("/reports/quality-report")
def quality_report():

    file_path = OUTPUT_FOLDER / "quality_report.json"

    return FileResponse(
        path=file_path,
        filename="quality_report.json",
        media_type="application/json"
    )


# ==========================================================
# Download Cleaning Log
# ==========================================================

@app.get("/reports/cleaning-log")
def cleaning_log():

    file_path = OUTPUT_FOLDER / "cleaning_log.txt"

    return FileResponse(
        path=file_path,
        filename="cleaning_log.txt",
        media_type="text/plain"
    )


# ==========================================================
# Download All Reports (ZIP)
# ==========================================================

@app.get("/reports/download-all")
def download_all_reports():

    zip_path = OUTPUT_FOLDER / "reports.zip"

    files = [
        "cleaned_data.csv",
        "quality_report.json",
        "cleaning_log.txt"
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

        for file_name in files:

            file_path = OUTPUT_FOLDER / file_name

            if file_path.exists():
                zipf.write(file_path, arcname=file_name)

    return FileResponse(
        path=zip_path,
        filename="reports.zip",
        media_type="application/zip"
    )