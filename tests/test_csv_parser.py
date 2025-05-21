import pytest

from salary_reporter.csv_parser import load_employees_from_files, read_employees_from_file, HOURLY_RATE_NAMES

@pytest.mark.parametrize("rate_alias", HOURLY_RATE_NAMES)
def test_read_employees_from_file(temp_csv_file, rate_alias):
    content = f"id,email,name,department,hours_worked,{rate_alias}\n1,a@a.com,Alice,IT,100,25"
    path = temp_csv_file("test.csv", content)
    employees = read_employees_from_file(path)
    assert len(employees) == 1
    emp = employees[0]
    assert emp.id == 1
    assert emp.name == "Alice"
    assert emp.email == "a@a.com"
    assert emp.department == "IT"
    assert emp.hours_worked == 100
    assert emp.hourly_rate == 25
    assert emp.calculate_salary() == 2500

def test_read_employees_different_column_order(temp_csv_file):
    content = "name,salary,id,hours_worked,department,email\nCarol,40,3,150,Sales,c@c.com"
    path = temp_csv_file("test.csv", content)
    employees = read_employees_from_file(path)
    assert len(employees) == 1
    emp = employees[0]
    assert emp.id == 3
    assert emp.name == "Carol"
    assert emp.email == "c@c.com"
    assert emp.department == "Sales"
    assert emp.hours_worked == 150
    assert emp.hourly_rate == 40
    assert emp.calculate_salary() == 6000

def test_read_employees_missing_column(temp_csv_file):
    content = "id,email,name,hours_worked,hourly_rate\n1,a@a.com, Alice,100,25"
    path = temp_csv_file("test.csv", content)
    with pytest.raises(ValueError):
        read_employees_from_file(path)

def test_read_employees_empty_file(temp_csv_file):
    path = temp_csv_file("empty.csv", "")
    employees = read_employees_from_file(path)
    assert employees == []

def test_load_employees_from_files(temp_csv_file):
    content1 = "id,name,department,hours_worked,hourly_rate,email\n1,Alice1,IT,10,20,a1@a.com"
    content2 = "id,name,department,hours_worked,hourly_rate,email\n2,Alice2,HR,20,30,a2@a.com"
    path1 = temp_csv_file("test1.csv", content1)
    path2 = temp_csv_file("test2.csv", content2)
    employees = load_employees_from_files([path1, path2])
    assert len(employees) == 2
    assert employees[0].name == "Alice1"
    assert employees[1].name == "Alice2"

def test_load_employees_from_files_invalid_file(temp_csv_file):
    content = "id,name,department,hours_worked,hourly_rate,email\n1,Alice1,IT,10,20,a1@a.com"
    path = temp_csv_file("test.csv", content)
    employees = load_employees_from_files([path, "invalid.csv"])
    assert len(employees) == 1
    assert employees[0].name == "Alice1"
    