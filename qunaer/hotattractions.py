import requests
from fake_useragent import UserAgent
import json
import pandas
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Map,Geo
from pyecharts.globals import ChartType, SymbolType


def get_hotattractions(query_params):
    '''
    获取热门景点门票数据
    '''
    url = 'https://piao.qunar.com/ticket/list.json'
    headers = {
        'UserAgent': UserAgent().random
    }
    params = query_params

    try:
        response = requests.get(url,headers=headers,params=params)
    except:
        return 'requests error'

    data = json.loads(response.text)
    sightlist = data['data']['sightList']

    sightName = []
    districts = []
    qunarPrice = []
    star = []
    saleCount = []
    totalsale = []

    for i in sightlist:
        try:
            star.append(i['star'])
        except KeyError:
            star.append('无星级')
        sightName.append(i['sightName'])
        districts.append(i['districts'].split('·')[0])
        qunarPrice.append(i['qunarPrice'])
        saleCount.append(i['saleCount'])
        totalsale.append(float(i['qunarPrice'])*int(i['saleCount']))
    
    info = {}
    info['sightName'] = sightName
    info['districts'] = districts
    info['qunarPrice'] = qunarPrice
    info['star'] = star
    info['saleCount'] = saleCount
    info['totalsale'] = totalsale

    return info

def write_to_excel(filepath,satrtpage,endpage):
    '''
    filepath：xlsx文件路径
    startpage：开始爬取页数
    endpage：结束爬取页数
    调用get_hotattractions爬取数据
    写入数据到excel
    '''
    infos = {
        'sightName':[],
        'districts':[],
        'qunarPrice':[],
        'star':[],
        'saleCount':[],
        'totalsale':[]
    }
    for i in range(satrtpage,endpage):
        print(f'爬取第{i}页')
        query_params = {
            'keyword':'热门景点',
            'region':'',
            'from':'mpl_search_suggest',
            'page':i,
            'sort':'pp'
        }
        info = get_hotattractions(query_params)
        infos['sightName'] += info['sightName']
        infos['districts'] += info['districts']
        infos['qunarPrice'] += info['qunarPrice']
        infos['star'] += info['star']
        infos['saleCount'] += info['saleCount']
        infos['totalsale'] += info['totalsale']

    df1 = pandas.DataFrame(infos)
    writer = pandas.ExcelWriter(filepath)

    df1.to_excel(writer,'df1')
    writer.save()
    


def saleCount_and_totalPrice(filepath):
    '''
    门票、价格、销量
    柱状图
    '''
    sightName = pandas.read_excel(filepath,usecols =[1],username=None)
    sightNameList = sightName.values.tolist()
    namedata = []
    for i in sightNameList:
        namedata.append(i[0])

    saleCount = pandas.read_excel(filepath,usecols =[5],username=None)
    saleCountList = saleCount.values.tolist()
    saledata = []
    for i in saleCountList:
        saledata.append(i[0])

    totalPrice = pandas.read_excel(filepath,usecols=[6],username=None)
    totalPriceList = totalPrice.values.tolist()
    totaldata = []
    for i in totalPriceList:
        totaldata.append(int(i[0]))     

    price = pandas.read_excel(filepath,usecols =[3],username=None)  
    priceList = price.values.tolist()
    pricedata = []
    for i in priceList:
        pricedata.append(int(i[0]))

    print(namedata)
    print(saledata)
    print(totaldata)
    print(pricedata)

    bar = (
        Bar()
        .add_xaxis(namedata)
        .add_yaxis('销量',saledata)
        .add_yaxis('门票价*销量',totaldata)
        .add_yaxis('门票价',pricedata)
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position="right"))
        .set_global_opts(
                        title_opts=opts.TitleOpts(title="国庆冷门旅游景点top30"),
                        # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-90)),
                        # legend_opts = opts.LegendOpts(pos_left='60%'),                      
                        )
    )
    # return bar
    bar.render('国庆冷门旅游景点top30.html')


def mapchart(filepath):
    '''
    地域分布
    地图
    '''
    sightName = pandas.read_excel(filepath,usecols =[2],username=None)
    sightNameList = sightName.values.tolist()
    citydata = []
    city = {}
    for i in sightNameList:
        if i[0] in city:
            city[i[0]] += 1
        else:
            city[i[0]] = 1

    for item in city.items():
        citydata.append(item)

    print(citydata)
    

    c = (
        # Geo()
        Map()
        # .add_schema(maptype="china")
        .add("", citydata)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(is_piecewise=False,min_=0,max_=10),
            title_opts=opts.TitleOpts(title="冷门城市分布"),
            toolbox_opts = opts.ToolboxOpts(is_show=True),
            tooltip_opts = opts.TooltipOpts(is_show=True,trigger_on= None,)
        )
    )
    c.render('冷门城市分布.html')
    return c


if __name__ == "__main__":

    # filepath = r'C:\Users\Administrator\Desktop\Python-imitate-login\qunaer\down30.xlsx'
    # # satrtpage = 3939
    # # endpage = 3941
    # # write_to_excel(filepath,satrtpage,endpage)
    # saleCount_and_totalPrice(filepath)

    filepath = r'C:\Users\Administrator\Desktop\Python-imitate-login\qunaer\down30.xlsx'
    # satrtpage = 1
    # endpage = 3
    # write_to_excel(filepath,satrtpage,endpage)
    saleCount_and_totalPrice(filepath)
    # mapchart(filepath)