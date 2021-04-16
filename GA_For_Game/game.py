# 表图，0，1，2，3表示上，下，左，右，-1表示出界
# 4个表，初始都为0（指向上）
map = [[-1, -1, -1, -1],                        
       [-1,  0,  0, -1],
       [-1,  0,  0, -1],
       [-1, -1, -1, -1]]
# 玩家操作0表示按下表图里1行1列的那个表，操作1表示按下表图里1行2列的那个表，依此类推
enCode = { 0:[1,1], 1:[1,2], 2:[2,1], 3:[2,2] }

def effect(map, now, score): # 当前效果： 指针顺时针转90度，温度提高90度， 并把当前位置顺指针方向移
       map[ now[0] ][ now[1] ] = ( map[ now[0] ][ now[1] ] + 1 ) % 4

       score += 90

       if( map[ now[0] ][ now[1] ] == 0):    # 指向上
              now[0] -= 1
       elif( map [now[0] ][ now[1] ] == 1 ): # 指向右
              now[1] += 1
       elif( map[ now[0] ][ now[1] ] == 2 ): # 指向下
              now[0] += 1
       else:                                 # 指向左
              now[1] -= 1

       return score

def star(operands): # 输入玩家操作operands，返回分数
       thisMap = [l[:] for l in map]
       score = 0
       now = [-1, -1]
       for operand in operands: # 读取玩家操作
              # 确定当前位置
              now[0] = enCode[operand][0]
              now[1] = enCode[operand][1]
              # 产生蝴蝶效应
              while( thisMap[ now[0] ][ now[1] ] != -1 ):
                     score = effect(thisMap, now, score)
       return score
#测试
print(star([0,0,0,0,0,0,0,0,0,0]))