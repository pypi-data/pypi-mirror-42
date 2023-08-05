# coding=utf8
import re
import datetime

from typing import Optional, Iterator, Tuple, Union

__all__ = ['LunarDate', 'LCalendars']

# Typing

Leap = Union[int, bool]

#  Constants

MIN_LUNAR_YEAR = 1900
MAX_LUNAR_YEAR = 2100

_START_SOLAR_DATE = datetime.date(1900, 1, 31)
_END_SOLAR_DATE = datetime.date(2101, 1, 28)

MAX_OFFSET = (_END_SOLAR_DATE - _START_SOLAR_DATE).days  # 73411 [0, 73411]


def _check_year_range(year):
    if year < MIN_LUNAR_YEAR or year > MAX_LUNAR_YEAR:
        raise ValueError('year out of range [1900, 2100]')


YEAR_INFOS = [
    0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,  # 1900 - 1909
    0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,  # 1910 - 1919
    0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,  # 1920 - 1929
    0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,  # 1930 - 1939
    0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,  # 1940 - 1949
    0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,  # 1950 - 1959
    0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,  # 1960 - 1969
    0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,  # 1970 - 1979
    0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,  # 1980 - 1989
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,  # 1990 - 1999
    0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,  # 2000 - 2009
    0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,  # 2010 - 2019
    0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,  # 2020 - 2029
    0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,  # 2030 - 2039
    0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,  # 2040 - 2049
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,  # 2050 - 2059
    0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,  # 2060 - 2069
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,  # 2070 - 2079
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,  # 2080 - 2089
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,  # 2090 - 2099
    0x0d520
]


def parse_year_days(year_info):
    """Parse year days from a year info.
    """
    year_info = int(year_info)
    res = 29 * 12

    leap = False
    if year_info % 16 != 0:
        leap = True
        res += 29

    year_info //= 16

    for i in range(12 + leap):
        if year_info % 2 == 1:
            res += 1
        year_info //= 2
    return res


YEAR_DAYS = [parse_year_days(x) for x in YEAR_INFOS]


def _iter_year_month(year_info):
    """ Iter the month days in a lunar year.
    """
    # info => month, days, leap
    months = [(i, 0) for i in range(1, 13)]
    leap_month = year_info % 16  # The leap month in this year.
    if leap_month == 0:
        pass
    elif leap_month <= 12:
        months.insert(leap_month, (leap_month, 1))
    else:
        raise ValueError("yearInfo 0x{0:x} mod 16 should in [0, 12]".format(year_info))

    for month, leap in months:
        if leap:
            days = (year_info >> 16) % 2 + 29
        else:
            days = (year_info >> (16 - month)) % 2 + 29
        yield month, days, leap


class LCalendars:
    """A public API for lunar calendar.
    """

    @staticmethod
    def is_leap_month(year: int, month: int) -> bool:
        _check_year_range(year)
        return YEAR_INFOS[year - MIN_LUNAR_YEAR] % 16 == month

    @staticmethod
    def iter_year_month(year: int) -> Iterator[Tuple[int, int, int]]:
        _check_year_range(year)
        return _iter_year_month(YEAR_INFOS[year - MIN_LUNAR_YEAR])

    @staticmethod
    def ndays(year: int, month: Optional[int] = None, leap: Leap = False) -> int:
        _check_year_range(year)
        if month is None:
            return YEAR_DAYS[year - MIN_LUNAR_YEAR]
        leap = int(bool(leap))
        for _month, _days, _leap in LCalendars.iter_year_month(year):
            if (_month, _leap) == (month, leap):
                return _days
        else:
            raise ValueError('Invalid month for the year {}'.format(year))

    @staticmethod
    def create_solar_date(year: int, term_index: Optional[int] = None,
                          term_name: Optional[str] = None) -> datetime.date:
        if term_name:
            term_index = TERMS_CN.index(term_name)
        _check_year_range(year)
        if term_index % 2 == 0:
            month = term_index // 2 + 1
        else:
            month = (term_index + 1) // 2
        days = TermUtils.parse_term_days(year)
        day = days[term_index]
        return datetime.date(year, month, day)


# offset <----> year, day_offset <----> year, month, day, leap

