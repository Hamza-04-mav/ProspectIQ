"""
sheets_export.py
-----------------
Optional push-to-Google-Sheets integration using a service-account JSON
credential supplied at runtime through the sidebar (nothing is stored on disk).
"""

import json
from datetime import datetime
from typing import List, Dict


class SheetsExportError(Exception):
    pass


def push_to_google_sheet(
    leads: List[Dict],
    sheet_id: str,
    service_account_json: str,
    worksheet_name: str = "Sheet1",
) -> int:
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as exc:
        raise SheetsExportError(
            "The 'gspread' and 'google-auth' packages are required for Sheets export."
        ) from exc

    try:
        info = json.loads(service_account_json)
    except json.JSONDecodeError as exc:
        raise SheetsExportError("Service account JSON is not valid JSON.") from exc

    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(info, scopes=scopes)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id)
        try:
            worksheet = sheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title=worksheet_name, rows=1000, cols=10)

        existing = worksheet.get_all_values()
        if not existing:
            worksheet.append_row(
                ["Name", "Address", "Phone", "Rating", "Reviews", "Website",
                 "Prospect Score", "Tier", "Exported At"]
            )

        rows = [
            [
                lead.get("name", ""),
                lead.get("address", ""),
                lead.get("phone", ""),
                lead.get("rating", ""),
                lead.get("reviews", ""),
                lead.get("website") or "No website found",
                lead.get("prospect_score", ""),
                lead.get("tier", ""),
                datetime.utcnow().isoformat(timespec="seconds") + "Z",
            ]
            for lead in leads
        ]
        worksheet.append_rows(rows, value_input_option="USER_ENTERED")
        return len(rows)
    except SheetsExportError:
        raise
    except Exception as exc:
        raise SheetsExportError(f"Google Sheets export failed: {exc}") from exc
