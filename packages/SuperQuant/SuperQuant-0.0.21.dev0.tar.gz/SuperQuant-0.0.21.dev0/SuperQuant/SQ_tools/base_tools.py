import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn
seaborn.set(palette='deep',style='darkgrid')
import QUANTAXIS as QA

def SQ_tools_get_random_position(data):
    data['SQ_position'] = np.random.randint(-1,2,len(data))
    return data


def read_h5_to_DataFrame(file=None,types=None,index = None, columns=None,data = None):
    import h5py
    import pandas as pd
    import numpy as np
    index = None
    columns = 'df/block1_items'
    data = 'df/block1_values'

    f = h5py.File(file,types)   #打开h5文件
    if index == None: pass
    else:
        index = f[index][:]
        if type(index[0]) == np.bytes_: index = list(map(lambda x:x.decode(encoding='UTF-8'),index.tolist()))
    if columns == None: pass
    else:
        columns = f[columns][:]
        if type(columns[0]) == np.bytes_: columns = list(map(lambda x:x.decode(encoding='UTF-8'),columns.tolist()))
    if data == None: pass
    else:
        data = f[data][:]

        result = pd.DataFrame(index=index,
                              columns=columns,
                              data = data)
    return result



