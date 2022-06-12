from multiprocessing.dummy import Condition
import numpy as np  # 数组相关的库
import matplotlib.pyplot as plt  # 绘图库
import time
from pylab import mpl
from flask import Flask, request, jsonify
from flask_cors import *
import pymysql
from soupsieve import select


app = Flask(__name__)
CORS(app, supports_credentials=True)
# 设置字体
# mpl.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
# mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 总共的人数统计
sum_of_human = 2000
# 潜伏期 表示患者感染上病毒后多少天才患病
incubation_period = 40
# 诊疗意愿，患者发病后多少天去医院
treat_willingness = 40
# 总的患者数等于潜伏期人数加上发病人数
isolation_all_day = incubation_period+treat_willingness
# 可容纳的隔离数
isolation_pos = 400
# 感染范围
infection_area = 0.02
# 运动范围参数 0-1
move_area_param = 0.3
# 初始感染者
first_infected_cnt = 20

# ————————————————————————
# 个人感觉上面这些东西可以作为输入参数来进行交互
# ————————————————————————

# 生成画布，在输出的时候可以改成在Cesium上
'''
plt.figure(figsize=(18, 14), dpi=80)
plt.ion()
'''


def get_normal_list(mu=0.0, sigma=0.7, sampleNo=sum_of_human, seed=0):
    '''
    :param mu: 对称轴
    :param sigma: 方差
    :param sampleNo: 样点个数
    :return:
    '''
    if seed:
        np.random.seed(seed)
    else:
        np.random.seed(round(time.time() * 100000) % 10000)
    if sigma < 0:
        sigma = 0
    s = np.random.normal(mu, sigma, sampleNo)
    return s


'''
x1 = get_normal_list(seed=1, sampleNo=int(sum_of_human / 2))
x2 = get_normal_list(seed=2, sampleNo=int(sum_of_human / 2))
x = get_normal_list(seed=3, sampleNo=sum_of_human)
y1 = get_normal_list(seed=5, sampleNo=int(sum_of_human / 2))
y2 = get_normal_list(seed=6, sampleNo=int(sum_of_human / 2))

# 设置初始感染者。从这段代码上来看，初始感染者应该是随机设置的。我们可以改成自行设置，比如感染者的位置等等
np.random.seed(10)
first_infected_cnt_index = np.random.randint(
    0, sum_of_human, size=first_infected_cnt)
infected_index_set = set(first_infected_cnt_index)
infected_index_history = []
infected_index_history.append(infected_index_set)
# 初始化相关变量
isolation_set = set()
plt_x_isolation = np.array([])
plt_y_isolation = np.array([])
plt_x_sick = np.array([])
plt_y_sick = np.array([])

# 这是感染者的运动过程，在Cesium中可以输出为感染者的位置
move_mu = 0
move_sigma = 0.01*move_area_param
for day in range(1, 1000):
    # plt.cla()
    # plt.grid(False)
    # 人员运动
    move_x1 = get_normal_list(
        mu=move_mu, sigma=move_sigma, sampleNo=int(sum_of_human / 2))
    move_x2 = get_normal_list(
        mu=-move_mu, sigma=move_sigma, sampleNo=int(sum_of_human / 2))
    move_y1 = get_normal_list(
        mu=move_mu, sigma=move_sigma, sampleNo=int(sum_of_human / 2))
    move_y2 = get_normal_list(
        mu=-move_mu, sigma=move_sigma, sampleNo=int(sum_of_human / 2))
    x1 = x1 + move_x1
    x2 = x2 + move_x2
    y1 = y1 + move_y1
    y2 = y2 + move_y2

    plt_x = np.concatenate((x1, x2), axis=0)
    plt_y = np.concatenate((y1, y2), axis=0)

    set_infected_index_today = set()
    for infected_index in infected_index_set:
        infected_point = (plt_x[infected_index], plt_y[infected_index])
        infected_array_index_today = np.where(
            (plt_x > infected_point[0] - infection_area) & (plt_x <
                                                            infected_point[0] + infection_area)
            & (plt_y > infected_point[1] - infection_area) & (plt_y < infected_point[1] + infection_area))
        infected_array_index_today = infected_array_index_today[0]
        set_infected_index_today = set_infected_index_today | set(
            infected_array_index_today)

    # 记录当天之后感染的所有人 set 和历史感染set的统计集合list
    infected_index_set = infected_index_set | set_infected_index_today
    infected_index_history.append(infected_index_set)

    # 已经在潜伏期的人数
    plt_x_infection = plt_x[list(infected_index_set)]
    plt_y_infection = plt_y[list(infected_index_set)]

    # 已出现病症的人数
    if day >= incubation_period:
        plt_x_sick = plt_x[list(infected_index_history[day-incubation_period])]
        plt_y_sick = plt_y[list(
            infected_index_history[day - incubation_period])]

    # 隔离人数
    if day >= isolation_all_day:

        if len(isolation_set) < isolation_pos:
            # print(len(isolation_set))
            isolation_set = isolation_set | infected_index_history[day -
                                                                   isolation_all_day]
        infected_index_set = infected_index_set-isolation_set
        plt_x_isolation = plt_x[list(isolation_set)]
        plt_y_isolation = plt_y[list(isolation_set)]

    # ——————————————————————————————————————————————————————
    # 上面这些内容是算法。但是，这些人数也可以作为数据显示在前端。我看matplotlib里面并没有数据。
    # 个人感觉下面这些内容可以用来输出。wyc用的是在matplotlib上进行输出，我们的大作业可以改成在Cesium上进行输出
    # 输出的经纬度范围可以通过输入来进行预设
    # ——————————————————————————————————————————————————————
    # 设置坐标轴范围 关闭坐标轴显示

    plt.xlim((-2, 2))
    plt.ylim((-2, 2))
    plt.axis('off')
    # 正常人
    plt.scatter(plt_x, plt_y, alpha=0.7, marker='.',label='normal') 

    # 潜伏期人
    plt.scatter(plt_x_infection, plt_y_infection, c='yellow',alpha=0.7, marker='.',label='incubation period')
    # 患病人
    if day >= incubation_period:
        plt.scatter(plt_x_sick, plt_y_sick, c='red', alpha=0.8, marker='.',label='sick')
    # 隔离人
    if day >= isolation_all_day:
        plt.scatter(plt_x_isolation, plt_y_isolation, c='white', marker='.')

    plt.legend(loc='upper right')
    plt.pause(0.0001)
    '''


