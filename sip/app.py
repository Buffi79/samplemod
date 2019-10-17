import envhelper
import time
import MyHelper

#logger = MyLogger.MyLogger()
logger = MyHelper.getLogger()


var = config = MyHelper.Config().getConfigVal("LOG","level")

print(var)




i = 1
while i < 10:
    i += 1
    logger.info("hallo Welt!" +str(i))
    logger.debug("hallo Welt!" +str(i))
    time.sleep (5)

logger.warning("hallo Welt2!")



