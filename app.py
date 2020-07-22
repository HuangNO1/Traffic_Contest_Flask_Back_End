import urllib
import requests
import json
import math
from decimal import *
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app, resources=r'/*')


#app.run(host='192.168.50.117', debug=True, threaded=True)  # 多进程多线程，进程processes默认为1

# 路由

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_way_1_route', methods=['GET', 'POST'])
def get_way_1_route():
    ori = request.args.get('ori')
    des = request.args.get('des')
    navi_way_1_result = navi_way_1(ori, des)

    result = {
        "code": 200,
        "name": "way 1 route",
        "msg": "get data success",
        "data": {  # 返回值会是一个dict类型的变量
            "way_1_route_final_min": navi_way_1_result[0],
            "way_1_route_final_second": navi_way_1_result[1]
        }
    }
    return jsonify(result)


@app.route('/get_way_2_route', methods=['GET', 'POST'])
def get_way_2_route():
    ori = request.args.get('ori')
    des = request.args.get('des')
    navi_way_2_result = navi_way_2(ori, des)

    result = {
        "code": 200,
        "name": "way 2 route",
        "msg": "get data success",
        "data": {  # 返回值会是一个dict类型的变量
            "way_2_route_final_min": navi_way_2_result[0],
            "way_2_route_final_second": navi_way_2_result[1]
        }
    }
    return result


@app.route('/get_way_3_route', methods=['GET', 'POST'])
def get_way_3_route():
    ori = request.args.get('ori')
    des = request.args.get('des')
    navi_way_3_result= navi_way_3(ori, des)

    result = {
        "code": 200,
        "name": "way 3 route",
        "msg": "get data success",
        "data": {  # 返回值会是一个dict类型的变量
            "way_3_route_final": navi_way_3_result,
        }
    }
    return result


@app.route('/send_fly_init_position', methods=['GET'])
def send_fly_init_position():
    x = request.args.get('x')
    y = request.args('y')
    z = request.args('z')



# 算法


error_code_list={'10001':'INVALID_USER_KEY',
                 '10002':'SERVICE_NOT_AVAILABLE',
                 '10003':'DAILY_QUERY_OVER_LIMIT',
                 '10004':'ACCESS_TOO_FREQUENT',
                 '10005':'INVALID_USER_IP',
                 '10006':'INVALID_USER_DOMAIN',
                 '10007':'INVALID_USER_SIGNATURE',
                 '10008':'INVALID_USER_SCODE',
                 '10009':'USERKEY_PLAT_NOMATCH',
                 '10010':'IP_QUERY_OVER_LIMIT',
                 '10011':'NOT_SUPPORT_HTTPS',
                 '10012':'INSUFFICIENT_PRIVILEGES',
                 '10013':'USER_KEY_RECYCLED',
                 '10014':'QPS_HAS_EXCEEDED_THE_LIMIT',
                 '10015':'GATEWAY_TIMEOUT',
                 '10016':'SERVER_IS_BUSY',
                 '10017':'RESOURCE_UNAVAILABLE',
                 '10019':'CQPS_HAS_EXCEEDED_THE_LIMIT',
                 '10020':'CKQPS_HAS_EXCEEDED_THE_LIMIT',
                 '10021':'CIQPS_HAS_EXCEEDED_THE_LIMIT',
                 '10022':'CIKQPS_HAS_EXCEEDED_THE_LIMIT',
                 '10023':'KQPS_HAS_EXCEEDED_THE_LIMIT',
                 '10029':'ABROAD_DAILY_QUERY_OVER_LIMIT',
                 '20000':'INVALID_PARAMS',
                 '20001':'MISSING_REQUIRED_PARAMS',
                 '20002':'ILLEGAL_REQUEST',
                 '20003':'UNKNOWN_ERROR',
                 '20011':'INSUFFICIENT_ABROAD_PRIVILEGES',
                 '20012':'ILLEGAL_CONTENT',
                 '20800':'OUT_OF_SERVICE',
                 '20801':'NO_ROADS_NEARBY',
                 '20802':'ROUTE_FAIL',
                 '20803':'OVER_DIRECTION_RANGE',
                 '40000':'QUOTA_PLAN_RUN_OUT',
                 '40001':'GEOFENCE_MAX_COUNT_REACHED',
                 '40002':'SERVICE_EXPIRED',
                 '40003':'ABROAD_QUOTA_PLAN_RUN_OUT',
                 '30000':'ENGINE_RESPONSE_DATA_ERROR'}

