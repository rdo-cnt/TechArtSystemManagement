
import os

DRIVE = 'G:'
BASE_PATH = os.path.join(DRIVE, os.sep, 'BCIT')
SYSTEM_PATH = os.path.join(BASE_PATH, 'system')
PIPELINE_PATH = os.path.join(SYSTEM_PATH, 'pipeline')
PROJECTS_PATH = os.path.join(SYSTEM_PATH, 'projects')
SANDBOX_PATH = os.path.join(SYSTEM_PATH, 'sandbox')
CODE_PATH = os.path.join(PIPELINE_PATH, 'code')


PROJECT_BASE_BLOCKS = [	'code', 
						'config']


PROJECT_PROD_BLOCKS = [	'assets']


PROD_BLOCK_BASE_FOLDERS = [	'geometry', 
							'audio', 
							'images',
							'images/playblasts',
							'images/renders',
							'scenefiles', 
							'scenefiles/maya',
							'scenefiles/houdini']