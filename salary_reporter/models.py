from dataclasses import dataclass

@dataclass
class Employee:
    id: int
    name: str
    email: str
    department: str
    hourly_rate: int # В примерах везде int, так что оставим int
    hours_worked: int # То же самое

    def calculate_salary(self) -> int:
        return self.hourly_rate * self.hours_worked