def check_error_code(error_code):
    result=error_code_list[str(error_code)]
    return result

def getkey():
#获取高德API的key
    key='13cc6976a639fe9f7349f43ee366b1c5'
    return key

def baidukey():
#获取百度API的key（key还没申请）
    key='0'
    return key

def getcityloc():
#获取所在城市的高德城市编码
    key=getkey()
    cityloc_url='https://restapi.amap.com/v3/ip?&key='+key
    cityloc_result=request_api(cityloc_url)
    #print(cityloc_result)
    return cityloc_result

def bd2gcj(ori):
#百度坐标系转换为火星坐标系（暂时未使用）
    key=getkey()
    bd2gcj_change_url='https://restapi.amap.com/v3/assistant/coordinate/convert?locations='+ori+'&coordsys=baidu&key='+key
    bd2gcj_change_result=request_api(bd2gcj_change_url)
    result=bd2gcj_change_result['locations']
    return result

def gcj2bd(ori):
#火星坐标系转换为百度坐标系（暂时未使用）
    key=baidukey()
    gcj2bd_change_url='http://api.map.baidu.com/geoconv/v1/?coords='+ori+'&from=3&to=5&ak='+key
    gcj2bd_change_result=request_api(gcj2bd_change_url)
    result=gcj2bd_change_result['result']
    return result

def gethospital(position,distance):
#检索给定范围内的医院急诊室
    key=getkey()
    gethospital_url='https://restapi.amap.com/v3/place/around?key='+key+'&location='+position+'&keywords=门诊&radius='+str(distance)+'&types=090101'
    gethospital_result=request_api(gethospital_url)
    if gethospital_result['infocode'] in error_code_list:
        return gethospital_result['infocode']
    counter=int(gethospital_result['count'])
    page=math.ceil(counter/20)
    result=[]
    for i in range(1,page+1):
        gethospital_url_page='https://restapi.amap.com/v3/place/around?key='+key+'&location='+position+'&keywords=门诊&radius='+str(distance)+'&types=090101&page='+str(i)
        gethospital_result_page=request_api(gethospital_url_page)
        if i<page:
            for j in range(0,20):
                result.append(gethospital_result_page['pois'][j])
        if i==page:
            for j in range(0,counter-(page-1)*20):
                result.append(gethospital_result_page['pois'][j])
    return result

def timechange(otime):
#输出时间转换
    ntime=[]
    hours=int(otime/3600)
    ntime.append(hours)
    minute=int((otime-hours*3600)/60)
    ntime.append(minute)
    return ntime

#暂时逻辑上有问题
def distancecalu(location1,location2):
#location1与location2间直线距离
    key=getkey()
    distance_index_url='http://restapi.amap.com/v3/distance?key='+key+'&origins='+location1+'&destination='+location2+'&type=0'
    distance_index_result=request_api(distance_index_url)
    if distance_index_result['infocode'] in error_code_list:
        return distance_index_result['infocode']
    distance=int(distance_index_result['results'][0]['distance'])
    return distance

def request_url_get(url):
    """ 请求url方法get方法 """
    try:
        r = requests.get(url=url, timeout=30)
        if r.status_code == 200:
            return r.text
        return None
    except RequestException:
        print('请求url返回错误异常')
        return None
    return 0

def parse_json(content_json):
    """  解析json函数 """
    result_json = json.loads(content_json)
    return result_json

def request_api(url):
    """ 请求高德api 解析json """
    result = request_url_get(url)
    result_json = parse_json(result)
    return result_json

def getloc(name):
#由地点名称查询地点坐标
    cityloc=getcityloc()
    city=cityloc['adcode']
    #city='changsha'
    key = getkey()
    loc_index_url = 'https://restapi.amap.com/v3/place/text?keywords='+str(name)+'&city='+str(city)+'&key='+str(key)+'&extensions=base'
    loc_index_result = request_api(loc_index_url)
    if loc_index_result['infocode'] in error_code_list:
        return loc_index_result['infocode']
    loc=loc_index_result['pois'][0]['location']
    return loc

