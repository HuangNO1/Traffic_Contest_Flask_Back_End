交科賽後端 Flask API
===

![交科賽前後端.png](https://i.loli.net/2020/04/15/BizEhrCJtuGvALU.png)

## 網頁端

### 算法一方案

#### Request

說明：放飞无人机后直到终点的算法，根据地点名称获取地点的坐标。

方法：**Get**

URL：

```
http://127.0.0.1:5000/get_way_1_route
```

參數：

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| 起點 | String | 當前起點 |
| 終點 | String | 無人機要到達的目的地 |

#### Success 200

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | Object | 算法二最優與次優計算結果 |

**Success-Response:**

```json
{
	"code": 200,
	"name": "way 1 route",
	"msg": "get data success",
	"data": {#返回值会是一个dict类型的变量
		"way_1_route_final_min": {#算法一最优计算结果
			"origin": {#起点信息
				"name": ori,#起点名字，与输入值相同
				"location": oriloc#起点坐标
			},
			"destination":{#终点信息
				"name": des,#终点名字
				"location": desloc#终点坐标
			},
			"option": 0,
			"paths": {
				"path": 0,
				"distance": min_distance,#路径的距离
				"duration": minduration,#路径的耗时
				"steps": {#每一步驾驶动作的内容
					"action":#简要的驾驶动作
					"distance":#驾驶动作的距离
					"duration":#驾驶动作的耗时
					"instruction":#具体的驾驶动作
					"polyline":#本驾驶动作经过的路径（以多个坐标的形式给出）
				}
			}
		},
		"way_1_route_final_second": {#算法一次优计算结果（输出含义不变）
			"origin": {
				"name": ori,
				"location": oriloc
			},
			"destination": {
				"name": des,
				"location": desloc
			},
			"option": 1,
			"paths": {
				"path": 1,
				"distance": second_distance,
				"duration": secondduration,
				"steps": secondresult
			}
		}
	}
}
```

#### Error 4xx

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | null | 無 |

**Error-Response:**

```json
{
	"code": 500,
	"name": "way 1 route",
	"msg": "ERROR message",
	"data": null
}
```

### 算法二方案

說明：放飞无人机至10公里范围内一三甲医院急诊室后再换回公路运输。

方法：**Get**

URL：

```
http://127.0.0.1:5000/get_way_2_route
```

參數：

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| 起點 | String | 當前起點 |
| 終點 | String | 無人機要到達的目的地 |

#### Success 200

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | Object | 算法二最優與次優計算結果 |

**Success-Response:**

```json
{
	"code": 200,
	"name": "way 2 route",
	"msg": "get data success",
	"data": {
		"way_2_route_final_min": {#算法二最优计算结果
			"origin":{#起点信息
				"name": ori,#起点名字，与输入值相同
				"location": oriloc#起点坐标
			},
			"destination":{#终点信息
				"name": des,#终点名字
				"location": desloc#终点坐标
			},
			"option": 0,
			"hosinfo": {#无人机飞行目标医院的信息
				"hosname": naviresult[mindurationpos][1],#医院名称
				"hosloc": naviresult[mindurationpos][2]#医院坐标
			},
			"paths": {"path":0,
				"distance": min_distance,
				"duration": minduration,
				"steps":｛#每一步驾驶动作的内容
					"action":#简要的驾驶动作
					"distance":#驾驶动作的距离
					"duration":#驾驶动作的耗时
					"instruction":#具体的驾驶动作
					"polyline":#本驾驶动作经过的路径（以多个坐标的形式给出）
				}
			}
		},
		"way_2_route_final_second": {#算法二次优计算结果（输出含义不变）
			"origin": {
				"name": ori,
				"location": oriloc
			},
			"destination": {
				"name":des,
				"location":desloc
			},
			"option": 1,
			"hosinfo": {
				"hosname": naviresult[seconddurationpos][1],
				"hosloc": naviresult[seconddurationpos][2]},
				"paths": {
					"path":1,
					"distance":second_distance,
					"duration":secondduration,
					"steps":secondresult
				}
			}
		}
	}
}
```

#### Error 4xx

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | null | 無 |

**Error-Response:**

```json
{
	"code": 500,
	"name": "way 2 route",
	"msg": "ERROR message",
	"data": null
}
```

### 算法三方案

#### Resquest

說明：完全空中跳板运输法，可能可以在市区内两点中的运输。

方法：**Get**

URL：

```
http://127.0.0.1:5000/get_way_3_route
```

參數：

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| 起點 | String | 當前起點 |
| 終點 | String | 無人機要到達的目的地 |

#### Success 200

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | Object | 算法三計算結果 |

**Success-Response:**

```json
{
	"code": 200,
	"name": "way 3 route",
	"msg": "get data success",
	"data": {
		way_3_route_final: {#算法三最优计算结果
			"origin":{#起点信息
				"name": ori,#起点名字，与输入值相同
				"location": oriloc#起点坐标
			},
			"destination":{#终点信息
				"name": des,#终点名字
				"location": desloc#终点坐标
			},
			"option": 0,
			"paths": {
				"path": 0,
				"distance": min_distance,
				"duration": minduration,
				"steps": {
					list0:#医院名称
					list1:#医院坐标
					list2:#从上一点到本医院的距离
				}
			}
		}   
	}
}
```

#### Error 4xx

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | null | 無 |

**Error-Response:**

```json
{
	"code": 500,
	"name": "way 3 route",
	"msg": "ERROR message",
	"data": null
}
```

### 網頁端傳輸用戶選擇方案的初始位置

#### Resquest

說明：用戶在前端選取想要的方案中的無人機初始放飛位置，並透過數據請求將座標傳到後端。

方法：**Get**

URL：

```
http://127.0.0.1:5000/send_fly_init_position
```

參數：

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| X | Int | 無人機放飛地點在地圖上的 x 軸上的座標點 |
| Y | Int | 無人機放飛地點在地圖上的 Y 軸上的座標點 |
| Z | Int | 無人機高度（預設 0） |

#### Success 200

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | Object | 初始的座標位置 |


**Success-Response:**

```json
{
	"code": 200,
	"name": "send fly init position",
	"msg": "send fly init position Success",
	"data": {
		"x": x,
		"y": y,
		"z": 0
	}
}
```

#### Error 4xx

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | null | 無 |

**Error-Response:**

```json
{
	"code": 500,
	"name": "send fly init position",
	"msg": "ERROR message",
	"data": null
}
```

### 網頁端獲取無人機實時位置

#### Resquest

說明：需要每幾秒獲取無人機的位置做定位。

方法：**Get**

URL：

```
http://127.0.0.1:5000/get_fly_current_position
```

參數：

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| X | Int | 無人機當前在地圖上的 x 軸上的座標點 |
| Y | Int | 無人機當前在地圖上的 Y 軸上的座標點 |
| Z | Int | 無人機當前高度 |

#### Success 200

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | Object | 最新的座標位置 |

**Success-Response:**

```json
{
	"code": 200,
	"name": "get fly current position",
	"msg": "get fly current position Success",
	"data": {
		"x": x,
		"y": y,
		"z": z
	}
}
```

#### Error 4xx

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | null | 無 |

**Error-Response:**

```json
{
	"code": 500,
	"name": "get fly current position",
	"msg": "ERROR message",
	"data": null
}
```

## 仿真無人機端

### 無人機獲取初始位置

#### Resquest

說明：無人機要獲取初始放置的座標。

方法：**Get**

URL：

```
http://127.0.0.1:5000/get_fly_init_position
```

參數：

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| X | Int | 無人機放飛地點在地圖上的 x 軸上的座標點 |
| Y | Int | 無人機放飛地點在地圖上的 Y 軸上的座標點 |
| Z | Int | 無人機高度（預設 0） |

#### Success 200

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | Object | 初始的座標位置 |


**Success-Response:**

```json
{
	"code": 200,
	"name": "get fly init position",
	"msg": "get fly init position Success",
	"data": {
		"x": x,
		"y": y,
		"z": 0
	}
}
```

#### Error 4xx

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | null | 無 |

**Error-Response:**

```json
{
	"code": 500,
	"name": "get fly init position",
	"msg": "ERROR message",
	"data": null
}
```

### 彷真無人機傳輸當前實時位置

#### Resquest

說明：需要每幾秒傳送無人機的當前位置做定位。

方法：**Get**

URL：

```
http://127.0.0.1:5000/send_fly_current_position
```

參數：

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| X | Int | 無人機當前在地圖上的 x 軸上的座標點 |
| Y | Int | 無人機當前在地圖上的 Y 軸上的座標點 |
| Z | Int | 無人機當前高度 |

#### Success 200

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | Object | 最新的座標位置 |

**Success-Response:**

```json
{
	"code": 200,
	"name": "send fly current position",
	"msg": "send fly current position Success",
	"data": {
		"x": x,
		"y": y,
		"z": z
	}
}
```

#### Error 4xx

| 欄位 | 類型 | 描述 |
| --- | --- | --- |
| code | Int | 狀態碼 |
| name | String | 請求名稱 |
| msg | String | 返回信息 |
| data | null | 無 |

**Error-Response:**

```json
{
	"code": 500,
	"name": "send fly current position",
	"msg": "ERROR message",
	"data": null
}
```
