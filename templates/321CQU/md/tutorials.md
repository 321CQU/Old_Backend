# 321CQU使用教程

## 志愿者时长

### 查看志愿时长

点击进入**志愿者时长**页面后，会自动刷新当前志愿者时长记录

- 支持下拉刷新更新志愿时长记录

### 发送至邮箱

勾选✔自己想要的志愿时长记录（或者点击全选），点击发送按钮后，所选的志愿时长对应pdf文件会发送至你的邮箱

### 查看发送状态

可前往**任务管理/任务**查看pdf文件发送状态

## 课表

### 获取课表信息

- 方式一：点击进入**课表**页面后，点击左下角刷新图标可获取**当前学期**、**下一学期**课表信息，以及自动合并**自定义课表信息**
- 方式二：长按课程表主体部分，底部弹出选择框，选择**刷新课表**

### 查看上/下周课程信息

点击下方左右方向图标（左右图标中间显示周数）

- 负数表示**当前周**日期距离**所选周**日期还有多少周

### 切换学期

1. 点击右下方图标，页面下方会显示当前学期名称（例如：2022春）
2. 点击当前学期名称（例如：2022春），会弹出学期列表（蓝色表示当前所选学期）
3. 点击想要切换的学期名称
4. 再次点击右下方图标退出**切换学期模式**

### 自定义课表

*自定义课表会自动与原始课表合并*

1. 长按课程表主体部分，底部弹出选择框，选择**课表配置**
2. 进入课表配置界面后，会显示当前自定义课表信息
3. 点击**说明部分**，底部弹出选择框，点击**新建**或**备份到云**或**同步到本地**进行想要的操作

## 成绩查询

*成绩，排名数据是从重大教务处获取*

### 查询成绩

- 点击进入成绩查询页面，下拉刷新后会获取**成绩，排名**信息
- 点击上方学期名称可切换学期

### 查询排名

1. 点击右下方**蓝色图标**，进入统计模式
2. 再次点击**蓝色图标**，即可查看排名信息（专业，年级，班级）
3. 点击**红色图标**退出统计模式

### 绩点统计

***平均绩点**表示小程序根据所选成绩计算得出*

***综合绩点**表示重大教务处给出*

1. 点击右下方**蓝色图标**，进入统计模式
2. 所有成绩（除四六级，重修外）项在统计模式下名称部分会标为**浅绿色**（默认情况）
3. 点击**课程名称**可进行选中，取消选中
   - 点击**黄色图标**可进行**快速配置**和切换**四分制/五分制**
4. 再次点击**蓝色图标**，即可查看所选的绩点统计信息

## 广场

### 发帖子

- 在**除全部分区外**的其他分区，右下方会出现**蓝色加号按钮**，点击进入**编辑**界面，写作完成后点击**发送**按钮

- 帖子支持以下扩展（❤感谢`Towxml`第三方库的支持！！！）详情请参考下文的**帖子样例**
  - markdown
  - LaTeX
  - echarts图表
  - yuml流程图
  - audio
  - video

### 浏览

点击**帖子空白处**（*尽力修复中！！！*）即可跳转到帖子详情页面

- 包括完整帖子内容和评论

### 删除、修改

*长按帖子，底部弹出选项框（如果有对应权限）*

- **作者本人**具有删除，修改权限（包括对应评论）
- **开发者**和**对应分区管理员**具有删除权限（包括对应评论）



## 帖子样例

> 本部分展示目前帖子支持的扩展，其中的数据不具有真实性，具体markdown语法请自行搜索查阅

### 表格

|    课程名称    |     开设学院     |
| :------------: | :--------------: |
|    高等数学    |     数统学院     |
|    操作系统    |    计算机学院    |
| 数据结构与算法 | 大数据与软件学院 |

### 图片

![耐劳苦、尚俭朴、勤学业、爱国家](https://cqu.edu.cn/Uploads/CQUmain/%E5%AD%A6%E6%A0%A1%E7%AE%80%E4%BB%8B/%E6%A0%A1%E8%AE%AD.png)





### 代码

~~~c
#include <stdio.h>
int main()
{
    printf("Hello World!");
    return 0;
}
~~~



### 公式


$$
       \frac{1}{(\sqrt{\phi \sqrt{5}}-\phi) e^{\frac25 \pi}} =
         1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}}
          {1+\frac{e^{-8\pi}} {1+\ldots} } } }
$$

$$
\left( \sum_{k=1}^n a_k b_k \right)^{\!\!2} \leq
     \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
$$




### TodoList

- [x] 干饭
- [ ] 实验报告
- [x] 乐跑
- [ ] 晨曦打卡



### Echarts

```echarts
{
  "height": 260,
  "option": {
    "xAxis": {
      "type": "category",
      "boundaryGap": false,
      "data": [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun"
      ]
    },
    "yAxis": {
      "type": "value"
    },
    "series": [
      {
        "data": [
          820,
          932,
          901,
          934,
          1290,
          1330,
          1320
        ],
        "type": "line",
        "areaStyle": {}
      }
    ]
  }
}
```



```echarts
{
  "height": 260,
  "option": {
    "tooltip": {
      "trigger": "axis",
      "axisPointer": {
        "type": "cross",
        "label": {
          "backgroundColor": "#6a7985"
        }
      }
    },
    "legend": {
      "data": [
        "邮件营销",
        "联盟广告"
      ]
    },
    "xAxis": [
      {
        "type": "category",
        "boundaryGap": false,
        "data": [
          "周一",
          "周二",
          "周三",
          "周四",
          "周五",
          "周六",
          "周日"
        ]
      }
    ],
    "yAxis": [
      {
        "type": "value"
      }
    ],
    "series": [
      {
        "name": "AAA",
        "type": "line",
        "stack": "value",
        "areaStyle": {},
        "data": [
          120,
          132,
          101,
          134,
          90,
          230,
          210
        ]
      },
      {
        "name": "BBB",
        "type": "line",
        "stack": "value",
        "areaStyle": {},
        "data": [
          220,
          182,
          191,
          234,
          290,
          330,
          310
        ]
      }
    ]
  }
}
```

### State diagram

```yuml
// {type:state}
// {generate:true}

(start)[Start]->(Simulator running)
(Simulator running)[Pause]->(Simulator paused|do / wait)
(Simulator running)[Stop]->(end)
(Log retrieval)[Continue]->(Simulator running)
(Simulator paused)[Unpause]->(Simulator running)
(Simulator paused)[Data requested]->(Log retrieval|do / output log)
(Log retrieval)->(end)
```

### Sequence diagram

```yuml
// {type:sequence}
// {generate:true}

[:Computer]sendUnsentEmail>[:Server]
[:Computer]newEmail>[:Server]
[:Server]reponse.>[:Computer]
[:Computer]downloadEmail>[:Server]
[:Computer]deleteOldEmail>[:Server]
```
### Audio
<audio autoplay="false" loop="true" name="穿越时空的思念" author="和田薫" poster="http://p2.music.126.net/JI9uLRvH629NZ5GZLE06AQ==/2330964650912440.jpg?param=130y130"  src="http://music.163.com/song/media/outer/url?id=539324.mp3"></audio>


### Video
<video class="vidoe" src="http://zhaosheng.cqu.edu.cn/Upload/Album/Video/yxcd20200709/%E9%87%8D%E5%BA%86%E5%A4%A7%E5%AD%A690%E5%91%A8%E5%B9%B4%E6%A0%A1%E5%BA%86.mp4">视频</video>