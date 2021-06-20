import utils
import logging

logger = logging.getLogger(__name__)

def mayaInitCallback():
	utils.createProjectFolders()
	logger.info('I can do something here')

def preSceneSaveCallback():
	logger.info('I can do something here')

def postSceneSaveCallback():
	logger.info('I can do something here')

def preSceneOpenCallback():
	logger.info('I can do something here')

def postSceneOpenCallback():
	logger.info('I can do something here')