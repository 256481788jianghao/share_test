import matplotlib.pyplot as plxy

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
    
