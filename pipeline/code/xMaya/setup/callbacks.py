import utils
import logging

logger = logging.getLogger(__name__)

def mayaInitCallback():
	"""Called when maya is initialized. Sets up the project in maya
	"""
	utils.createProjectFolders()
	logger.info('I can do something here')

def preSceneSaveCallback():
	"""Called before saving a scene
	"""
	logger.info('I can do something here')

def postSceneSaveCallback():
	"""Called after saving a scene
	"""
	logger.info('I can do something here')

def preSceneOpenCallback():
	"""Called before opening a scene
	"""
	logger.info('I can do something here')

def postSceneOpenCallback():
	"""Called after opening a scene
	"""
	logger.info('I can do something here')