import envhelper

logger = envhelper.setupLogger()

logger.info("hallo Welt!")
logger.warning("hallo Welt2!")

envhelper.getConfigVal("Hallo", "Welt")