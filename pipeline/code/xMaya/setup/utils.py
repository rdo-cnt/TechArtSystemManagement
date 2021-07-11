
from xConfig import baseConfig
import projectConfig
import os
import maya.mel as MM

def createProjectFolders():
    """Create folders based on the projectConfig, either on an active project or the sandbox
    """
    user = os.getenv('USER')

    # check basepath
    if os.getenv('ACTIVE_PROJECT'):
        project = os.getenv('ACTIVE_PROJECT')
        block = os.getenv('ACTIVE_BLOCK')
        projectsPath = baseConfig.PROJECTS_PATH

        basePath = os.path.join(projectsPath, project, block, 'scenefiles', 'maya', user)
        if not os.path.isdir(basePath):
            os.mkdir(basePath)
    else:
        mayaPath = os.path.join(baseConfig.SANDBOX_PATH, 'maya')
        basePath = os.path.join(mayaPath, user)
        if not os.path.isdir(mayaPath):
            os.mkdir(mayaPath)
        if not os.path.isdir(basePath):
            os.mkdir(basePath)

    # make sure to set the project path
    setProject(basePath)

    # get already existing folders
    existingFolders = os.listdir(basePath)

    # create relevant subfolders
    for folder in projectConfig.PROJECT_BASE_FOLDERS:
        if folder not in existingFolders:
            folderPath = os.path.join(basePath, folder)
            os.mkdir(folderPath)


def setProject(projectPath):
    """Set the Maya project

    :param projectPath: Project directory
    :type projectPath: string
    """
    MM.eval('setProject "{}"'.format(projectPath.replace(os.sep, '/')))