def navi(ori,des):
#请求高德导航路线规划结果并取得最优解
    key=getkey()
    direct_index_url='https://restapi.amap.com/v3/direction/driving?strategy=10&origin='+ori+'&destination='+des+'&key='+key+'&extensions=base'
    direct_index_result=request_api(direct_index_url)
    if direct_index_result['infocode'] in error_code_list:
        return direct_index_result['infocode']
    result=direct_index_result['route']['paths'][0]
    return result

def cut(long):
#截取坐标
    short=''
    num=len(long)
    for i in range(0,num):
        if long[i] != ';':
            short=short+str(long[i])
        else:
            break
    return short

def getlnglat(point):
    lng=''
    lat=''
    for i in range(0,len(point)):
        if point[i]!=',':
            lng=lng+str(point[i])
        else:
            for j in range(i+1,len(point)):
                lat=lat+str(point[j])
            break
    result=[lng,lat]
    return result

def reconnectpoint(point):
    pointlist=[]
    for i in range(0,len(point)):
        pointlist.append(str(point[i][0])+','+str(point[i][1]))
    return pointlist

def clean_endpoint(point):
    ori=point
    pointnum=len(point)
    opi=list([0]*pointnum)
    for i in range(0,pointnum):
        point[i]=getlnglat(ori[i])
    for lngcounter in range(0,pointnum):
        for j in range(lngcounter+1,pointnum):
            if abs(float(point[lngcounter][0])-float(point[j][0]))<0.01:
                if abs(float(point[lngcounter][1])-float(point[j][1]))<0.01:
                    opi[lngcounter]=1  
    ori=reconnectpoint(ori)                
    endpointlist=[ori,opi]
    return endpointlist

def navi_way_1(ori,des):
#放飞无人机后直到终点的算法
#根据地点名称获取地点的坐标
    oriloc=getloc(ori)
    desloc=getloc(des)
    if oriloc in error_code_list or desloc in error_code_list:
        return check_error_code(oriloc)
#高德中求当前最优驾驶路线
    mainnaviresult=navi(oriloc,desloc)
    if type(mainnaviresult)=='str':
        return check_error_code(mainnaviresult)
#建立耗时表，并将第一项填充为当前最优驾驶路线耗时
    durationlist=[]
    durationlist.append(float(mainnaviresult['duration']))
    #naviresult=[]
    #naviresult.append(mainnaviresult)
#将当前方案按照每一个step的起点做分割并记录起点坐标
    steps=mainnaviresult['steps']
    pointnum=len(steps)
    endpoint=[]

    for i in range(0,pointnum):
        endpoint.append(cut(steps[i]['polyline']))
#计算起点运输到分割点，分割点起飞至终点的耗时（此处无人机飞行速度设置为50km/h，起飞降落需要5分钟备用时间，没有飞行范围限制），并将耗时放置在耗时表中
    for j in range(0,pointnum):
        tempnaviresult=navi(oriloc,endpoint[j])
        if type(tempnaviresult)=='str':
            return check_error_code(tempnaviresult)
        durationbycar=int(tempnaviresult['duration'])
        tempdistance=distancecalu(endpoint[j],desloc)
        if tempdistance in error_code_list:
            return check_error_code(tempdistance)
        durationbyair=(tempdistance/50000*60+5)*60
        duration=durationbycar+durationbyair
        durationlist.append(duration)
#清洗距离太近的点
    endpointopi=clean_endpoint(endpoint)
    for i in range(0,pointnum):
        if endpointopi[1][i]==1:
            durationlist[i]=float('inf')
    endpoint=endpointopi[0]
#计算最优解与次优解，并找出最优解和次优解放飞地点（即在耗时表中的位置）
    minduration=min(durationlist)
    mindurationpos=durationlist.index(min(durationlist))
    durationlist[mindurationpos]=float('inf')
    secondduration=min(durationlist)
    seconddurationpos=durationlist.index(min(durationlist))

#构建最优解paths值
    minresult=[]
    for i in range(0,mindurationpos):
        minresult.append(mainnaviresult['steps'][i])
    min_air_distance=distancecalu(endpoint[mindurationpos],desloc)
    min_distance=int(distancecalu(oriloc,endpoint[mindurationpos]))+int(min_air_distance)
    polyline=endpoint[mindurationpos]+','+desloc
    air_info={'action':'放飞无人机','instruction':'由此处放飞无人机至终点','distance':min_air_distance,'duration':minduration,'polyline':polyline}
    minresult.append(air_info)
