from .qnotebook import QNotebookPlugin

def classFactory(iface):
    return QNotebookPlugin(iface)
