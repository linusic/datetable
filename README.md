## Usage
```python
from datetable import DateTable

# put a year
dt = DateTable(2022) 

# judge workday
print(dt.is_workday("20220101"))               # 0 
print(dt.is_workday(1700000000))               # 1

# get format rule
print(DateTable.get_format_rules())  # ['YYYY-MM-DD HH:mm:ss', 'YYYY-MM-DD', 'YYYYMMDD', ...]

# to_date
print(DateTable.to_date("20220101")) # 2022-01-01
print(DateTable.to_date("2022-1-1")) # 2022-01-01
print(DateTable.to_date(1800000000)) # 2027-01-15

# make holiday table to file
file_path = "./date.csv"
dt.make_to_file(file_path, sep="\t", head=False)
```


`make_to_file(..., head=True)` result sample
```csv
Date	Year	Month	Day	Week	WeekOfYear	Quarter	IsWeekDay	Holiday
2022-01-01	2022	1	1	6	52	1	0	元旦
2022-01-02	2022	1	2	0	52	1	0	元旦
2022-01-03	2022	1	3	1	1	1	0	元旦
2022-01-04	2022	1	4	2	1	1	1	\N
2022-01-05	2022	1	5	3	1	1	1	\N
...
```
## Modify
change below in `datetable.py` to yours
```python
# Holiday Range
YuanDan = ("01-01", "01-03")  # "01-01", "01-02", "01-03"
...

# Even on "Saturday" or "Sunday", you still need to work
BLACK_WORKDAY = [
    "01-29",  
    ...
]

# Named Holiday
HOLIDAY_DICT = {
    "<HOLIDAY_NAME>":YuanDan,    # named "Holiday" column of result
    ...
}
```