def getPosition(x, y, w, e, n, s):  # 将算法求得的坐标映射到指定经纬度范围
    if len(x) == 0:
        return x, y
    minx = np.min(x)
    miny = np.min(y)
    maxx = np.max(x)
    maxy = np.max(y)
    x = x - minx
    y = y - miny
    x = (float(e) - float(w)) / (maxx - minx) * x + float(w)
    y = (float(n) - float(s)) / (maxy - miny) * y + float(s)
    return x, y


@app.route('/injection', methods=['GET', 'POST'])
def injection():
    request_method = request.method
    if request_method == 'POST':
        # 初始化算法
        condition = request.get_json()
        sum_of_human = int(condition["sum_of_human"])
        day = int(condition["day"])
        if day == 0:
            x1 = get_normal_list(seed=1, sampleNo=int(sum_of_human / 2))
            x2 = get_normal_list(seed=2, sampleNo=int(sum_of_human / 2))
            y1 = get_normal_list(seed=5, sampleNo=int(sum_of_human / 2))
            y2 = get_normal_list(seed=6, sampleNo=int(sum_of_human / 2))
        else:
            x1 = condition["x1"]
            x2 = condition["x2"]
            y1 = condition["y1"]
            y2 = condition["y2"]
        incubation_period = int(condition["incubation_period"])
        treat_willingness = int(condition["treat_willingness"])
        isolation_all_day = incubation_period+treat_willingness
        isolation_pos = int(condition["isolation_pos"])
        infection_area = float(condition["infection_area"])
        move_area_param = float(condition["move_area_param"])
        first_infected_cnt = int(condition["first_infected_cnt"])
        infected_index_history = condition["infected_index_history"]
        west = condition["west"]
        east = condition["east"]
        north = condition["north"]
        south = condition["south"]

        # 设置初始感染者。从这段代码上来看，初始感染者应该是随机设置的。我们可以改成自行设置，比如感染者的位置等等
        np.random.seed(10)
        if day==0:
            first_infected_cnt_index = np.random.randint(
                0, sum_of_human, size=first_infected_cnt)
            infected_index_set = set(first_infected_cnt_index)
        else:
            infected_index_set = condition["infected_index_set"]
        if day == 0:
            infected_index_history = []
            infected_index_history.append(
                np.array(list(infected_index_set)).astype(dtype=int).tolist())
        # 初始化相关变量
        if day==0:
            isolation_set = set()
        else:
            isolation_set = condition["isolation_set"]

        plt_x_isolation = np.array([])
        plt_y_isolation = np.array([])
        plt_x_sick = np.array([])
        plt_y_sick = np.array([])
        move_mu = 0
        move_sigma = 0.01*move_area_param

        # 执行一天的感染
        move_x1 = get_normal_list(
            mu=move_mu, sigma=move_sigma, sampleNo=int(sum_of_human / 2))
        move_x2 = get_normal_list(
            mu=-move_mu, sigma=move_sigma, sampleNo=int(sum_of_human / 2))
        move_y1 = get_normal_list(
            mu=move_mu, sigma=move_sigma, sampleNo=int(sum_of_human / 2))
        move_y2 = get_normal_list(
            mu=-move_mu, sigma=move_sigma, sampleNo=int(sum_of_human / 2))
        x1 = x1 + move_x1
        x2 = x2 + move_x2
        y1 = y1 + move_y1
        y2 = y2 + move_y2

        plt_x = np.concatenate((x1, x2), axis=0)
        plt_y = np.concatenate((y1, y2), axis=0)

        set_infected_index_today = set()
        for infected_index in infected_index_set:
            infected_point = (plt_x[infected_index], plt_y[infected_index])
            infected_array_index_today = np.where(
                (plt_x > infected_point[0] - infection_area) & (plt_x <
                                                                infected_point[0] + infection_area)
                & (plt_y > infected_point[1] - infection_area) & (plt_y < infected_point[1] + infection_area))
            infected_array_index_today = infected_array_index_today[0]
            set_infected_index_today = set_infected_index_today | set(
                infected_array_index_today)

        # 记录当天之后感染的所有人 set 和历史感染set的统计集合list
        infected_index_set = set(infected_index_set) | set_infected_index_today
        infected_index_history.append(
            np.array(list(infected_index_set)).astype(dtype=int).tolist())

        # 已经在潜伏期的人数
        plt_x_infection = plt_x[list(infected_index_set)]
        plt_y_infection = plt_y[list(infected_index_set)]

        # 已出现病症的人数
        if day >= incubation_period:
            plt_x_sick = plt_x[list(
                infected_index_history[day-incubation_period])]
            plt_y_sick = plt_y[list(
                infected_index_history[day - incubation_period])]

        # 隔离人数
        if day >= isolation_all_day:

            if len(isolation_set) < isolation_pos:
                # print(len(isolation_set))
                isolation_set = set(isolation_set) | set(infected_index_history[day -
                                                                           isolation_all_day])
            infected_index_set = set(infected_index_set)-set(isolation_set)
            plt_x_isolation = plt_x[list(isolation_set)]
            plt_y_isolation = plt_y[list(isolation_set)]


        plt_x, plt_y = getPosition(plt_x, plt_y, west, east, north, south)
        plt_x_isolation, plt_y_isolation = getPosition(
            plt_x_isolation, plt_y_isolation, west, east, north, south)
        plt_x_infection, plt_y_infection = getPosition(
            plt_x_infection, plt_y_infection, west, east, north, south)
        plt_x_sick, plt_y_sick = getPosition(
            plt_x_sick, plt_y_sick, west, east, north, south)

        condition["x1"] = list(x1)
        condition["x2"] = list(x2)
        condition["y1"] = list(y1)
        condition["y2"] = list(y2)
        condition["plt_xSet"].insert(day, list(plt_x))
        condition["plt_ySet"].insert(day, list(plt_y))
        condition["plt_x_isolationSet"].insert(day, list(plt_x_isolation))
        condition["plt_y_isolationSet"].insert(day, list(plt_y_isolation))
        condition["plt_x_infectionSet"].insert(day, list(plt_x_infection))
        condition["plt_y_infectionSet"].insert(day, list(plt_y_infection))
        condition["plt_x_sickSet"].insert(day, list(plt_x_sick))
        condition["plt_y_sickSet"].insert(day, list(plt_y_sick))
        condition["infected_index_history"] = infected_index_history
        infected_index_set = [int(i) for i in infected_index_set]
        isolation_set = [int(i) for i in isolation_set]
        condition["infected_index_set"] = list(infected_index_set)
        condition["isolation_set"] = list(isolation_set)
        return jsonify(condition)
    else:
        return "404 error"


