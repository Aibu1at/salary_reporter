# Генератор отчетов по зарплатам

Python-скрипт для составления отчетов по сотрудникам.

## Функционал

* Чтение нескольких CSV-файлов
* Гибкий парсинг:
    * Любой порядок столбцов в csv файлах
    * Обработка разных имен почасовой ставки: `hourly_rate`, `rate`, `salary`
* Генерация отчета `payout`: группировка по отделам, индивидульные и общие выплаты по отделам
* Форматы вывода:
    * Текстовая таблица (пример ниже)
    * json
* Только стандартная библиотека, без библиотеки csv (согласно тз)
*  Тесты на pytest, покрытие 80%+



##  Установка

1. Клонировать репозиторий.

2. Окружение и зависимости (для тестов):

    ```
    python -m venv venv && source venv/bin/activate && pip install -r requirements-dev.txt
    ```

## Использование

Синтаксис команды:
```
python main.py <файлы.csv> --report <тип> [--format <формат>]
```

Пример (отчет payout, текстовый формат):

```
python salary_reporter/main.py data_examples/data1.csv data_examples/data2.csv data_examples/data3.csv --report payout
```

Вывод:
```
               name               hours  rate   payout    

Design
-------------- Bob Smith          150    40     $6000    
-------------- Carol Williams     170    60     $10200   
                                  320           $16200   

HR
-------------- Grace Lee          160    45     $7200    
-------------- Ivy Clark          158    38     $6004    
-------------- Liam Harris        155    42     $6510    
                                  473           $19714   

Marketing
-------------- Alice Johnson      160    50     $8000    
-------------- Henry Martin       150    35     $5250    
                                  310           $13250   

Sales
-------------- Karen White        165    50     $8250    
-------------- Mia Young          160    37     $5920    
                                  325           $14170   
```


## Тесты

Все: 
```
pytest
```

С покрытием: 
```
pytest --cov=salary_calculator --cov-report term-missing
```

