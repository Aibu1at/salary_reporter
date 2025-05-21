import pytest

from salary_reporter.reporters import get_report_generator, PayoutReport

def test_payout_report(sample_employees):
    report = PayoutReport(sample_employees)
    report_data = report.generate_data()

    assert len(report_data) == 2
    assert "Marketing" in report_data
    assert "Design" in report_data

    marketing_dept = report_data["Marketing"]
    design_dept = report_data["Design"]

    assert len(marketing_dept["employees"]) == 1
    assert marketing_dept["total_hours"] == 160
    assert marketing_dept["total_payout"] == 8000

    assert len(design_dept["employees"]) == 2
    assert design_dept["total_hours"] == 320
    assert design_dept["total_payout"] == 16200

def test_get_report_generator(sample_employees):
    report = get_report_generator("payout", sample_employees)
    assert isinstance(report, PayoutReport)
    with pytest.raises(ValueError):
        get_report_generator("unknown_report", sample_employees)