#构建次优解paths值
    secondresult=[]
    for i in range(0,seconddurationpos):
        secondresult.append(mainnaviresult['steps'][i])
    second_air_distance=distancecalu(endpoint[seconddurationpos],desloc)
    second_distance=int(distancecalu(oriloc,endpoint[seconddurationpos]))+int(second_air_distance)
    second_polyline=endpoint[seconddurationpos]+','+desloc
    air_info={'action':'放飞无人机','instruction':'由此处放飞无人机至终点','distance':second_air_distance,'duration':secondduration,'polyline':second_polyline}
    secondresult.append(air_info)
#输出最优解及次优解
    way_1_route_final_min={'origin':{'name':ori,'location':oriloc},'destination':{'name':des,'location':desloc},'option':0,'paths':{'path':0,'distance':min_distance,'duration':minduration,'steps':minresult}}
    way_1_route_final_second={'origin':{'name':ori,'location':oriloc},'destination':{'name':des,'location':desloc},'option':1,'paths':{'path':1,'distance':second_distance,'duration':secondduration,'steps':secondresult}}
#调试检验输出结果
    #print(minresult)
    #print(secondresult)
    #print(way_1_route_final_min)
    #print(way_1_route_final_second)
    return [way_1_route_final_min,way_1_route_final_second]

def navi_way_2(ori,des):
#放飞无人机至10公里范围内一三甲医院急诊室后再换回公路运输
#根据地点名称获取地点的坐标
    oriloc=getloc(ori)
    desloc=getloc(des)
    if oriloc in error_code_list:
        return check_error_code(oriloc)
    if desloc in error_code_list:
        return check_error_code(desloc)
    distance_limit=10000
#高德中求当前最优驾驶路线
    mainnaviresult=navi(oriloc,desloc)
    if type(mainnaviresult)=='str':
        return check_error_code(mainnaviresult)
#建立耗时表，并将第一项填充为当前最优驾驶路线耗时
    durationlist=[]
    durationlist.append(float(mainnaviresult['duration']))
#将当前方案按照每一个step的起点做分割并记录起点坐标
    steps=mainnaviresult['steps']
    pointnum=len(steps)
    endpoint=[]
    naviresult=[]
    firstresult=[float(mainnaviresult['duration']),'NOHOSPITAL','NOHOSPITAL']
    naviresult.append(firstresult)
    for i in range(0,pointnum):
        endpoint.append(cut(steps[i]['polyline']))    
#清洗距离太近的点
    endpointopi=clean_endpoint(endpoint)
    for i in range(0,pointnum):
        if endpointopi[1][i]==1:
            endpoint[i]=float('inf')
    for i in range(0,pointnum):
        if float('inf') in endpoint:
            endpoint.remove(float('inf'))
    pointnum=len(endpoint)
    endpoint=reconnectpoint(endpoint)
    #print()
#计算每个分割点与分割点周围医院急诊室的空中耗时与到达急诊室后的地面运输时间，并取出最小值及对应的急诊室POIID
    for j in range(0,pointnum):
        #print(['当前进行到第'+str(j)+'次循环，一共需要'+str(pointnum)+'次循环'])
        tempnaviresult=navi(oriloc,endpoint[j])
        if type(tempnaviresult)=='str':
            return check_error_code(tempnaviresult)
        durationbycar=int(tempnaviresult['duration'])
        nearbyhospital=gethospital(endpoint[j],distance_limit)
        hospitalnum=len(nearbyhospital)
        tempduration=[]
        hospoint=[]
        delepoint=[]
        for i in range(0,hospitalnum):
            hospoint.append(nearbyhospital[i]['location'])
        hospointopi=clean_endpoint(hospoint)
        for i in range(0,hospitalnum):
            if hospointopi[1][i]==1:
                hospoint[i]=float('inf')
                delepoint.append(i)
        for i in range(0,hospitalnum):
            if float('inf') in hospoint:
                hospoint.remove(float('inf'))
        nearbyhospital=[nearbyhospital[i] for i in range(0,hospitalnum) if (i not in delepoint)]
        hospitalnum=len(hospoint)

        if hospitalnum!=0:
            for k in range(0,hospitalnum):
                hospitalpos=nearbyhospital[k]['location']
                navi_after_air=navi(hospitalpos,desloc)
                air_distance=distancecalu(endpoint[j],hospitalpos)
                air_duration=(air_distance/50000*60+5)*60
                duration_after_air=float(navi_after_air['duration'])
                tempduration.append(duration_after_air+air_duration)
            minduration=min(tempduration)
            mindurationpos=tempduration.index(minduration)
            pointnaviresult=[minduration+durationbycar,nearbyhospital[mindurationpos]['name'],nearbyhospital[mindurationpos]['location']]
        if hospitalnum==0:
            pointnaviresult=[float(mainnaviresult['duration']),'NOHOSPITAL','NOHOSPITAL']
        naviresult.append(pointnaviresult)
        #print(['第'+str(j)+'次循环已完成'])