def offset2ymdl(offset):
    def _o2mdl(_year_info, _offset):
        for _month, _days, _leap in _iter_year_month(_year_info):
            if _offset < _days:
                break
            _offset -= _days
        else:
            raise ValueError('Out of range.')
        return _month, _offset + 1, _leap

    offset = int(offset)

    for idx, year_day in enumerate(YEAR_DAYS):
        if offset < year_day:
            break
        offset -= year_day
    else:
        raise ValueError('Out of range')
    year = MIN_LUNAR_YEAR + idx

    year_info = YEAR_INFOS[idx]
    month, day, leap = _o2mdl(year_info, offset)
    return year, month, day, leap


def ymdl2offset(year, month, day, leap):
    def _mdl2o(_year_info, _month, _day, _leap):
        _leap = int(_leap)
        res = 0
        for _month_, _days_, _leap_ in _iter_year_month(_year_info):
            if (_month_, _leap_) == (_month, _leap):
                if 1 <= _day <= _days_:
                    res += _day - 1
                    return res
                else:
                    raise ValueError("day out of range")
            res += _days_

        raise ValueError("month out of range")

    offset = 0
    _check_year_range(year)
    year_idx = year - MIN_LUNAR_YEAR
    for i in range(year_idx):
        offset += YEAR_DAYS[i]
    offset += _mdl2o(YEAR_INFOS[year_idx], month, day, leap)
    return offset


# ------ Term Info ------

TERMS_CN = [
    "小寒", "大寒", "立春", "雨水", "惊蛰", "春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至",
    "小暑", "大暑", "立秋", "处暑", "白露", "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至"
]

TERM_INFO = [
    '654466556667788888998877', '664466566767888989998887', '665466666777898989998888', '665577667777899999998888',
    '765566556667788888998877', '664466566767888989998887', '665466666767898989998888', '665577667777899999998888',
    '765566556667788888998877', '664466566767888989998887', '665466666767898989998888', '665577667777899999998888',
    '765566556667788888998877', '654466566767888989998887', '664466566767898989998888', '665567666777898999998888',
    '665566556667788888898777', '654466566667888988998877', '664466566767898989998887', '665567666777898999998888',
    '665566556667788888898777', '654466556667888988998877', '664466566767898989998887', '665466666777898999998888',
    '665566556667788888898777', '654466556667888988998877', '664466566767888989998887', '665466666777898989998888',
    '665566556666788888887777', '654466556667788888998877', '664466566767888989998887', '665466666777898989998888',
    '665566556666788888887777', '654466556667788888998877', '664466566767888989998887', '665466666767898989998888',
    '665566556666788888887777', '654466556667788888998877', '664466566767888989998887', '665466666767898989998888',
    '665566556666788888887777', '654466556667788888998877', '664466566767888989998887', '665466666767898989998888',
    '665566555666788888887777', '654466556667788888898777', '654466566767888988998887', '664466566767898989998888',
    '665556555666787888887777', '554466556667788888898777', '654466556667888988998887', '664466566767898989998888',
    '665556555666787888887777', '554466556667788888898777', '654466556667888988998877', '664466566767888989998887',
    '665555555666787888887777', '554466556667788888898777', '654466556667788888998877', '664466566767888989998887',
    '665455555666787878887777', '554466556666788888887777', '654466556667788888998877', '664466566767888989998887',
    '665455555666787878887777', '554466556666788888887777', '654466556667788888998877', '664466566767888989998887',
    '665455555656787878887777', '554466556666788888887777', '654466556667788888998877', '664466566767888989998887',
    '665455555656787878887777', '554466555666788888887777', '654466556667788888998877', '664466566767888988998887',
    '665455455656787878887777', '554466555666787888887777', '654466556667788888898877', '664466566667888988998887',
    '665455455656787878887777', '554466555666787888887777', '654466556667788888898777', '654466556667888988998887',
    '664455455656777878887777', '554456555666787888887777', '554466556667788888898777', '654466556667788988998877',
    '664455455656777878887776', '554455555666787878887777', '554466556666788888898777', '654466556667788888998877',
    '664455455656777878887776', '554355555666787878887777', '554466556666788888887777', '654466556667788888998877',
    '664455455656777878887776', '554355555656787878887777', '554466556666788888887777', '654466556667788888998877',
    '664455455656777878887776', '554355555656787878887777', '554466556666788888887777', '654466556667788888998877',
    '664455455656777878887776', '554355555656787878887777', '554466555666787888887777', '654466556667788888998877',
    '664455455656777877887776', '554355455656787878887777', '554466555666787888887777', '654466556667788888898877',
    '664455455556777877887776', '554355455656777878887777', '554466555666787888887777', '654466556667788888898777',
    '654455445556777877887776', '553355455656777878887777', '554456555666787888887777', '554466556666788888898777',
    '654455445556677777887776', '553355455656777878887776', '554455555666787878887777', '554466556666788888898777',
    '654455445556677777887766', '553355455656777878887776', '554355555656787878887777', '554466556666788888887777',
    '654455445556677777887766', '553355455656777878887776', '554355555656787878887777', '554466556666788888887777',
    '654455445556677777887766', '553355455656777878887776', '554355555656787878887777', '554466555666787888887777',
    '654455445556677777887766', '553355455656777878887776', '554355555656787878887777', '554466555666787888887777',
    '654455445556677777887766', '553355455556777877887776', '554355455656787878887777', '554466555666787888887777',
    '654455445556677777787766', '553355445556777877887776', '554355455656777878887777', '554466555666787888887777',
    '654455445555677777787666', '543355445556677777887776', '553355455656777878887777', '554455555666787878887777',
    '554455445555677777787666', '543355445556677777887776', '553355455656777878887777', '554455555656787878887777',
    '554455445555677777787666', '543355445556677777887766', '553355455656777878887776', '554455555656787878887777',
    '554455445555677777776666', '543355445556677777887766', '553355455656777878887776', '554355555656787878887777',
    '554455445555677777776666', '543355445556677777887766', '553355455656777878887776', '554355555656787878887777',
    '554455444555676777776666', '543355445556677777887766', '553355455556777877887776', '554355555656787878887777',
    '554455444555676777776666', '543355445556677777787766', '553355455556777877887776', '554355455656777878887777',
    '554455444555676777776666', '543355445556677777787766', '553355445556677877887776', '554355455656777878887777',
    '554455444555676777776666', '543355445555677777787666', '553355445556677777887776', '553355455656777878887777',
    '554444444555676767776666', '443355445555677777787666', '543355445556677777887776', '553355455656777878887777',
    '554444444545676767776666', '443355445555677777787666', '543355445556677777887766', '553355455656777878887776',
    '554444444545676767776666', '443355445555677777776666', '543355445556677777887766', '553355455656777878887776',
    '554344444545676767776666', '443355445555676777776666', '543355445556677777887766', '553355455656777878887776',
    '554355555656787878887777'
]


