import pytest
import os
from salary_reporter.models import Employee

@pytest.fixture
def sample_employees():
    return [
        Employee(id="1", email="a@f.com", name="A B", department="Marketing", hours_worked=160, hourly_rate=50),
        Employee(id="2", email="b@f.com", name="C D", department="Design", hours_worked=150, hourly_rate=40),
        Employee(id="3", email="c@f.com", name="E F", department="Design", hours_worked=170, hourly_rate=60),
    ]

@pytest.fixture
def temp_csv_file(tmp_path):
    def _create_csv(filename: str, content: str):
        file_path = tmp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(file_path)
    return _create_csv