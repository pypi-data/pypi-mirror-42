import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn
seaborn.set(palette='deep',style='darkgrid')


class SQ_matplotlib_tools():
    def __init__(self):
        pass

    def explain(self,section = 'all'):
        # TODO (617644591@qq.com):增加并丰富seaborn的功能
        if section == 'all' or section =='seaborn':
            print('############## seaborn #############')
            print('seaborn暂时封装2个参数：[palette,style],请参考以下网址')
            print('palette设置：http://seaborn.pydata.org/tutorial/color_palettes.html#palette-tutorial')
            print('style设置：https://blog.csdn.net/llh_1178/article/details/77923033')


    def set_basics(self,palette='deep', style='darkgrid'):
        self.set_seaborn(palette = palette,style = style)

    def set_seaborn(self,palette='deep', style='darkgrid'):
        self.palette = palette
        self.style = style
        seaborn.set(palette=self.palette, style=self.style)

    # def single_plot(self,figsize = [20,10],add_subplot = [1,1,1],init = True):
    #     if init:
    #         self.fig = plt.figure(figsize=(figsize[0], figsize[1]))
    #     else: pass
    #     figp = self.fig.add_subplot(add_subplot[0], add_subplot[1], add_subplot[2])
    #     figp.plot(data.iloc[:500, :]['Close'], label='当前日期走势')



if __name__ == '__main__':
    SQ_matplotlib = SQ_matplotlib_tools()
    SQ_matplotlib.explain()
    SQ_matplotlib.set_basics()





