
import maya.OpenMaya as OM
import callbacks
import os


def mayaInit(input):
    """Run these functions when initializing Maya
    """
    print '- running mayaInit callback'
    reload(callbacks)
    callbacks.mayaInitCallback()

def preSceneSave(input):
    """Run these functions before saving a Maya scene
    """
    print '- running preSceneSave callback'
    reload(callbacks)
    callbacks.preSceneSaveCallback()

def postSceneSave(input):
    """Run these functions after saving a Maya scene
    """
    print '- running postSceneSave callback'
    reload(callbacks)
    callbacks.postSceneSaveCallback()
    
def preSceneOpen(input):
    """Run these functions before opening a scene
    """
    print '- running preSceneOpen callback'
    reload(callbacks)
    callbacks.preSceneOpenCallback()

def postSceneOpen(input):
    """Run these functions after opening a scene
    """
    print '- running postSceneOpen callback'
    reload(callbacks)
    callbacks.postSceneOpenCallback()

def setupCallbacks():
    """Setup the Open Maya callback listeners
    """
    mayaInitCB      = OM.MSceneMessage.addCallback(OM.MSceneMessage.kMayaInitialized,mayaInit)
    preSceneSaveCB  = OM.MSceneMessage.addCallback(OM.MSceneMessage.kBeforeSave,preSceneSave)
    postSceneSaveCB = OM.MSceneMessage.addCallback(OM.MSceneMessage.kAfterSave,postSceneSave)
    preSceneOpenCB  = OM.MSceneMessage.addCallback(OM.MSceneMessage.kBeforeOpen,preSceneOpen)
    postSceneOpenCB = OM.MSceneMessage.addCallback(OM.MSceneMessage.kAfterOpen,postSceneOpen)

def setupGlobals():
    """Create the maya environment variables
    """
    os.environ['ACTIVE_PROJECT'] = ''
    os.environ['ACTIVE_BLOCK']   = ''

# KEEP ON BOTTOM OF MODULE
def mainSetup():
    """Calls for the Main setup, setting up the global variables and assigning the callbacks
    """
    setupGlobals()
    setupCallbacks()