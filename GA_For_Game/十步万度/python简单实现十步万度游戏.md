@[TOC](python简单实现十步万度)
**故事起因：** 闲逛TapTap时看到了一个游戏十步万度，看到论坛里有人用代码过关，就自己下了玩一下。
随后在百度b站Tap上搜索攻略发现基本都是1000到10000度的攻略，后面更高难度关卡的基本就无了。

刚好最近学校学了遗传算法，突然想到可以用遗传算法求最优解。
但是作为第一步，实现是要用代码把这个游戏的功能实现了！
![梦幻联动](https://img-blog.csdnimg.cn/20210424235535158.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NjaWVuY2VMaW1pdA==,size_16,color_FFFFFF,t_70#pic_center =370x370)


# 一、 游戏介绍与代码实现
## 1. 玩法
**规则：** 每点击一个指针它会顺时针旋转90度，之后该指针所指方向的指针也会顺时针旋转90度。（连锁效应，类似于多米诺骨牌）
**目标：** 在限定点击次数下使指针旋转度数总和最多。
个人感觉整个游戏像是多米诺骨牌二维化。
例：点击左上角的指针2次，便达到了450度。（为方便，后面代码均以该图为例）
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210425000847133.gif#pic_center =250x400)
## 2. 游戏代码实现


**对指针标号：** 如图：把四个指针依次标号为0123
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210425013901669.jpg?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L1NjaWVuY2VMaW1pdA==,size_16,color_FFFFFF,t_70#pic_center =340x)
**存储玩家操作：** 
数组有序存储十个数表示玩家按该顺序点击十次。
例： [0 0 0 0 0 3 3 3 3 3] ： 点击标号为0的指针5次，再点击标号为3的指针5次

**对方向编码：**
 0，1，2，3 表示 上，右，下，左 四个方向。（游戏里指针初始方向为上，顺时针90度后依次为右，下，左）。
方便计算指针转动后的方向：==转动后的方向 = （ 原方向 + 1 ） % 4==
**存储指针及其位置：** 
map1000作为地图存储游戏里第一关的指针，==-1表示出界，其余数字表示该位置指针的方向==，一般指针初状态都指向上为0。
标号为n的指针在map1000中的位置： ==行：index1000[n][0]，列：index1000[n][1]==
```python
map1000 = [[-1, -1, -1, -1],
           [-1,  0,  0, -1],
           [-1,  0,  0, -1],
           [-1, -1, -1, -1]]

index1000 = [[1, 1], [1, 2],
             [2, 1], [2, 2]]
```
由于关卡较多，单独用Map.py存所有关卡地图，运行时再调用Map。
**代码实现：** 
传入：地图数组，指针位置数组，玩家操作数组
返回：分数
运行时只需改变传入的参数map和index即可更换关卡。
省去了游戏页面显示等功能，代码相对简洁。

```python
def star(map, index, operands):   # 输入地图map，表的位置index，玩家操作operands，返回分数
    thisMap = [l[:] for l in map] # 不能修改原地图，所以先进行复制
    score = 0
    
    for operand in operands:  # 依次读取玩家点击的指针标号

        # r,c表示下一个转动的指针在第r行c列
        r = index[int(operand)][0] # 玩家点击的行数
        c = index[int(operand)][1] # 玩家点击的列数
        
        while( thisMap[r][c] != -1 ): # 当下一个转动的指针不在界外时，产生蝴蝶效应
            # 改变指针方向，分数增加90
            thisMap[r][c] = (thisMap[r][c] + 1) % 4
            score += 90

            # 顺着该指针所指方向改变r，c，得到下一个转动的指针位置
            if(thisMap[r][c] == 0):   # 指向上
                r -= 1
            elif(thisMap[r][c] == 1): # 指向右
                c += 1
            elif(thisMap[r][c] == 2): # 指向下
                r += 1
            else:                     # 指向左
                c -= 1
                
    return score
```
这些代码存储到Game.py文件，运行时再调用。
## 3. 通关
### 大力出奇迹
运用代码通关有很多种方式，最简单的有随机和遍历。
**随机：** 随机生成许多个操作数组，再选出得分最高的数组。
**遍历：** 得出关卡里所有可能的操作数组，选出得分最高的。
但这两种方式不大可行，假设关卡里有n个指针，玩家可以点击tryNum次，则共有==n的tryNum次方==种情况，最简单的第一关就有4^10种。
这种方法就只能把一切交给奇迹了。
### 贪心
玩家每次点击前都会预判所有情况，从中选出得分最高的，局部最优解。

```python
map = Map.map1000
index = Map.index1000
tryNum = 10          # 规定的玩家点击次数
uIndex = len(index)  # 指针的数量，即指针标号的上界

'''贪心'''
best_operations = []
best_score = 0
for i in range(tryNum):                                      # 列表添加tryNum个元素
    for try_index in range(uIndex):                          # 添加元素时预判所有情况
        try_operations = best_operations + [try_index]
        try_score = Game.star(map, index, try_operations)
        #print("if add ", try_index, " then score: ", try_score)
        if(try_score > best_score):
            best_score = try_score
            best_index = try_index
    #print("so add: ", best_index)
    best_operations.append(best_index)                       # 选出局部最优解
print('best operands: ', best_operations, ' best score:  ' , best_score)
```
但事实再次证明了==每次局部最优不能代表全局最优==。
例如第一关用贪心得到1800，但第一关最优解应该是 2070 如 [0 1 1 2 1 2 1 3 0 0]
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210427185436788.PNG#pic_center =560x)

在4000的关卡里用贪心只能达到3870，甚至不能通关。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210427185138742.jpg#pic_center =550x)
换一个角度，玩家点击十次就相当于有十个变量，每个变量在指针标号里取值，那么这就成了一个找高维点集最值问题。
为简化，假设玩家
**==遗传算法：==** 最近刚学了遗传算法，发现可以用遗传算法通关，目前已实现遗传算法通关十步万度1000到10000的关卡，后续将整理发表。