#构建完整的耗时矩阵
    for i in range(1,len(naviresult)):
        durationlist.append(naviresult[i][0])
#计算最优解及次优解，并输出在耗时矩阵中的位置
    minduration=min(durationlist)
    mindurationpos=durationlist.index(min(durationlist))
    durationlist[mindurationpos]=float('inf')
    for i in range(0,len(durationlist)):
        if durationlist[i]==minduration:
            durationlist[i]=float('inf')
    secondduration=min(durationlist)
    seconddurationpos=durationlist.index(min(durationlist))
#构建最优解paths值
    minresult=[]
    if naviresult[mindurationpos][1]!='NOHOSPITAL':    
        for i in range(0,mindurationpos):
            minresult.append(mainnaviresult['steps'][i])
        hosloc=naviresult[mindurationpos][2]
        min_air_distance=distancecalu(endpoint[mindurationpos],hosloc)
        min_air_duration=(min_air_distance/50000*60+5)*60
        polyline=endpoint[mindurationpos]+','+hosloc
        air_info={'action':'放飞无人机','instruction':'由此处放飞无人机至'+naviresult[mindurationpos][1],'distance':min_air_distance,'duration':min_air_duration,'polyline':polyline}
        minresult.append(air_info)
        navi_after_air=navi(hosloc,desloc)        
        min_distance=int(distancecalu(oriloc,endpoint[mindurationpos]))+int(min_air_distance)+int(navi_after_air['distance'])
        for i in range(0,len(navi_after_air['steps'])):
            minresult.append(navi_after_air['steps'][i])
    if naviresult[mindurationpos][1]=='NOHOSPITAL':
        minresult=mainnaviresult['steps']
        min_distance=mainnaviresult['distance']
#构建次优解paths值
    secondresult=[]
    for i in range(0,seconddurationpos):
        secondresult.append(mainnaviresult['steps'][i])
    if naviresult[seconddurationpos][1]!='NOHOSPITAL':
        hosloc=naviresult[seconddurationpos][2]
        second_air_distance=distancecalu(endpoint[seconddurationpos],hosloc)
        second_air_duration=(second_air_distance/50000*60+5)*60
        polyline=endpoint[seconddurationpos]+','+hosloc
        air_info={'action':'放飞无人机','instruction':'由此处放飞无人机至'+naviresult[seconddurationpos][1],'distance':second_air_distance,'duration':second_air_duration,'polyline':polyline}
        secondresult.append(air_info)
        navi_after_air=navi(hosloc,desloc)
        second_distance=int(distancecalu(oriloc,endpoint[seconddurationpos]))+int(second_air_distance)+int(navi_after_air['distance'])
        for i in range(0,len(navi_after_air['steps'])):
            secondresult.append(navi_after_air['steps'][i])
    if naviresult[seconddurationpos][1]=='NOHOSPITAL':
        secondresult=mainnaviresult['steps']
        second_distance=mainnaviresult['distance']
#输出最优解及次优解
    way_2_route_final_min={'origin':{'name':ori,'location':oriloc},'destination':{'name':des,'location':desloc},'option':0,'hosinfo':{'hosname':naviresult[mindurationpos][1],'hosloc':naviresult[mindurationpos][2]},'paths':{'path':0,'distance':min_distance,'duration':minduration,'steps':minresult}}
    way_2_route_final_second={'origin':{'name':ori,'location':oriloc},'destination':{'name':des,'location':desloc},'option':1,'hosinfo':{'hosname':naviresult[seconddurationpos][1],'hosloc':naviresult[seconddurationpos][2]},'paths':{'path':1,'distance':second_distance,'duration':secondduration,'steps':secondresult}}
