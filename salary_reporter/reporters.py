from abc import ABC, abstractmethod
from typing import List, Dict, Any
from .models import Employee

class Report(ABC):
    def __init__(self, employees: List[Employee]):
        self.employees = employees

    @abstractmethod
    def generate_data(self) -> Any:
        pass

class PayoutReport(Report):
    def generate_data(self) -> Dict[str, Dict[str, Any]]:
        department_summary: Dict[str, Dict[str, Any]] = {}
        for emp in self.employees:
            dept_key = emp.department
            if dept_key not in department_summary:
                department_summary[dept_key] = {
                    "employees": [],
                    "total_hours": 0.0,
                    "total_payout": 0.0
                }
            department_summary[dept_key]["employees"].append(emp)
            department_summary[dept_key]["total_hours"] += emp.hours_worked
            if emp.payout is not None:
                department_summary[dept_key]["total_payout"] += emp.payout
        
        for dept_name in department_summary:
            department_summary[dept_name]["employees"].sort(key=lambda employee: employee.name)
            
        return dict(sorted(department_summary.items()))

def get_report_generator(report_name: str, employees: List[Employee]) -> Report:
    report_name_lower = report_name.lower()
    if report_name_lower == "payout":
        return PayoutReport(employees)
    else:
        raise ValueError(f"Неизвестный тип отчета: {report_name}. Доступен толко отчет 'payout'.")