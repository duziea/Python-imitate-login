
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
import json


def get_district():
    file = open(r'lagou\pythonjobinfo.json', 'r', encoding='utf-8')
    district_list = json.load(file)
    print(len(district_list))
    district = {}
    for i in district_list:
        city = i['city']
        if city in district:
            district[city] += 1
        else:
            district[city] = 1

    print(district)

    return district


def export_bar(dic):
    keys = list(dic.keys())
    values = list(dic.values())
    print(keys)
    print(values)
    bar = (
        Bar()
        .add_xaxis(keys)
        .add_yaxis('city', values)
        .set_global_opts(title_opts=opts.TitleOpts(title=""))
    )
    bar.render()


def get_salary():
    file = open(r'lagou\pythonjobinfo.json', 'r', encoding='utf-8')
    data_list = json.load(file)
    print(len(data_list))
    salary_dic = {}
    for i in data_list:
        salary = i['salary']
        if salary in salary_dic:
            salary_dic[salary] += 1
        else:
            salary_dic[salary] = 1

    print(salary_dic)

    return salary_dic


def export_pie(dic):
    keys = list(dic.keys())
    values = list(dic.values())
    print(keys)
    print(values)
    pie = (
        Pie()
        .add(
            '',
            [list(z) for z in zip(keys, values)],
            radius=["40%", "75%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="java_salary"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="80%", orient="vertical"
            ),
        )
        # .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    pie.render()
    # return pie

def get_skill_label():
    file = open(r'lagou\pythonjobinfo.json', 'r', encoding='utf-8')
    data_list = json.load(file)
    print(len(data_list))
    skill_label = ''
    for i in data_list:
        skillLables = i["skillLables"]
        if skillLables != []:
            for skill in skillLables:
                skill_label += skill

    print(skill_label)

    return skill_label

        
if __name__ == "__main__":
    # d = get_district()
    # export_district_echart(d)

    d=get_salary()
    export_pie(d)

    # get_skill_label()
