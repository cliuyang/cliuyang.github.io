from typing import List

import pyecharts.options as opts
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode
from pyecharts.charts import Timeline, Grid, Bar, Map, Pie, Line, Tab
import getData
import time

date_list = []
simple_date_list = []
provinces_list = []

China_daily_sick_data = []

provinces_daily_sick_data = []

# 数据和的最值
maxNum = 50000
minNum = 0


def InitData():
    global date_list
    global simple_date_list
    global provinces_list

    global China_daily_sick_data

    global provinces_daily_sick_data

    date_list = getData.get_date_list()
    simple_date_list = [time.strftime(
        '%m-%d', time.strptime(d, '%Y-%m-%d')) for d in date_list]
    provinces_list = getData.get_provinces_list()

    China_daily_sick_data = getData.get_China_sick_daily_data()

    provinces_daily_sick_data = getData.get_provinces_sick_daily_data()


def get_provinces_daily_map_chart(date: str):
    date_index = date_list.index(date)

    date_data = provinces_daily_sick_data[date_index]

    map_data = [[key, date_data[key]] for key in date_data.keys()]

    map_chart = (
        Map()
        .add(
            series_name="",
            data_pair=map_data,
            zoom=0.85,
            center=[119.5, 34.5],
            is_map_symbol_show=False,
            itemstyle_opts={
                "normal": {"areaColor": "#323c48", "borderColor": "#404a59"},
                "emphasis": {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                },
            },
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=time.strftime('%Y年%m月%d日', time.strptime(
                    date, '%Y-%m-%d')) + '新型冠状病毒肺炎感染总人数',
                subtitle='制作：陈留阳\n数据源：CSSEGISandData\n(可适当放缩以观看全貌)',
                subtitle_link='https://github.com/CSSEGISandData/COVID-19',
                subtitle_target='blank',
                item_gap=20,
                pos_left="center",
                pos_top="top",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25,
                    color="rgba(255,255,255, 0.9)"
                ),
                subtitle_textstyle_opts=opts.TextStyleOpts(
                    font_size=15,
                    line_height=20
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """function(params) {
                    if ('value' in params.data) {
                        return params.data.value[2] + ': ' + params.data.value[0];
                    }
                }"""
                ),
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="30",
                pos_top="center",
                range_text=['感染人数'],
                is_piecewise=True,
                pieces=[
                    {'min': 10000},
                    {'min': 5000, 'max': 10000},
                    {'min': 1000, 'max': 5000},
                    {'min': 900, 'max': 1000},
                    {'min': 800, 'max': 900},
                    {'min': 700, 'max': 800},
                    {'min': 600, 'max': 700},
                    {'min': 500, 'max': 600},
                    {'min': 400, 'max': 500},
                    {'min': 300, 'max': 400},
                    {'min': 200, 'max': 300},
                    {'min': 100, 'max': 200},
                    {'min': 10, 'max': 100},
                    {'min': 1, 'max': 10},
                    {'max': 1}
                ],
                range_color=['#fde3a7', '#cf000f'],
                textstyle_opts=opts.TextStyleOpts(
                    color="#ddd"
                ),
                min_=minNum,
                max_=maxNum,
            ),
        )
    )

    return map_chart


def get_provinces_daily_pie_chart(date: str):
    date_index = date_list.index(date)

    date_data = provinces_daily_sick_data[date_index]

    pie_data = sorted([[key, date_data[key]] for key in date_data.keys()],
                      key=lambda item: item[1], reverse=True)

    pie_chart = (
        Pie()
        .add(
            series_name="",
            data_pair=pie_data,
            radius=["5%", "20%"],
            center=["80%", "80%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(
                # is_show=True,
                is_show=False,
                formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(
                is_show=False
            ),
        )
    )

    return pie_chart


def get_provinces_daily_bar_chart(date: str):
    date_index = date_list.index(date)

    date_data = provinces_daily_sick_data[date_index]

    bar_x_data = provinces_list
    bar_y_data = sorted([{'name': key, 'value': date_data[key]}
                         for key in date_data.keys()], key=lambda item: item['value'], reverse=True)

    bar_chart = (
        Bar()
        .add_xaxis(xaxis_data=bar_x_data)
        .add_yaxis(
            series_name="",
            yaxis_data=bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=True,
                position="right",
                formatter="{b} : {c}"
            ),
        )
        .reversal_axis()
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_='dataMax',
                axislabel_opts=opts.LabelOpts(
                    is_show=False
                )
            ),
            yaxis_opts=opts.AxisOpts(

                axislabel_opts=opts.LabelOpts(
                    is_show=False
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=False
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="top",
                range_text=['感染人数'],
                is_piecewise=True,
                pieces=[
                    {'min': 10000},
                    {'min': 5000, 'max': 10000},
                    {'min': 1000, 'max': 5000},
                    {'min': 900, 'max': 1000},
                    {'min': 800, 'max': 900},
                    {'min': 700, 'max': 800},
                    {'min': 600, 'max': 700},
                    {'min': 500, 'max': 600},
                    {'min': 400, 'max': 500},
                    {'min': 300, 'max': 400},
                    {'min': 200, 'max': 300},
                    {'min': 100, 'max': 200},
                    {'min': 10, 'max': 100},
                    {'min': 1, 'max': 10},
                    {'max': 1}
                ],
                range_color=['#fde3a7', '#cf000f'],
                textstyle_opts=opts.TextStyleOpts(
                    color="#ddd"
                ),
                min_=minNum,
                max_=maxNum,
            ),
        )
    )

    return bar_chart


def get_China_sum_line_chart(date: str):
    show_index = date_list.index(date) + 1

    line_chart = (
        Line()
        .add_xaxis(simple_date_list[:show_index])
        .add_yaxis(
            '',
            China_daily_sick_data
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                is_show=False
            )
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                pos_left="74%",
                pos_top="3%"
            )
        )
    )
    return line_chart


def get_date_chart(date: str):
    grid_chart = (
        Grid()
        .add(
            get_provinces_daily_bar_chart(date),
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
            ),
        )
        .add(
            get_China_sum_line_chart(date),
            grid_opts=opts.GridOpts(
                pos_left="65%", pos_right="80", pos_top="5%", pos_bottom="65%"
            ),
        )
        .add(
            get_provinces_daily_pie_chart(date),
            grid_opts=opts.GridOpts(
                pos_left="45%", pos_top="65%"
            )
        )
        .add(
            get_provinces_daily_map_chart(date),
            grid_opts=opts.GridOpts(
                pos_left='10'
            )
        )
    )

    return grid_chart


def get_whole_chart():
    timeline = Timeline(
        init_opts=opts.InitOpts(
            width="1600px", height="900px", theme=ThemeType.DARK,
            page_title='新冠肺炎疫情地图',)
    )
    for i in range(len(date_list)):

        g = get_date_chart(date=date_list[i])

        timeline.add(
            g,
            time_point=simple_date_list[i]
        )

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=2000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="70",
        label_opts=opts.LabelOpts(
            is_show=True,
            color="#fff"
        ),
    )

    return timeline


if __name__ == '__main__':
    InitData()

    chart = get_whole_chart()
    chart.render("COVID-map.html")
