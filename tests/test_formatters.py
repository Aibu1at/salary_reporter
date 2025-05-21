import pytest
import json

from salary_reporter.formatters import get_output_formatter, TextPayoutFormatter, JsonOutputFormatter
from salary_reporter.reporters import PayoutReport

def test_text_payout_formatter(sample_employees):
    payout_report_generator = PayoutReport(sample_employees)
    report_data = payout_report_generator.generate_data()

    formatter = TextPayoutFormatter()
    output_string = formatter.format(report_data)

    expected_lines = [
        "",
        "",
        f"{'':<15}{'name':<19}{'hours':>7}{'rate':>7}{'payout':>7}",
        "",
        "Design",
        f"{'-------------- ':<15}{'C D':<19}{150:>7.0f}{40:>7.0f}{'$'}{6000:>6.0f}",
        f"{'-------------- ':<15}{'E F':<19}{170:>7.0f}{60:>7.0f}{'$'}{10200:>6.0f}",
        f"{'':<15}{'':<19}{320:>7.0f}{'':>7}{'$'}{16200:>6.0f}",
        "",
        "Marketing",
        f"{'-------------- ':<15}{'A B':<19}{160:>7.0f}{50:>7.0f}{'$'}{8000:>6.0f}",
        f"{'':<15}{'':<19}{160:>7.0f}{'':>7}{'$'}{8000:>6.0f}",
    ]
    
    actual_lines = output_string.splitlines()
    while actual_lines and not actual_lines[-1].strip():
        actual_lines.pop()
        

def test_json_output_formatter(sample_employees):
    payout_report_generator = PayoutReport(sample_employees)
    report_data = payout_report_generator.generate_data()

    formatter = JsonOutputFormatter()
    json_string = formatter.format(report_data)
    output_data = json.loads(json_string)

    assert "Design" in output_data
    assert len(output_data["Design"]["employees"]) == 2
    assert output_data["Design"]["employees"][0]["name"] == "C D" 
    assert output_data["Design"]["total_payout"] == 16200.0

    assert "Marketing" in output_data
    assert output_data["Marketing"]["employees"][0]["name"] == "A B"
    assert output_data["Marketing"]["total_payout"] == 8000.0

def test_get_output_formatter():
    assert isinstance(get_output_formatter("text", "payout"), TextPayoutFormatter)
    assert isinstance(get_output_formatter("json", "payout"), JsonOutputFormatter)
    with pytest.raises(ValueError):
        get_output_formatter("unknown_format", "payout")
    with pytest.raises(ValueError):
        get_output_formatter("text", "unknown_report")

