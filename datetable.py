"""Date Format
STD datetime date format:
    => https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

pendulum date format:
    => https://pendulum.eustace.io/docs/#tokens
"""


""" 常识
国内/国际(也是 标准ISO8601协议):
    若1月1号是   周1:
        那么这就是 第1周
    若1月1号不是 周1:
        那么向后推, 直到周1 为止, 这段期间算是第一周;
        从周1开始, 算是第2周

国外特殊习惯: 
    把上述周1 换成 周日 , 再推下来即可

pendulum默认:
    默认采用 ISO8601 =>也即 (周1-周日) 为完整的一周 (符合习惯)

    # print(pendulum.MONDAY)    # 1
    # print(pendulum.TUESDAY)   # 2
    # print(pendulum.WEDNESDAY) # 3
    # print(pendulum.THURSDAY)  # 4
    # print(pendulum.FRIDAY)    # 5
    # print(pendulum.SATURDAY)  # 6
    # print(pendulum.SUNDAY)    # 0  - 星期日
"""

from typing import Generator
from pathlib import Path
from itertools import product
from datetime import date, datetime

import pendulum
from pendulum.date import Date
from pendulum.datetime import DateTime

class DateTable:
    ### 声明阶段: 节假日-具体看每年 务院官方网站通知 (从1月1日开始)
    # 元旦：2022年1月1日至3日放假，共3天。
    YuanDan = ("01-01", "01-03")  # from "01-01" to "01-03"  => "01-01", "01-02", "01-03"
    # 春节：1月31日至2月6日放假调休，共7天。1月29日（星期六）、1月30日（星期日）上班。
    ChunJie = ("01-31", "02-06")
    # 清明节：4月3日至5日放假调休，共3天。4月2日（星期六）上班。
    QingMing = ("04-03", "04-05")
    # 劳动节：4月30日至5月4日放假调休，共5天。4月24日（星期日）、5月7日（星期六）上班。
    LaoDong = ("04-30", "05-04")
    # 端午节：6月3日至5日放假，共3天。
    DuanWu = ("06-03", "06-05")
    # 中秋节：9月10日至12日放假，共3天。
    ZhongQiu = ("09-10", "09-12")
    # 国庆节：10月1日至7日放假调休，共7天。10月8日（星期六）、10月9日（星期日）上班。
    GuoQing = ("10-01", "10-07")

    # 特殊情况:
    # 若有重叠, 则可额外添加 逗号并列声明, eg:
    # ZhongQiuGuoQing = (..., ...)

    BLACK_WORKDAY = [
        "01-29", # 六
        "01-30", # 日
        "04-02", # 六
        "04-24", # 日
        "05-07", # 六
        "10-08", # 六
        "10-09", # 日
    ]

    HOLIDAY_DICT = {
        "元旦":YuanDan,
        "春节":ChunJie,
        "清明节":QingMing,
        "劳动节":LaoDong,
        "端午节":DuanWu,
        "中秋节":ZhongQiu,
        "国庆节":GuoQing,
        # 若有重叠, 则可逗号并列声明为, eg:
        # "中秋节,国庆节": ZhongQiuGuoQing
    }

    def __init__(self, year:int) -> None:
        self.year = year

    def handle_black_workday(self) -> list:
        new_black_workday = []
        for month_day in self.BLACK_WORKDAY:
            black_m, black_d = month_day.split("-")
            new_black_workday.append( str(pendulum.datetime(self.year, int(black_m), int(black_d)).date()) )
        return new_black_workday

    def gen_holiday_seq(self) -> Generator:
        for start, end in self.HOLIDAY_DICT.values():
            start_m, start_d = start.split("-")
            start_dt = pendulum.datetime(self.year, int(start_m), int(start_d)).date()
            end_m, end_d = end.split("-")
            end_dt = pendulum.datetime(self.year, int(end_m), int(end_d)).date()

            period = pendulum.period(start_dt, end_dt)
            yield list(map(str,period.range("days", 1)))

    def get_holiday_index(self):
        # 正序索引  {'YuanDan': ['2022-01-01', '2022-01-02', '2022-01-03'], 
        return dict(zip(self.HOLIDAY_DICT.keys(), self.gen_holiday_seq()) )

    def get_holiday_reverse_index(self):
        holiday_reverse_index = self.get_holiday_index()
        # 倒排索引  {'2022-01-01': 'YuanDan', '2022-01-02': 'YuanDan', ...}
        return { 
            y[i]:x for x,y in holiday_reverse_index.items()
            for i in range(len(y))
        }
    
    def get_holidays_eval_date(self):
        # 所有节假日日期列表
        holiday_index = self.get_holiday_index()
        return sum(holiday_index.values(), start=[])


    def day_list(self) -> list[Date]:
        start = pendulum.datetime(self.year, 1, 1, tz="Asia/Shanghai")
        end = pendulum.datetime(self.year, 12, 31, tz="Asia/Shanghai")

        period = pendulum.period(start, end) 

        # 为了后续使用方便, 此处直接返回 Data对象
            # 若不格式化, 直接: str() 强转即可
            # 转成格式化字符串: dt.format("YYYY-MM-DD")  或 "Y-M-D"
            # 格式化也可用    : f-string  
        return [dt.date() for dt in period.range('days', 1)]

    @staticmethod
    def get_format_rules(date_sep="-", time_sep=":", datetim_sep=" "):
        year_combo  = ["YYYY", "YY"]
        month_combo = ["MM", "M"]
        day_combo   = ["DD", "D"]

        hour_combo   = ["HH", "H"]
        minute_combo = ["mm", "m"]
        second_combo = ["ss", "s"]

        date_rule_list = [date_sep.join(_tuple) for _tuple in product(year_combo, month_combo, day_combo)]
        time_rule_list = [time_sep.join(_tuple) for _tuple in product(hour_combo, minute_combo, second_combo)]

        datetime_rule_list = [datetim_sep.join(_tuple) for _tuple in product(date_rule_list, time_rule_list)]
        result_rule_list = date_rule_list + datetime_rule_list

        result_rule_list.remove("YYYY-MM-DD HH:mm:ss")
        result_rule_list.insert(0, "YYYY-MM-DD HH:mm:ss") # 将习惯格式放在最前, 便于优化后续扫描 (查到即终止)
        result_rule_list.insert(2, "YYYYMMDD") # 将习惯格式放在最前, 便于优化后续扫描 (查到即终止)
        result_rule_list.insert(3, "YYYYMMDDHHmmss") # 将习惯格式放在最前, 便于优化后续扫描 (查到即终止)

        return result_rule_list

    @staticmethod
    def to_date(date_one: int|float|str|date|datetime|Date|DateTime, fmt="") -> Date:
        """Usage:
            print( to_date("20220212 23:08:12", "YYYYMMDD HH:mm:ss") ) # 2022-02-12
            print( to_date(datetime.now(), "YYYYMMDD HH:mm:ss") )      # 2022-11-07
            print( to_date(1750000000, "YYYYMMDD HH:mm:ss") )          # 2025-06-15
            print( to_date([1,2,3]) )                                  # Exception: not support type: <class 'list'>
        """

        if isinstance(date_one, (date, datetime, Date, DateTime) ):
            return pendulum.date(date_one.year, date_one.month, date_one.day)

        elif isinstance(date_one, str):
            rule_list = DateTable.get_format_rules()

            search_format_result = None
            for rule_fmt in rule_list:
                # datetime.strptime(date_one, fmt).date() # 标准库写法 (不过标准库只支持: "%Y-%m-%d %H:%M:%S" 这种格式)
                try:
                    search_format_result = pendulum.from_format(date_one, rule_fmt)
                    break
                except:
                    continue

            if not search_format_result:
                try:
                    return pendulum.from_format(date_one, fmt)
                except:
                    raise Exception(f'Format Failded! you must put the fmt argument, eg: fmt="YYYY-MM-DD HH:mm:ss.SSS-zz" ')

            return search_format_result.date()

        elif isinstance(date_one, (int, float)):
            # return datetime.fromtimestamp(date_one).date()     # 标准库写法
            return pendulum.from_timestamp(date_one).date() # 同样用 datetime 中转
        else:
            raise Exception(f"not support type: {type(date_one)}")


    def is_workday(self, date_one: int|float|str|date|datetime|Date|DateTime) -> int:
        """Usage:
            print(is_workday("20220103"))  # 0 - 节假日
            print(is_workday("2022-01-4")) # 1 - 工作日
        """
        date_one = DateTable.to_date(date_one)

        new_black_workday_list = self.handle_black_workday()
        holidays_eval_date_list = self.get_holidays_eval_date()
        
        if str(date_one) in holidays_eval_date_list \
        or  \
        date_one.day_of_week in [6,0]   and   str(date_one) not in new_black_workday_list:
            is_work_day = 0
        else:
            is_work_day = 1
        return is_work_day

    def make_date_csv_str(self, date_one:Date, sep="\t") -> str:
        temp_list = []

        temp_list.append(str(date_one))          # 原日期作为主键ID

        temp_list.append(date_one.year)          # 年 (无API,默认取属性)
        temp_list.append(date_one.month)         # 月 (无API,默认取属性)
        temp_list.append(date_one.day)           # 天 (无API,默认取属性)
        temp_list.append(date_one.day_of_week)   # 1代表周1 (0是周日)   => 周几
        temp_list.append(date_one.week_of_year)  # 1-based   => 一年之中的第几周
        # print(date_one.week_of_month) # 1-based => 一个月的第几周 (此API v2.12版本有BUG(返回负数), v2.0.5)
        temp_list.append(date_one.quarter)       # 季 (无API,默认取属性)

        # 是否是工作日
            # or前面: 若在节假日历程内, 则一定是节假日期(但~放不放假不知...), or后面是星期几都无所谓, 进而返回 0           (表示"节假日")
            # or后面: 若不在节假日历程内, 再判断 or后面是星期几, 若属于 星期6和星期日 其中一个 (也表示假期), 进而同样返回 0 (表示 "节假日")
            # 其余可能均为 工作日:  进而返回1  (表示"工作日")
        temp_list.append(self.is_workday(date_one))

        # 标注节日, 是否是节日 (若有则标注 "节日名(eg:春节) =>可通过字典枚举", 若无则返回 "\N" => 与Hive的空值保持一致)
        reverse_dict = self.get_holiday_reverse_index()
        temp_list.append(reverse_dict.get(str(date_one), "\\N"))
        content = sep.join( map(str, temp_list) )
        return content
        
    def make_to_file(self, filename, sep="\t", head=False) -> None:
        csv_rows_str = "\n".join( [self.make_date_csv_str(per_date, sep=sep) for per_date in self.day_list()] )
        if head:
            head_list = ["Date","Year","Month","Day","Week", "WeekOfYear","Quarter","IsWeekDay","Holiday"]
            csv_rows_str = sep.join(head_list) + "\n" + csv_rows_str

        file_path = Path(filename).resolve()
        file_path.write_text(csv_rows_str, encoding="utf-8")
        print(f"Complete to write into: {file_path}")
