import pytest
import json

from salary_reporter.main import run_application

@pytest.fixture
def create_test_files(temp_csv_file):
    file1_content = (
        "id,email,name,department,hours_worked,hourly_rate\n"
        "1,alice@example.com,Alice Johnson,Marketing,160,50\n"
        "2,bob@example.com,Bob Smith,Design,150,40\n"
        "3,carol@example.com,Carol Williams,Design,170,60"
    )
    file2_content = (
        "department,id,email,name,hours_worked,rate\n"
        "HR,101,grace@example.com,Grace Lee,160,45\n"
        "Marketing,102,henry@example.com,Henry Martin,150,35\n"
        "HR,103,ivy@example.com,Ivy Clark,158,38"
    )
    file3_content = (
        "email,name,department,hours_worked,salary,id\n"
        "karen@example.com,Karen White,Sales,165,50,201\n"
        "liam@example.com,Liam Harris,HR,155,42,202\n"
        "mia@example.com,Mia Young,Sales,160,37,203"
    )
    paths = [temp_csv_file("data1.csv", file1_content),
             temp_csv_file("data2.csv", file2_content),
             temp_csv_file("data3.csv", file3_content)]
    return paths

def test_run_application_text(create_test_files, capsys):
    csv_files = create_test_files
    cli_args = csv_files + ["--format", "text", "--report", "payout"]
    
    run_application(cli_args)
    captured = capsys.readouterr()
    output = captured.out

    assert "Design" in output
    assert "Bob Smith" in output and "$6000" in output
    assert "Carol Williams" in output and "$10200" in output
    assert "$16200" in output

    assert "HR" in output
    assert "Grace Lee" in output and "$7200" in output
    assert "Ivy Clark" in output and "$6004" in output
    assert "Liam Harris" in output and "$6510" in output
    assert "$19714" in output

    assert "Marketing" in output
    assert "Alice Johnson" in output and "$8000" in output
    assert "Henry Martin" in output and "$5250" in output
    assert "$13250" in output

    assert "Sales" in output
    assert "Karen White" in output and "$8250" in output
    assert "Mia Young" in output and "$5920" in output
    assert "$14170" in output

def test_run_application_json(temp_csv_file, capsys):
    content = "id,name,department,hours_worked,rate,email\n1,Json Test,JSON_Dept,10,5,j@j.com"
    file_path = temp_csv_file("json_test.csv", content)
    cli_args = [file_path, "--format", "json", "--report", "payout"]
    run_application(cli_args)
    captured = capsys.readouterr()

    data = json.loads(captured.out)
    assert "JSON_Dept" in data
    assert data["JSON_Dept"]["employees"][0]["name"] == "Json Test"
    assert data["JSON_Dept"]["total_payout"] == 50.0

def test_run_application_file_not_found():
    with pytest.raises(SystemExit):
        run_application(["non_existent_file.csv", "--format", "json", "--report", "payout"])

def test_run_application_unknown_report(temp_csv_file):
    file_path = temp_csv_file("dummy.csv", "id,name,dept,hours,rate,email\n1,N,D,1,1,e@e.com")
    cli_args = [file_path, "--report", "weird_report"]
    with pytest.raises(SystemExit):
        run_application(cli_args)

    