class TermUtils:
    @staticmethod
    def parse_term_days(year):
        value_offset = [0, 15]
        year_index = year - 1900
        days = [int(c) + value_offset[i % 2] for i, c in enumerate(TERM_INFO[year_index])]
        return days

    @staticmethod
    def get_term_info(year, month, day):
        """Parse solar term and stem-branch year/month/day from a solar date.
        (sy, sm, sd) => (term, next_gz_month)
        """
        days = TermUtils.parse_term_days(year)
        term_index1 = 2 * (month - 1)
        term_index2 = 2 * (month - 1) + 1
        day1 = days[term_index1]
        day2 = days[term_index2]
        if day == day1:
            term_name = TERMS_CN[term_index1]
        elif day == day2:
            term_name = TERMS_CN[term_index2]
        else:
            term_name = None

        next_gz_month = day >= day1
        return term_name, next_gz_month


# ------ Stems and Branches ------


class TextUtils:
    MONTHS_CN = '〇正二三四五六七八九十冬腊'
    TENS = '初十廿卅'
    DAYS_CN = '日一二三四五六七八九十'

    STEMS = '甲乙丙丁戊己庚辛壬癸'
    BRANCHES = '子丑寅卯辰巳午未申酉戌亥'
    ANIMALS = '鼠牛虎兔龙蛇马羊猴鸡狗猪'

    @staticmethod
    def year_cn(year: int) -> str:
        s = ''.join([TextUtils.MONTHS_CN[int(c)] for c in str(year)])
        return s.replace('正', '一')

    @staticmethod
    def month_cn(month: int) -> str:
        return TextUtils.MONTHS_CN[month]

    @staticmethod
    def day_cn(day: int) -> str:
        a, b = divmod(day, 10)
        if b == 0:  # 10,20,30
            b = 10
            if a == 1:  # 10
                a = 0
        return TextUtils.TENS[a] + TextUtils.DAYS_CN[b]

    @staticmethod
    def get_gz_cn(offset: int) -> str:
        """Get n-th(0-based) GanZhi
        """
        return TextUtils.STEMS[offset % 10] + TextUtils.BRANCHES[offset % 12]