@app.route('/addCondition', methods=['GET', 'POST'])
def addCondition():
    request_method = request.method
    if request_method == 'POST':
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='cjs530124HHH',
                             database='ESPS')
        cursor = db.cursor()
        sql = 0
        view = request.get_json()["view"]
        condition = request.get_json()["condition"]
        sql = "INSERT INTO Condition_TABLE(condition_name,lat,lon,alt,Roll,Pitch,Heading,sum_of_human,incubation_period,treat_willingness, isolation_pos,infection_area,move_area_param,first_infected_cnt,total_day) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (view["name"], view["Lat"], view["Lon"], view["Alt"], view["Roll"], view["Pitch"], view["Heading"],
                  condition["sum_of_human"], condition["incubation_period"], condition["treat_willingness"], condition["isolation_pos"], condition["infection_area"], condition["move_area_param"], condition["first_infected_cnt"], condition["total_day"])
        cursor.execute(sql, values)
        for i in range(int(condition["total_day"])):
            for j in range(len(condition["plt_xSet"][i])):
                sql = "INSERT INTO Normal(condition_name,now_day,x,y) VALUES (%s,%s,%s,%s)"
                values = (view["name"], i, condition["plt_xSet"]
                          [i][j], condition["plt_ySet"][i][j])
                cursor.execute(sql, values)
            for j in range(len(condition["plt_x_infectionSet"][i])):
                sql = "INSERT INTO infection(condition_name,now_day,x,y) VALUES (%s,%s,%s,%s)"
                values = (view["name"], i, condition["plt_x_infectionSet"]
                          [i][j], condition["plt_y_infectionSet"][i][j])
                cursor.execute(sql, values)
            if i >= int(condition["incubation_period"]):
                for j in range(len(condition["plt_x_sickSet"][i])):
                    sql = "INSERT INTO sick(condition_name,now_day,x,y) VALUES (%s,%s,%s,%s)"
                    values = (view["name"], i, condition["plt_x_sickSet"]
                              [i][j], condition["plt_y_sickSet"][i][j])
                    cursor.execute(sql, values)
            if i >= int(condition["incubation_period"]) + int(condition["treat_willingness"]):
                for j in range(len(condition["plt_x_isolationSet"][i])):
                    sql = "INSERT INTO isolation_table(condition_name,now_day,x,y) VALUES (%s,%s,%s,%s)"
                    values = (view["name"], i, condition["plt_x_isolationSet"]
                              [i][j], condition["plt_y_isolationSet"][i][j])
                    cursor.execute(sql, values)
        results = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        return request.get_json()
    else:
        return "404 error"

