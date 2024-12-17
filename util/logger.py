import os
import sys
import logbook
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler


# 日志类型 自定义
def log_type(record, handler):
    log = "[{date}] [{level}] [{filename}] [{func_name}] [{lineno}] {msg}".format(
        date=record.time,  # 日志时间
        level=record.level_name,  # 日志等级
        filename=record.filename,  # 文件名
        func_name=record.func_name,  # 函数名
        lineno=record.lineno,  # 行号
        msg=record.message  # 日志内容
    )
    return log


# 日志打印到屏幕
log_std = ColorizedStderrHandler(bubble=True)
log_std.formatter = log_type

# 日志存放路径
# 如果不存在，则创建日志目录
LOG_DIR = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
# 日志打印到文件
log_path = os.path.join(LOG_DIR, '%s.log' % 'log')

log_file = TimedRotatingFileHandler(log_path, date_format='%Y-%m-%d', bubble=True, encoding='utf-8')
log_file.formatter = log_type

# 脚本日志
logger = Logger("script_log")


def init_logger():
    logbook.set_datetime_format("local")  # 设置时区格式为本地
    logger.handlers = []
    logger.handlers.append(log_file)
    logger.handlers.append(log_std)


# 实例化，默认调用
init_logger()