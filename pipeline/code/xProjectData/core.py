
# import
import os
import string
import logging
from xConfig import baseConfig
reload(baseConfig)

# setup
logger = logging.getLogger(__name__)


def getListOfProjects():
	"""
	Returns a list of active projects
	"""
	projects = os.listdir(baseConfig.PROJECTS_PATH)

	return projects


def getListOfProjectBlocks(project):

	"""Returns a list of active projects

	:return: List of project blocks
	:rtype: list
	"""
	projectPath = os.path.join(baseConfig.PROJECTS_PATH, project)
	blocks = os.listdir(projectPath)

	return blocks


def setProject(project):
	"""Set the project in the environment variable

	:param project: Project name
	:type project: string 
	:raises Exception: Project must exist to be set
	"""
	if not project in getListOfProjects():
		raise Exception('Invalid project')
	os.environ['ACTIVE_PROJECT'] = project


def setBlock(block):
	"""Set the block in the environment variable

	:param block: Block name
	:type block: string 
	:raises Exception: Block must exist to be set
	"""
	if not block in getListOfProjectBlocks(os.getenv('ACTIVE_PROJECT')):
		raise Exception('Invalid block')
	os.environ['ACTIVE_BLOCK'] = block


def setProjectBlock(project, block):
	"""Sets the project and block at the same time

	:param project: Project name
	:type project: string
	:param block: Block name
	:type block: string
	"""
	setProject(project)
	setBlock(block)


def getProjectBlock():
	"""Obtain the active project and block

	:return: Return the active project and active block
	:rtype: string, string
	"""
	return os.getenv('ACTIVE_PROJECT'), os.getenv('ACTIVE_BLOCK')



class Project(object):
	"""The root of all the content inside it, the project holds blocks with assets
	"""
	def __init__(self, project=None, create=False):
		"""Initialize asset

		:param project: Project name, defaults to None
		:type project: string, optional
		:param create: Will the project be created?, defaults to False
		:type create: bool, optional
		:raises Exception: A project name must be passed on as a parameter
		:raises Exception: The project name must exist!
		"""
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
		"""Checks if project exists

		:param project: Project name
		:type project: string
		:return: Return if project exists
		:rtype: bool
		"""
		return project in getListOfProjects()


	def __createProject(self, project):
		"""Create the project directory

		:param project: [description]
		:type project: [type]
		:raises Exception: The project id must have 4 letters
		:raises Exception: The project id needs to be lower cased with no digits or special characters
		"""
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
		"""Create a block object

		:param block: Block name
		:type block: string
		:param validate: Will validate?, defaults to True
		:type validate: bool, optional
		:param prod: Will be set in production, defaults to True
		:type prod: bool, optional
		:return: Return new block
		:rtype: block
		"""
		block = Block(block, create=True, validate=validate, prod=prod)
		return block


	def createBlocks(self, blocks):
		"""Create multiple blocks

		:param blocks: List of blocks
		:type blocks: list
		:return: List of objects
		:rtype: list
		"""
		blockObjs = []
		for block in blocks:
			blockObj = self.createBlock(block)
			blockObjs.append(blockObj)

		return blockObjs


	def getListOfProjectBlocks(self):
		"""Returns a list of active projects

		:return: list of blocks
		:rtype: list
		"""
		projectPath = os.path.join(baseConfig.PROJECTS_PATH, self.__project)		
		blocks = os.listdir(projectPath)
		blocks.sort()
		return blocks


	def getListOfProductionBlocks(self):
		"""Returns a list of production blocks

		:return: Return a list of production blocks
		:rtype: list
		"""
		'''
		
		'''
		blocks = []
		for block in self.getListOfProjectBlocks():
			blockObj = Block(block)
			if blockObj.isProductionBlock():
				blocks.append(block)
		blocks.sort()
		return blocks



class Block(object):
	"""Second layer of a project. Can be a scene of movie.
	"""
	def __init__(self, block=None, create=False, validate=True, prod=True):
		"""Initialize the block

		:param block: block Name, defaults to None
		:type block: string, optional
		:param create: Will be created?, defaults to False
		:type create: bool, optional
		:param validate: will be validated?, defaults to True
		:type validate: bool, optional
		:param prod: Will be set in production, defaults to True
		:type prod: bool, optional
		:raises Exception: A project must be assigned in the environment variables
		:raises Exception: A block must be assigned in the environment variables
		:raises Exception: A valid block name must be given
		"""
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
		"""Checks if block directory exists

		:param block: Block name
		:type block: string
		:return: Does the asset folder exist in the block folder?
        :rtype: bool
		"""
		blockPath = os.path.join(baseConfig.PROJECTS_PATH, self.__project, block)
		return os.path.isdir(blockPath)


	def __createBlock(self, block, validate=True, prod=True):
		"""[summary]

		:param block: Block name
		:type block: string
		:param validate: Will validate?, defaults to True
		:type validate: bool, optional
		:param prod: Will be set in production, defaults to True
		:type prod: bool, optional
		:raises Exception: Block must not already exist
		:raises Exception: Project ID must 4 letters and 4 digits
		:raises Exception: Block ID must start with 4 lower case letters
		"""

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
		"""Get the block type

		:param block: Block name
		:type block: string
		:return: Block type
		:rtype: string
		"""
		if block == 'code':
			return 'code'
		elif block == 'config':
			return 'config'
		else:
			return 'production'

	def getType(self):
		"""Get type

		:return: Type
		:rtype: string
		"""
		return self.__type

	def isAssetBlock(self):
		"""Checks if block's of asset type

		:return: Is of asset type?
		:rtype: bool
		"""
		return self.getType() == 'assets'

	def isCodeBlock(self):
		"""Checks if block's of code type

		:return: Is of code type?
		:rtype: bool
		"""
		return self.getType() == 'code'

	def isConfigBlock(self):
		"""Checks if block's of config type

		:return: Is of config type?
		:rtype: bool
		"""
		return self.getType() == 'config'

	def isProductionBlock(self):
		"""Checks if block's of production type

		:return: Is of production type?
		:rtype: bool
		"""
		return self.getType() == 'production'

	def getBlockPath(self):
		"""Get the block's path

		:return: Block's directory path
		:rtype: string
		"""
		return os.path.join(baseConfig.PROJECTS_PATH, self.__project, self.__block)