#调试检验输出结果
    #print(minresult)
    #print(secondresult)
    #print(way_2_route_final_min)
    #print(way_2_route_final_second)    
    return [way_2_route_final_min,way_2_route_final_second]

def navi_way_3(ori,des):
#完全空中跳板运输法，可能可以在市区内两点中的运输。
#获取起点、终点坐标并计算两点间距离
    oriloc=getloc(ori)
    desloc=getloc(des)
    distance=distancecalu(oriloc,desloc)
    distance_limit=10000
    steps=[]
    steps.append([ori,oriloc,'0'])
#小于10公里，直接采用无人机运输
    if distance<=distance_limit:
        air_distance=distance
        air_duration=(air_distance/50000*60+5)*60
        steps.append(['直接放飞无人机至终点',air_distance,desloc])
#大于10公里，寻找跳板
    if distance>distance_limit:
        ori_pos=getlnglat(oriloc)
        des_pos=getlnglat(desloc)
        theta_od=math.atan2(float(des_pos[0])-float(ori_pos[0]),float(des_pos[1])-float(ori_pos[1]))
        condition=0
        on_search=oriloc
        point_list=[]
        q=[]
        limit_to_des_distance=distancecalu(desloc,oriloc)+10
        while(condition==0):
            to_des_distance=distancecalu(desloc,on_search)
            if to_des_distance>limit_to_des_distance:
                condition=2
                break
            if to_des_distance<limit_to_des_distance:
                limit_to_des_distance=to_des_distance
            if to_des_distance<=distance_limit:
                point_list.append([des,desloc,str(to_des_distance)])
                condition=1
                break
            hospital_list=gethospital(on_search,distance_limit)
            next_search=[]
            for i in range(0,len(hospital_list)):
                next_search.append([hospital_list[i]['name'],hospital_list[i]['location'],hospital_list[i]['distance']])
            #清洗距离太近的点
            endpoint=[]
            pointnum=len(next_search)
            for i in range(0,pointnum):
                endpoint.append(next_search[i][1])
            endpointopi=clean_endpoint(endpoint)
            for i in range(0,pointnum):
                if endpointopi[1][i]==1:
                    next_search[i]=float('inf')
            for i in range(0,pointnum):
                if float('inf') in next_search:
                    next_search.remove(float('inf'))
            if len(next_search)==0:
                condition=2
                break
            on_search_pos=getlnglat(on_search)
            alpha=0.5
            for i in range(0,len(next_search)):
                next_search_pos=getlnglat(next_search[i][1])
                theta_temp=math.atan2(float(next_search_pos[0])-float(on_search_pos[0]),float(next_search_pos[1])-float(on_search_pos[1]))
                q_temp=Decimal(str(alpha))*(Decimal(1)-abs(Decimal(str(theta_temp))-Decimal(str(theta_od)))/Decimal(str(math.pi)))+(Decimal(1)-Decimal(str(alpha)))*Decimal(next_search[i][2])/Decimal(10000)
                q_temp=float(q_temp)
                q.append(q_temp)
            max_q=max(q)
            max_q_loc=q.index(max_q)
            point_list.append(next_search[max_q_loc])
            on_search=next_search[max_q_loc][1]
            q=[]
        if condition==1:
            min_distance=0
            for i in range(0,len(point_list)):
                steps.append(point_list[i])
                min_distance=min_distance+float(point_list[i][2])
            minduration=(min_distance/50000*60+5)*60+(len(point_list)-1)*300
        if condition==2:
            steps.append(['CANNOT REACH','CANNOT REACH','CANNOT REACH'])
            min_distance=float('inf')
            minduration=float('inf')
    way_3_route_final={'origin':{'name':ori,'location':oriloc},'destination':{'name':des,'location':desloc},'option':0,'paths':{'path':0,'distance':min_distance,'duration':minduration,'steps':steps}}    
    #print(way_3_route_final)
    return way_3_route_final

#主函数由此开始#    
#ori=input('Input Ori:\n')
#des=input('Input Des:\n')
#test_error_code=input('Test Error Code Mode:')

#错误码测试入口
#if test_error_code in error_code_list:
    #print(check_error_code(test_error_code))
#oriloc=getloc(ori)
#desloc=getloc(des)
#函数入口位置
#navi_way_1_result=navi_way_1(ori,des)
#navi_way_2_result=navi_way_2(ori,des)
#navi_way_3_result=navi_way_3(ori,des)
#print('EoE')
