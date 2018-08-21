import logging
LEVELS = { 'debug':logging.DEBUG,
            'info':logging.INFO,
            'warning':logging.WARNING,
            'error':logging.ERROR,
            'critical':logging.CRITICAL,
            }
logging.basicConfig(
    filename="/home/cso/Neo4j_script_output/test3.log",
    level=LEVELS,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

from datetime import timedelta
import datetime

aa = datetime.datetime.now().date()
bb = aa + datetime.timedelta(days=-1)

aaa=str(aa).replace("-","")+'000000'
bbb=str(bb).replace("-","")+'000000'
print (aaa,bbb)
#logging.debug("Hello")
logging.info("Today's date: %s \nTomorrow's date:%s"%(aaa, bbb))

#Write error only when assert condition is False
assert (aaa==bbb), logging.error("aaa and bbb are not same. Difference: %d"%(55-10))