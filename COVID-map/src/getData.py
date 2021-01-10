import numpy as np
import pandas as pd
import os
import datetime
from pandas.testing import assert_frame_equal

DATA_PATH = '/src/data/COVID_ALL.csv'

CHINA_PROVINCES = pd.Series([
    '湖北',
    '广东',
    '北京',
    '上海',
    '浙江',
    '天津',
    '重庆',
    '江西',
    '山东',
    '河南',
    '湖南',
    '四川',
    '云南',
    '山西',
    '福建',
    '辽宁',
    '海南',
    '安徽',
    '贵州',
    '广西',
    '宁夏',
    '河北',
    '江苏',
    '吉林',
    '黑龙江',
    '陕西',
    '新疆',
    '甘肃',
    '内蒙古',
    '青海',
    '西藏',
    '台湾',
    '香港'])

INNER_MONGOLIA = '内蒙古自治区'
HEILONGJIANG = '黑龙江省'

CHINA = '中国'

BASE_DATA = None

COUNTRY = 'country'
CITY = 'city'
DATE = 'date'
PROVINCE = 'province'
CURED = 'cured'
CONFIRMED = 'confirmed'
DEAD = 'dead'

NAN_STR = 'NaN'


def __update_data():
    # 从数据源处获得原始数据
    pass


def __get_provinces_base_data():
    # 列名为['报道时间', '省份', '治愈', '新增', '死亡']
    global BASE_DATA
    if (not isinstance(BASE_DATA, pd.DataFrame)):
        Country = 'Country/Region'
        Province = 'Province/State'
        China = 'Mainland China'
        Hong_Kong = 'Hong Kong'
        Taiwan = 'Taiwan'
        Macau = 'Macau'
        Date = 'Last Update'
        Recovered = 'Recovered'
        Confirmed = 'Confirmed'
        Deaths = 'Deaths'

        Province_Map = {'Anhui': '安徽',
                        'Beijing': '北京',
                        'Chongqing': '重庆',
                        'Fujian': '福建',
                        'Gansu': '甘肃',
                        'Guangdong': '广东',
                        'Guangxi': '广西',
                        'Guizhou': '贵州',
                        'Hainan': '海南',
                        'Hebei': '河北',
                        'Heilongjiang': '黑龙江',
                        'Henan': '河南',
                        'Hong Kong': '香港',
                        'Hubei': '湖北',
                        'Hunan': '湖南',
                        'Inner Mongolia': '内蒙古',
                        'Jiangsu': '江苏',
                        'Jiangxi': '江西',
                        'Jilin': '吉林',
                        'Liaoning': '辽宁',
                        'Macau': '澳门',
                        'Ningxia': '宁夏',
                        'Qinghai': '青海',
                        'Shaanxi': '陕西',
                        'Shandong': '山东',
                        'Shanghai': '上海',
                        'Shanxi': '山西',
                        'Sichuan': '四川',
                        'Taiwan': '台湾',
                        'Tianjin': '天津',
                        'Tibet': '西藏',
                        'Xinjiang': '新疆',
                        'Yunnan': '云南',
                        'Zhejiang': '浙江',
                        }

        Data_dir = '/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'

        date = datetime.date(2020, 1, 22)

        df = pd.DataFrame(
            {DATE: {}, PROVINCE: {}, CURED: {}, CONFIRMED: {}, DEAD: {}})
        df = pd.DataFrame()
        while date < datetime.date.today()+datetime.timedelta(days=1):
            Data_path = os.getcwd() + Data_dir + date.strftime('%m-%d-%Y') + '.csv'
            print('cope with data comes from '+Data_path)
            if not os.path.exists(Data_path):
                print(
                    '请通过\n  \'cd COVID-19/\'\n  \'git pull https://github.com/CSSEGISandData/COVID-19.git\'\n更新数据!')
                break
            if (date == datetime.date(2020, 3, 22)):
                Country = 'Country_Region'
                Province = 'Province_State'
                Date = 'Last_Update'
            if (date == datetime.date(2020, 3, 11)):
                China = 'China'
            d = pd.read_csv(Data_path)
            d = d[d[Country].isin(
                [China, Hong_Kong, Taiwan, Macau])]
            d = d.loc[:, [Date, Province, Recovered, Confirmed, Deaths]]
            d = d.fillna(value=0.0)
            for key in Province_Map.keys():
                d.loc[d[Province] == key, Province] = Province_Map[key]
            d = d.rename(columns={Date: DATE, Province: PROVINCE,
                                  Recovered: CURED, Confirmed: CONFIRMED, Deaths: DEAD})
            d[DATE] = date.strftime('%Y-%m-%d')
            d = d.set_index(PROVINCE)
            df = pd.concat([df, d])
            date = date + datetime.timedelta(days=1)
        df[[CURED, CONFIRMED, DEAD]] = df[[
            CURED, CONFIRMED, DEAD]].astype(float)
        BASE_DATA = df
    else:
        df = BASE_DATA
    return df


def __get_China_base_data():
    # 列名为['报道时间', '治愈', '新增', '死亡']
    df = __get_provinces_base_data()
    return df.groupby(DATE).sum()


def get_date_list():
    # ['日期', '日期', ...]
    df = __get_provinces_base_data()
    df = df.groupby(DATE).sum()

    data = [i for i in df.index]
    return data


def get_provinces_list():
    # ['北京', '上海', ]
    return [province for province in CHINA_PROVINCES]


def get_China_sum_data(column: str):
    # 中国累计治愈/确诊/死亡总人数
    df = __get_China_base_data()
    return [float(df.at[i, column]) for i in df.index]


def get_China_sick_daily_data():
    # 中国每日住院人数
    cured_data = get_China_sum_data(CURED)
    confirm_data = get_China_sum_data(CONFIRMED)
    dead_data = get_China_sum_data(DEAD)

    return [confirm_data[i] - cured_data[i] - dead_data[i]
            for i in range(len(cured_data))]


def get_provinces_sum_data(column: str):
    # 获取各省累计治愈/确诊/死亡人数
    df = __get_provinces_base_data()

    # df = df.loc[:, column]
    dates = get_date_list()
    provinces = get_provinces_list()

    df = [df.groupby(DATE).get_group(date) for date in dates]

    data = [{i: float(item.at[i, column])
             for i in item.index} for item in df]

    for item in data:
        for province in provinces:
            if province not in item:
                item[province] = 0.0

    return data


def get_provinces_sick_daily_data():
    # 各省每日住院人数
    cured_data = get_provinces_sum_data(CURED)
    confirm_data = get_provinces_sum_data(CONFIRMED)
    dead_data = get_provinces_sum_data(DEAD)
    provinces = get_provinces_list()

    sick_data = []
    sick_num = {province: 0.0 for province in provinces}
    for i in range(len(cured_data)):
        for province in provinces:
            sick_num[province] = confirm_data[i][province] - \
                cured_data[i][province] - dead_data[i][province]
        sick_data.append({key: sick_num[key] for key in sick_num.keys()})

    return sick_data
