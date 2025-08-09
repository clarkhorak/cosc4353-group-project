from __future__ import annotations

import csv
import io
from typing import Literal, List, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, JSONResponse

from app.api.auth import get_current_user
from app.models.user import User
from app.services.report_service import ReportService
from app.utils.rbac import admin_required


router = APIRouter(prefix="/reports", tags=["reports"])

# Use a shared instance to avoid re-creating on every request
_report_service_instance = ReportService()

def get_report_service() -> ReportService:
    return _report_service_instance


def _rows_to_csv(rows: List[Dict[str, Any]]) -> bytes:
    if not rows:
        return b""
    output = io.StringIO()
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return output.getvalue().encode("utf-8")


def _rows_to_pdf(rows: List[Dict[str, Any]]) -> bytes:
    """Render a simple table PDF from rows using reportlab (imported lazily)."""
    if not rows:
        return b""

    # Lazy import to avoid hard dependency unless PDF is requested
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), leftMargin=18, rightMargin=18, topMargin=18, bottomMargin=18)

    fieldnames = list(rows[0].keys())
    data: List[List[Any]] = [fieldnames]
    for row in rows:
        data.append([row.get(k, "") for k in fieldnames])

    elements: List[Any] = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Report", styles["Title"]))

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0f0f0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()


@router.get("/volunteer-history")
@admin_required
async def volunteer_history_report(
    format: Literal["csv", "json", "pdf"] = Query("csv", description="Report output format"),
    current_user: User = Depends(get_current_user),
    report_service: ReportService = Depends(get_report_service),
):
    """Admin-only: List of volunteers and their participation history."""
    rows = report_service.get_volunteer_history_rows()
    if format == "json":
        return JSONResponse(content=rows)
    if format == "pdf":
        pdf_bytes = _rows_to_pdf(rows)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=volunteer_history.pdf"},
        )

    csv_bytes = _rows_to_csv(rows)
    return StreamingResponse(
        io.BytesIO(csv_bytes),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=volunteer_history.csv"},
    )


@router.get("/event-assignments")
@admin_required
async def event_assignments_report(
    format: Literal["csv", "json", "pdf"] = Query("csv", description="Report output format"),
    current_user: User = Depends(get_current_user),
    report_service: ReportService = Depends(get_report_service),
):
    """Admin-only: Event details and volunteer assignments."""
    rows = report_service.get_event_assignment_rows()
    if format == "json":
        return JSONResponse(content=rows)
    if format == "pdf":
        pdf_bytes = _rows_to_pdf(rows)
        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=event_assignments.pdf"},
        )

    csv_bytes = _rows_to_csv(rows)
    return StreamingResponse(
        io.BytesIO(csv_bytes),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=event_assignments.csv"},
    )


__all__ = ["router"]


