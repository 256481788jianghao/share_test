import matplotlib.pyplot as plxy

class PlotTool:
    colors = ['red','blue','yellow','green','black']
    
    def plotxy(self,XYs,xlabal='x',ylabal='y',title='(x,y)'):
        line_count = len(XYs);
        for i in range(line_count):
            xy = XYs[i]
            x = xy[0]
            y = xy[1]
            plxy.plot(x,y,color=self.colors[0])
        plxy.show()


if __name__ == '__main__':
    pt = PlotTool()
    x=[1,2,3,4]
    y=[1,2,3,4]
    XYs=[[x,y]]
    pt.plotxy(XYs)
    
