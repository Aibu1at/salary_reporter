import argparse
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from salary_reporter.csv_parser import load_employees_from_files
from salary_reporter.reporters import get_report_generator
from salary_reporter.formatters import get_output_formatter

def run_application(cli_args=None):
    parser = argparse.ArgumentParser(description="Генерация отчета по зарплате сотрудников")
    parser.add_argument("file_paths", nargs="+", help="Пути к файлам с данными сотрудников")
    parser.add_argument("--report", default="payout", help="Тип отчета (по умолчанию 'payout')")
    parser.add_argument("--format", default="text", help="Формат отчета (по умолчанию 'text')")
    args = parser.parse_args(cli_args)
    try:
        employees = load_employees_from_files(args.file_paths)
        if not employees:
            print("Нет данных для обработки.")
            sys.exit(1)
        report_generator = get_report_generator(args.report, employees)
        report_data = report_generator.generate_data()
        output_formatter = get_output_formatter(args.format, args.report)
        formatted_output = output_formatter.format(report_data)
        print(formatted_output)
    except FileNotFoundError as e: 
        print(f"Ошибка: файл не найден - {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except TypeError as e:
        print(f"Ошибка: неверный тип данных - {e}")
        sys.exit(1)
    except Exception as e: 
        print(f"Необработанная ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_application()