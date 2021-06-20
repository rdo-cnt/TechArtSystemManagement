
# import
import os
import string
import logging
from xConfig import baseConfig
reload(baseConfig)

# setup
logger = logging.getLogger(__name__)


def getListOfProjects():
	'''
	returns a list of active projects
	'''
	projects = os.listdir(baseConfig.PROJECTS_PATH)

	return projects


def getListOfProjectBlocks(project):
	'''
	returns a list of active projects
	'''
	projectPath = os.path.join(baseConfig.PROJECTS_PATH, project)
	blocks = os.listdir(projectPath)

	return blocks


def setProject(project):
	if not project in getListOfProjects():
		raise Exception('Invalid project')
	os.environ['ACTIVE_PROJECT'] = project


def setBlock(block):
	if not block in getListOfProjectBlocks(os.getenv('ACTIVE_PROJECT')):
		raise Exception('Invalid block')
	os.environ['ACTIVE_BLOCK'] = block


def setProjectBlock(project, block):
	setProject(project)
	setBlock(block)


def getProjectBlock():
	return os.getenv('ACTIVE_PROJECT'), os.getenv('ACTIVE_BLOCK')



class Project(object):

	def __init__(self, project=None, create=False):

		# if the user wants it created
		if create:
			self.__project = project
			os.environ['ACTIVE_PROJECT'] = self.__project
			self.__createProject(self.__project)

		else:
			# if nothing passed in, get active project
			if project == None:
				project = os.getenv('ACTIVE_PROJECT')
				if project == None:
					raise Exception('No project is active. Please pass in a particular project')

			# make sure it's valid
			if not self.__isValidProject(project):
				raise Exception('{} is not a valid project!'.format(project))

			# then set it
			self.__project = project
			os.environ['ACTIVE_PROJECT'] = self.__project


	def __isValidProject(self, project):
		return project in getListOfProjects()


	def __createProject(self, project):

		# test for existing
		if project in getListOfProjects():
			logger.error('this project is already in place')
			return

		# test for 5 chars
		if not len(project) == 4:
			logger.error('the project id needs to be exactly 4 letters')
			raise Exception

		# test for ascii lower case letters only
		for letter in project:
			if not letter in string.ascii_lowercase:
				logger.error('the project id needs to be all lower case letters. no digits or special characters are allowed')
				raise Exception			

		# create the project
		projectPath = os.path.join(baseConfig.PROJECTS_PATH, project)
		os.mkdir(projectPath)

		# create relevant subfolders
		for block in baseConfig.PROJECT_BASE_BLOCKS:
			self.createBlock(block, validate=False, prod=False)
		for block in baseConfig.PROJECT_PROD_BLOCKS:
			self.createBlock(block, validate=False, prod=True)


	def createBlock(self, block, validate=True, prod=True):
		block = Block(block, create=True, validate=validate, prod=prod)
		return block


	def createBlocks(self, blocks):
		blockObjs = []
		for block in blocks:
			blockObj = self.createBlock(block)
			blockObjs.append(blockObj)

		return blockObjs


	def getListOfProjectBlocks(self):
		'''
		returns a list of active projects
		'''
		projectPath = os.path.join(baseConfig.PROJECTS_PATH, self.__project)		
		blocks = os.listdir(projectPath)
		blocks.sort()
		return blocks


	def getListOfProductionBlocks(self):
		'''
		returns a list of production blocks
		'''
		blocks = []
		for block in self.getListOfProjectBlocks():
			blockObj = Block(block)
			if blockObj.isProductionBlock():
				blocks.append(block)
		blocks.sort()
		return blocks



class Block(object):

	def __init__(self, block=None, create=False, validate=True, prod=True):

		# make sure we have an active project
		self.__project = os.getenv('ACTIVE_PROJECT')
		if self.__project == None:
			raise Exception('No project is active. Cannot instance block')

		# if the user wants it created
		if create:
			self.__createBlock(block, validate=validate, prod=prod)

		else:
			# if nothing passed in, get active block
			if block == None:
				block = os.getenv('ACTIVE_BLOCK')
				if block == None:
					raise Exception('No block is active. Please pass in a particular block')

			# make sure it's valid
			if not self.__isValidBlock(block):
				raise Exception('{} is not a valid block!'.format(block))

		# then set it
		self.__block = block
		os.environ['ACTIVE_BLOCK'] = self.__block

		# and set data
		self.__type = self.__getBlockType(block)


	def __isValidBlock(self, block):
		blockPath = os.path.join(baseConfig.PROJECTS_PATH, self.__project, block)
		return os.path.isdir(blockPath)


	def __createBlock(self, block, validate=True, prod=True):

		# test for existing
		if self.__isValidBlock(block):
			logger.error('this block is already in place')
			return

		if validate and prod:
			# test for 5 chars
			if not len(block) == 8:
				logger.error('the project id needs to be exactly 4 letters and 4 digits')
				raise Exception

			# test letters
			for letter in block[0:4]:
				if not letter in string.ascii_lowercase:
					logger.error('the block id needs to start with 4 lower case letters. no digits or special characters are allowed')
					raise Exception			

			# test digits
			for letter in block[4:]:
				if not letter in string.digits:
					logger.error('the block id needs to end with 4 digits. no letters or special characters are allowed')
					raise Exception

		# create the block
		blockPath = os.path.join(baseConfig.PROJECTS_PATH, self.__project, block)
		os.mkdir(blockPath)

		# create relevant subfolders
		if prod:
			for folder in baseConfig.PROD_BLOCK_BASE_FOLDERS:
				folderPath = os.path.join(blockPath, folder)
				os.mkdir(folderPath)


	def __getBlockType(self, block):
		
		if block == 'code':
			return 'code'
		elif block == 'config':
			return 'config'
		else:
			return 'production'

	def getType(self):
		return self.__type

	def isAssetBlock(self):
		return self.getType() == 'assets'

	def isCodeBlock(self):
		return self.getType() == 'code'

	def isConfigBlock(self):
		return self.getType() == 'config'

	def isProductionBlock(self):
		return self.getType() == 'production'

	def getBlockPath(self):
		return os.path.join(baseConfig.PROJECTS_PATH, self.__project, self.__block)