class LunarDate:
    __slots__ = [
        '_year', '_month', '_day', '_leap',
        '_offset', '_solar_ymd', '_term',
        '_gz_year', '_gz_month', '_gz_day',
        '_animal'
    ]

    def __new__(cls, year: int, month: int, day: int, leap: Leap = False):
        self = object.__new__(cls)
        offset = ymdl2offset(year, month, day, leap)
        self._year = year
        self._month = month
        self._day = day
        self._leap = leap
        self._offset = offset

        solar_date = _START_SOLAR_DATE + datetime.timedelta(days=self._offset)
        self._solar_ymd = solar_date.year, solar_date.month, solar_date.day
        self._gz_year, self._gz_month, self._gz_day, self._term = self._get_gz_ymd()
        return self

    @property
    def year(self) -> int:
        return self._year

    @property
    def month(self) -> int:
        return self._month

    @property
    def day(self) -> int:
        return self._day

    @property
    def leap(self) -> bool:
        return self._leap

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def term(self) -> str:
        return self._term

    @property
    def gz_year(self) -> str:
        return self._gz_year

    @property
    def gz_month(self) -> str:
        return self._gz_month

    @property
    def gz_day(self) -> str:
        return self._gz_day

    @property
    def animal(self) -> str:
        return TextUtils.ANIMALS[(self.year - 4) % 12]

    def _get_gz_ymd(self):
        """
        (sy, sm, sd) -> term / gz_year / gz_month / gz_day
        """
        sy, sm, sd = self._solar_ymd
        # [2101.1.1-2100.1.28] has no term info.
        if sy < 1900 or sy > 2100:
            return None, None, None, None
        term_name, next_gz_month = TermUtils.get_term_info(sy, sm, sd)
        s_offset = (datetime.date(sy, sm, sd) - _START_SOLAR_DATE).days
        gz_year = TextUtils.STEMS[(self.year - 4) % 10] + TextUtils.BRANCHES[(self.year - 4) % 12]
        if next_gz_month:
            gz_month = TextUtils.get_gz_cn((sy - 1900) * 12 + sm + 12)
        else:
            gz_month = TextUtils.get_gz_cn((sy - 1900) * 12 + sm + 11)
        gz_day = TextUtils.get_gz_cn((s_offset + 40) % 60)
        return gz_year, gz_month, gz_day, term_name

    @property
    def cn_year(self) -> str:
        return '{}年'.format(TextUtils.year_cn(self.year))

    @property
    def cn_month(self) -> str:
        return '{}{}月'.format('闰' if self.leap else '', TextUtils.month_cn(self.month))

    @property
    def cn_day(self) -> str:
        return '{}'.format(TextUtils.day_cn(self.day))

    def cn_str(self) -> str:
        return '{}{}{}'.format(self.cn_year, self.cn_month, self.cn_day)

    def gz_str(self) -> str:
        return '{}年{}月{}日'.format(self.gz_year, self.gz_month, self.gz_day)

    def to_solar_date(self) -> datetime.date:
        return _START_SOLAR_DATE + datetime.timedelta(days=self.offset)

    def before(self, day_delta: int = 1) -> 'LunarDate':
        y, m, d, leap = offset2ymdl(self._offset - day_delta)
        return LunarDate(y, m, d, leap)

    def after(self, day_delta: int = 1) -> 'LunarDate':
        y, m, d, leap = offset2ymdl(self._offset + day_delta)
        return LunarDate(y, m, d, leap)

    def replace(self, *, year: Optional[int] = None, month: Optional[int] = None, day: Optional[int] = None,
                leap: Optional[Leap] = None):
        if year is None:
            year = self._year
        if month is None:
            month = self._month
        if day is None:
            day = self._day
        if leap is None:
            leap = self._leap
        return type(self)(year, month, day, leap)

    def strftime(self, fmt: str) -> str:
        return Formatter(fmt).format(self)

    def __format__(self, fmt):
        if not isinstance(fmt, str):
            raise TypeError("must be str, not %s" % type(fmt).__name__)
        if len(fmt) != 0:
            return self.strftime(fmt)
        return str(self)

    @classmethod
    def from_solar_date(cls, year: int, month: int, day: int) -> 'LunarDate':
        solar_date = datetime.date(year, month, day)
        return cls.from_solar(solar_date)

    @classmethod
    def from_solar(cls, date_obj: datetime.date) -> 'LunarDate':
        offset = (date_obj - _START_SOLAR_DATE).days
        y, m, d, leap = offset2ymdl(offset)
        return cls(y, m, d, leap)

    @classmethod
    def today(cls) -> 'LunarDate':
        res = datetime.date.today()
        return cls.from_solar_date(res.year, res.month, res.day)

    @classmethod
    def yesterday(cls) -> 'LunarDate':
        sd = datetime.date.today() - datetime.timedelta(days=1)
        return cls.from_solar_date(sd.year, sd.month, sd.day)

    @classmethod
    def tomorrow(cls) -> 'LunarDate':
        sd = datetime.date.today() + datetime.timedelta(days=1)
        return cls.from_solar_date(sd.year, sd.month, sd.day)

    def __str__(self):
        return 'LunarDate(%d, %d, %d, %d)' % (self.year, self.month, self.day, self.leap)

    __repr__ = __str__

    def __sub__(self, other):
        if isinstance(other, LunarDate):
            return self.to_solar_date() - other.to_solar_date()
        elif isinstance(other, datetime.date):
            return self.to_solar_date() - other
        elif isinstance(other, datetime.timedelta):
            res = self.to_solar_date() - other
            return LunarDate.from_solar_date(res.year, res.month, res.day)
        raise TypeError

    def __rsub__(self, other):
        if isinstance(other, datetime.date):
            return other - self.to_solar_date()

    def __add__(self, other):
        if isinstance(other, datetime.timedelta):
            res = self.to_solar_date() + other
            return LunarDate.from_solar_date(res.year, res.month, res.day)
        raise TypeError

    def __radd__(self, other):
        return self + other

    def __eq__(self, other):
        if not isinstance(other, LunarDate):
            return False

        return self - other == datetime.timedelta(0)

    def __lt__(self, other):
        try:
            return self - other < datetime.timedelta(0)
        except TypeError:
            raise TypeError("can't compare LunarDate to %s" % (type(other).__name__,))

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other

    def __hash__(self):
        return hash((self.year, self.month, self.day, self.leap))


