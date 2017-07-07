import matplotlib.pyplot as plxy
import datetime
import time

class PlotTool:
    colors = ['red','blue','yellow','green','black']
    
    def plotxy(self,XYs,xlabel='x',ylabel='y',title='(x,y)'):
        line_count = len(XYs)
        colIndex = 0
        for i in range(line_count):
            xy = XYs[i]
            x = xy[0]
            y = xy[1]

            if colIndex >= line_count -1:
                colIndex = 0
            plxy.plot(x,y,color=self.colors[colIndex])
            colIndex += 1
        plxy.xlabel(xlabel)
        plxy.ylabel(ylabel)
        plxy.show()

#得到包括今天在内过去n天的日期列表
def getDateList(n=0,removeWeekend = True):
    now = datetime.datetime.now()
    deltalist = [datetime.timedelta(days=-x) for x in range(n*2+1)]
    #print(deltalist)
    n_days = [ now + delta for delta in deltalist]
    if removeWeekend:
        n_days = [x for x in n_days if x.weekday() < 5]
    return [ x.strftime('%Y-%m-%d') for x in n_days ][0:n+1]

def dateToNum(date):
    return int(date.replace('-',''))

def numToDate(num):
    tmp = str(num)
    y = tmp[0:4]
    m = tmp[4:6]
    d = tmp[6:len(tmp)]
    return y+'-'+m+'-'+d

def getNow():
    now = time.time()
    return now

def strToFloat(string):
    #str_len = len(string)
    tmp = string
    try:
        return float(tmp)
    except:
        print(tmp)
        i = -1
        while not tmp[i].isdigit():
            tmp = tmp[0:i]
            i = i -1
        print(tmp)
        return float(tmp)

if __name__ == '__main__':
    pt = PlotTool()
    x=[1,2,3,4]
    y=[1,2,3,4]
    y2=[t+0.5 for t in y]
    y3=[t+0.5 for t in y2]
    y4=[t+0.5 for t in y3]
    y5=[t+0.5 for t in y4]
    y6=[t+0.5 for t in y5]
    XYs=[[x,y],[x,y2],[x,y3],[x,y4],[x,y5],[x,y6]]
    pt.plotxy(XYs)
    #getDateList(10)
    
