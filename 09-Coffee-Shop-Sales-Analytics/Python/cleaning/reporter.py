import json
from pathlib import Path


class DataReporter:

    OUTPUT_FOLDER = Path("data/output")

    @staticmethod
    def save(df, cleaning_report, profile):

        DataReporter.OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

        # Save cleaned data
        df.to_csv(
            DataReporter.OUTPUT_FOLDER / "cleaned_data.csv",
            index=False
        )

        # Save JSON report
        with open(
            DataReporter.OUTPUT_FOLDER / "quality_report.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "cleaning": cleaning_report,
                    "profile": profile
                },
                f,
                indent=4,
                default=str
            )

        # Save log
        with open(
            DataReporter.OUTPUT_FOLDER / "cleaning_log.txt",
            "w",
            encoding="utf-8"
        ) as f:

            f.write("Cleaning completed successfully.\n")
            f.write(f"Rows: {len(df)}\n")