@app.route('/getAllCondition', methods=['GET', 'POST'])
def getAllCondition():
    request_method = request.method
    if request_method == 'POST':
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='cjs530124HHH',
                             database='ESPS')
        cursor = db.cursor()
        sql = "Select condition_name, sum_of_human, first_infected_cnt, total_day from Condition_TABLE"
        cursor.execute(sql)
        results = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()
        return jsonify(results)
    else:
        return "404 error"


@app.route('/getCondition', methods=['GET', 'POST'])
def getCondition():
    request_method = request.method
    if request_method == 'POST':
        db = pymysql.connect(host='localhost',
                             user='root',
                             password='cjs530124HHH',
                             database='ESPS')
        cursor = db.cursor()
        sql = 0
        value = 0
        name = request.get_json()["name"]
        result = {}
        result["view"] = {}
        result["condition"] = {}
        result["condition"]["haveComp"] = True
        sql = "Select * from Condition_TABLE Where condition_name = %s"
        value = (name)
        cursor.execute(sql,value)
        sqlResult = cursor.fetchall()
        result["view"]["name"] = sqlResult[0][0]
        result["view"]["Lat"] = sqlResult[0][1]
        result["view"]["Lon"] = sqlResult[0][2]
        result["view"]["Alt"] = sqlResult[0][3]
        result["view"]["Roll"] = sqlResult[0][4]
        result["view"]["Heading"] = sqlResult[0][5]
        result["view"]["Pitch"] = sqlResult[0][6]
        result["condition"]["sum_of_human"] = sqlResult[0][7]
        result["condition"]["incubation_period"] = sqlResult[0][8]
        result["condition"]["treat_willingness"] = sqlResult[0][9]
        result["condition"]["isolation_pos"] = sqlResult[0][10]
        result["condition"]["infection_area"] = sqlResult[0][11]
        result["condition"]["move_area_param"] = sqlResult[0][12]
        result["condition"]["first_infected_cnt"] = sqlResult[0][13]
        result["condition"]["total_day"] = sqlResult[0][14]
        result["condition"]["plt_xSet"] =[]
        result["condition"]["plt_ySet"] =[]
        result["condition"]["plt_x_infectionSet"] =[]
        result["condition"]["plt_y_infectionSet"] =[]
        result["condition"]["plt_x_sickSet"] =[]
        result["condition"]["plt_y_sickSet"] =[]
        result["condition"]["plt_x_isolationSet"] =[]
        result["condition"]["plt_y_isolationSet"] =[]
        for day in range(result["condition"]["total_day"]):
            sql = "Select x , y from normal Where condition_name = %s and now_day = %s"
            value=(name,day)
            cursor.execute(sql,value)
            sqlResult = cursor.fetchall()
            xSet = []
            ySet = []
            for i in range(len(sqlResult)):
                xSet.append(float(sqlResult[i][0]))
                ySet.append(float(sqlResult[i][1]))
            result["condition"]["plt_xSet"].append(xSet)
            result["condition"]["plt_ySet"].append(ySet)
            sql = "Select x , y from infection Where condition_name = %s and now_day = %s"
            value=(name,day)
            cursor.execute(sql,value)
            sqlResult = cursor.fetchall()
            xSet = []
            ySet = []
            for i in range(len(sqlResult)):
                xSet.append(float(sqlResult[i][0]))
                ySet.append(float(sqlResult[i][1]))
            result["condition"]["plt_x_infectionSet"].append(xSet)
            result["condition"]["plt_y_infectionSet"].append(ySet)
            if day >= int(result["condition"]["incubation_period"]):
                sql = "Select x , y from sick Where condition_name = %s and now_day = %s"
                value=(name,day)
                cursor.execute(sql,value)
                sqlResult = cursor.fetchall()
                xSet = []
                ySet = []
                for i in range(len(sqlResult)):
                    xSet.append(float(sqlResult[i][0]))
                    ySet.append(float(sqlResult[i][1]))
                result["condition"]["plt_x_sickSet"].append(xSet)
                result["condition"]["plt_y_sickSet"].append(ySet)
            else:
                xSet = []
                ySet = []
                result["condition"]["plt_x_sickSet"].append(xSet)
                result["condition"]["plt_y_sickSet"].append(ySet)
            if day >= int(result["condition"]["incubation_period"])  + int(result["condition"]["treat_willingness"]):
                sql = "Select x , y from isolation_table Where condition_name = %s and now_day = %s"
                value=(name,day)
                cursor.execute(sql,value)
                sqlResult = cursor.fetchall()
                xSet = []
                ySet = []
                for i in range(len(sqlResult)):
                    xSet.append(float(sqlResult[i][0]))
                    ySet.append(float(sqlResult[i][1]))
                result["condition"]["plt_x_isolationSet"].append(xSet)
                result["condition"]["plt_y_isolationSet"].append(ySet)
            else:
                xSet = []
                ySet = []
                result["condition"]["plt_x_isolationSet"].append(xSet)
                result["condition"]["plt_y_isolationSet"].append(ySet)
        db.commit()
        cursor.close()
        db.close()
        return jsonify(result)
    else:
        return "404 error"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    