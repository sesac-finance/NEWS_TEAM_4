import logging
import sys
import datetime
import matplotlib.font_manager

logging.basicConfig(
    level=logging.DEBUG,
    format="'%(asctime)s : %(filename)s	: %(funcName)s : %(lineno)d	: %(levelname)s : %(message)s",
    # format="'%(asctime)s : %(name)s  : %(filename)s	: %(funcName)s : %(lineno)d	: %(levelname)s : %(message)s",
    handlers=[
        logging.FileHandler('./NEWS_TEAM_4_PACKAGE/log/debug_{:%Y%m%d}.log'.format(datetime.datetime.now()),
                            encoding='UTF-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)