LunarDate.min = LunarDate(1990, 1, 1, False)
LunarDate.max = LunarDate(2100, 12, 29, False)


class Formatter:
    """A formatter based on %-fmt .
    """
    directives = {
        '%y': 'year',
        '%Y': 'cn_year',
        '%m': 'month',
        '%A': 'padding_month',
        '%l': 'leap',
        '%L': 'cn_leap',
        '%M': 'cn_month',
        '%d': 'day',
        '%B': 'padding_day',
        '%D': 'cn_day',
        '%a': 'animal',
        '%t': 'term',
        '%0': 'gz_year',
        '%p': 'gz_month',
        '%q': 'gz_day',
        '%C': 'cn_str',
        '%G': 'gz_str',
        '%%': '%'
    }

    def __init__(self, fmt: str):
        self._fields = set({})
        pattern = re.compile('|'.join(self.directives.keys()))
        self._fmt = pattern.sub(self.replace_rex, fmt)

    def replace_rex(self, match):
        directive = match.group()
        if directive == '%%':
            return '%'
        field = self.directives[directive]
        self._fields.add(field)
        return ''.join(['{', field, '}'])

    def format(self, obj: LunarDate) -> str:
        values = {f: self.resolve(obj, f) for f in self._fields}
        return self._fmt.format(**values)

    def resolve(self, obj, field):
        try:
            func = getattr(self, 'get_' + field)
            return func(obj)
        except AttributeError:
            attr = getattr(obj, field)
            if callable(attr):
                return attr()
            else:
                return attr

    # Custom values

    def get_leap(self, obj):
        return int(obj.leap)

    def get_cn_leap(self, obj):
        if obj.leap:
            return '闰'
        else:
            return ''

    def get_cn_year(self, obj):
        return TextUtils.year_cn(obj.year)

    def get_cn_month(self, obj):
        return TextUtils.month_cn(obj.month)

    def get_cn_day(self, obj):
        return TextUtils.day_cn(obj.day)

    def get_padding_month(self, obj):
        return '{0:02d}'.format(obj.month)

    def get_padding_day(self, obj):
        return '{0:02d}'.format(obj.day)
