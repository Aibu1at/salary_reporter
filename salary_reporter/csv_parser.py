from .models import Employee

HOURLY_RATE_NAMES = {"hourly_rate", "rate", "salary"}
HOURLY_RATE_TYPE = int
COLUMN_NAMES: dict[str, type | None] = {
    "id": int,
    "name": str,
    "email": str,
    "department": str,
    "hours_worked": int,
    # hourly_rate отдельно
}

def _find_column_indices(header: list[str]) -> dict[str, int]:
    column_indices: dict[str, int] = {}
    for i, column_name in enumerate(header):
        if column_name in HOURLY_RATE_NAMES:
            column_indices["hourly_rate"] = i
        elif column_name in COLUMN_NAMES:
            column_indices[column_name] = i
    if  column_indices.keys() != set(COLUMN_NAMES.keys()) | {"hourly_rate"}:
        raise ValueError(f"Отсутствует обязательная ячейка: {set(COLUMN_NAMES.keys()) | {"hourly_rate"} - column_indices.keys()}")
    return column_indices

def read_employees_from_file(file_path: str) -> list[Employee]:
    employees: list[Employee] = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        if not lines:
            return employees
        header = lines[0].strip().split(",")
        column_indices = _find_column_indices(header)
        for line_index, line in enumerate(lines[1:]):
            raw_values = line.strip().split(",")
            if len(raw_values) != len(header):
                print(f"Пропуск строки {line_index} из-за несоответствия количества ячеек: {line.strip()}")
                continue
            try:
                employee_data = {}
                for col_name, col_type in COLUMN_NAMES.items():
                    employee_data[col_name] = col_type(raw_values[column_indices[col_name]])
                hourly_rate_value = raw_values[column_indices["hourly_rate"]]
                employee_data["hourly_rate"] = HOURLY_RATE_TYPE(hourly_rate_value)
                employees.append(Employee(**employee_data))
            except ValueError as e:
                print(f"Ошибка преобразования данных в строке {line_index}: {line.strip()}. Ошибка: {e}")
    except FileNotFoundError:
        print(f"Файл не найден: {file_path}")
    return employees

def load_employees_from_files(file_paths: list[str]) -> list[Employee]:
    employees: list[Employee] = []
    for file_path in file_paths:
        employees.extend(read_employees_from_file(file_path))
    return employees
        
if __name__ == "__main__":
    file_paths = ["data_examples/data1.csv", "data_examples/data2.csv", "data_examples/data3.csv"]
    employees = load_employees_from_files(file_paths)
    for employee in employees:
        print(f"{employee.id:>4} {employee.name:>15} {employee.email:>17} {employee.department:>9} {employee.hourly_rate:>4} {employee.hours_worked:>4} {employee.calculate_salary():>5}")