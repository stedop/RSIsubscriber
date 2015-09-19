import logging
import datetime


""" init log """
LOGFORMAT = '%(asctime)-15s %(message)s \n\n'
today = datetime.date.today()
logfile = "Logs/" + today.strftime('%d-%b-%Y') + ".log"
logging.basicConfig(
    filename=logfile,
    filemode="w",
    level=logging.WARN,
    format=LOGFORMAT
)
logging.captureWarnings(True)