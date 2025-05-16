import json
from abc import ABC, abstractmethod
from typing import Any
from .models import Employee

class OutputFormatter(ABC):
    @abstractmethod
    def format(self, report_data: Any) -> str:
        pass

class TextPayoutFormatter(OutputFormatter):
    MARKER_SPACE_WIDTH = 15
    NAME_WIDTH = 19
    HOURS_WIDTH = 7
    RATE_WIDTH = 7
    PAYOUT_WIDTH = 7

    def format(self, report_data: dict[str, dict[str, Any]]) -> str:
        lines = []
        lines.append("")
        lines.append("")
        header_name_part = f"{'name':<{self.NAME_WIDTH}}"
        header_hours_part = f"{'hours':>{self.HOURS_WIDTH}}"
        header_rate_part = f"{'rate':>{self.RATE_WIDTH}}"
        header_payout_part = f"{'payout':>{self.PAYOUT_WIDTH}}"
        lines.append(
            f"{'':<{self.MARKER_SPACE_WIDTH}}"
            f"{header_name_part}"
            f"{header_hours_part}"
            f"{header_rate_part}"
            f"{header_payout_part}"
        )
        for dept_name, dept_info in report_data.items():
            lines.append(f"\n{dept_name}")
            dept_employees: list[Employee] = dept_info["employees"]
            for emp in dept_employees:
                payout_str = f"${emp.payout:>{self.PAYOUT_WIDTH - 1}.0f}"
                emp_line = (
                    f"{'-------------- ':<{self.MARKER_SPACE_WIDTH}}"
                    f"{emp.name:<{self.NAME_WIDTH}}"
                    f"{emp.hours_worked:>{self.HOURS_WIDTH}.0f}"
                    f"{emp.hourly_rate:>{self.RATE_WIDTH}.0f}"
                    f"{payout_str}"
                )
                lines.append(emp_line)
            total_payout_str = f"${dept_info['total_payout']:>{self.PAYOUT_WIDTH - 1}.0f}"
            total_line = (
                f"{'':<{self.MARKER_SPACE_WIDTH}}"
                f"{'':<{self.NAME_WIDTH}}"
                f"{dept_info['total_hours']:>{self.HOURS_WIDTH}.0f}"
                f"{'':>{self.RATE_WIDTH}}"
                f"{total_payout_str}"
            )
            lines.append(total_line)
        return "\n".join(lines)

class JsonOutputFormatter(OutputFormatter):
    def format(self, report_data: Any) -> str:
        def default_encoder(obj):
            if isinstance(obj, Employee):
                return obj.__dict__
            raise TypeError(f"Объект типа {obj.__class__.__name__} не сериализуем в JSON")
        try:
            return json.dumps(report_data, indent=2, default=default_encoder, ensure_ascii=False)
        except TypeError as e:
            print(f"ОШИБКА: Данные для JSON форматирования содержат несериализуемые объекты: {e}")
            raise

def get_output_formatter(format_name: str, report_type: str) -> OutputFormatter:
    format_name_lower = format_name.lower()
    report_type_lower = report_type.lower()
    if format_name_lower == "text":
        if report_type_lower == "payout":
            return TextPayoutFormatter()
        else:
            raise ValueError(
                f"Формат 'text' специфично реализован для отчета 'payout'. "
                f"Для типа отчета '{report_type}', пожалуйста, используйте 'json' или реализуйте соответствующий текстовый форматер."
            )
    elif format_name_lower == "json":
        return JsonOutputFormatter()
    else:
        raise ValueError(f"Неизвестный формат вывода: '{format_name}'. Поддерживаются: 'text' (для payout), 'json'.")