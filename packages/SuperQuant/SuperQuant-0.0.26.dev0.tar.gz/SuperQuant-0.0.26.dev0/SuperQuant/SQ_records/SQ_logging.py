import logging
'''
logging级别注释：
DEBUG：详细信息，一般只在调试问题的时候使用
INFO：证明事情按预期工作
'''

def logging_explain():
    print('#############################################################################')
    print('#############################################################################')
    print('logging级别注释：')
    print('NOTSET：级别数字值：0,：无设置')
    print('DEBUG：级别数字值：10,：详细信息，一般只在调试问题的时候使用')
    print('INFO：级别数字值：20,：证明事情按预期工作')
    print('WARNING：级别数字值：30,：某些没有预料到的事件的提示，或者在将来可能会出现的问题提示。例如：磁盘空间不足。但是软件还是会照常运行')
    print('ERROR：级别数字值：40,：由于更严重的问题，软件已不能执行一些功能了')
    print('CRITICAL：级别数字值：50,：严重错误，表明软件已不能继续运行了')
    print('#############################################################################')
    print('#############################################################################')
    print('filemode解释："a"代表每次运行程序都继续写log；"w"则每次运行都覆盖之前的log')

def set_logging(level='INFO',
                path = '',
                filename='log.txt',
                filemode = 'a',
                format = '%(asctime)s - %(process)d - %(thread)d : Line: %(lineno)s - %(funcName)s - %(name)s - %(levelname)s : %(message)s',
                datefmt = None,#'%Y-%m-%d %H:%M:%S',
                whether_to_file = 1,
                whether_to_console = 1,
                name=__name__):
    if level == 'NOTSET': level = logging.NOTSET
    elif level == 'DEBUG': level = logging.DEBUG
    elif level == 'INFO': level = logging.INFO
    elif level == 'WARN': level = logging.WARN
    elif level == 'ERROR': level = logging.ERROR
    elif level == 'CRITICAL': level = logging.CRITICAL

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    if whether_to_file:
        logFilename = path+filename

        logging.basicConfig(level = level,
                            format = format,
                            filename = logFilename,
                            datefmt=datefmt,
                            filemode=filemode
                            )

    if whether_to_console:
        console = logging.StreamHandler()
        console.setLevel(level)
        console.setFormatter( logging.Formatter(format,datefmt))
        logging.getLogger('').addHandler(console)

    logger = logging.getLogger(name)
    return logger





