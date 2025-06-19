from qgis.utils import iface
from qgis.core import (
    QgsProject,
)
try:
    from qgis.PyQt.QtCore import QAction
except ImportError:
    from qgis.PyQt.QtGui import QAction
from qgis.PyQt.QtGui import QIcon
import subprocess
import os
import shutil
import pickle
from .manage_dialog import ManageNotebooksDialog

note_icon = QIcon(':/images/themes/default/propertyicons/notes.svg')
book_icon = QIcon(':/images/themes/default/mActionLayoutManager.svg')
_command = [
    '@echo off\n',
    'call C:\\OSGeo4W\\bin\\04w_env.bat\n',
    '@echo off\n',
    'PATH %OSGEO4W_ROOT%\\apps\\qgis\\python;%PATH%\n',
    'PATH %OSGEO4W_Root%\\apps\\qgis\\bin;%PATH%\n',
    'PATH %OSGEO4W_ROOT%\\apps\\Qt5\\bin;%PATH%\n',
    'PATH %OSGEO4W_ROOT%\\apps\\Python312;%PATH%\n',
    'PATH %OSGEO4W_ROOT%\\apps\\Python312\\Scripts;%PATH%\n',
    'PATH %OSGEO4W_ROOT%\\apps\\qgis\\python\\plugins;%PATH%\n',
    'PATH %OSGEO4W_ROOT%\\apps\\Python312\\DLLs;%PATH%\n',
    'PATH %OSGEO4W_ROOT%\\apps\\Python312\\Lib;%PATH%\n',
    'PATH %OSGEO4W_ROOT%\\apps\\Python312\\Lib\\site-packages;%PATH%\n',
    '\n',
    'set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\\=/%/apps/qgis\n',
    'set GDAL_FILENAME_IS_UTF8=YES\n',
    'set VSI_CACHE=TRUE\n',
    'set VSI_CACHE_SIZE=1000000\n',
    'set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\\apps\\qgis\\qtplugins;%OSGEO4W_ROOT%\\apps\\qt5\\plugins\n',
    'set PYTHONPATH=%OSGEO4W_ROOT%\\apps\\qgis\\python\n',
    '\n'
    '@echo off\n'
]


class QNotebookPlugin:
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.jupyter_action = None
        self.manage_action = None
        self.project = QgsProject.instance()
        self.proj_path = self.project.absolutePath()
        self.file_path = self.project.absoluteFilePath()
        self.shell_path = "C:\\OSGeo4W\\OSGeo4W.bat"

        self.plugin_root = os.path.dirname(os.path.realpath(__file__))
        self.saved_path = os.path.join(self.plugin_root, 'notebooks.pkl')
        if os.path.exists(self.saved_path):
            with open(self.saved_path, 'rb') as f:
                self.saved_books = pickle.load(f)
        else:
            self.saved_books = []
        self.bat_path = os.path.join(self.plugin_root, 'run-jupyter.bat')
        if not os.path.exists(self.bat_path):
            with open(self.bat_path, 'w') as f:
                f.writelines(_command)

        self.iface.projectRead.connect(self.setVars)

    def initGui(self):
        self.jupyter_action = QAction(note_icon, 'Launch Jupyter')
        self.jupyter_action.triggered.connect(self.runJupyter)
        self.iface.addPluginToMenu('Jupyter Notebooks', self.jupyter_action)
        self.iface.addToolBarIcon(self.jupyter_action)
        self.manage_action = QAction(book_icon, 'Manage Saved Notebooks')
        self.manage_action.triggered.connect(self.manageNotebooks)
        self.iface.addPluginToMenu('Jupyter Notebooks', self.manage_action)

    def unload(self):
        self.iface.removeToolBarIcon(self.jupyter_action)
        self.iface.removePluginMenu('Jupyter Notebooks', self.jupyter_action)
        self.iface.removePluginMenu('Jupyter Notebooks', self.manage_action)

    def setVars(self):
        self.project = QgsProject.instance()
        self.proj_path = self.project.absolutePath()
        self.file_path = self.project.absoluteFilePath()

    def runJupyter(self):
        # copy placeholder .bat, add this line, run
        self.copy_path = os.path.join(self.plugin_root, 'run-jupyter-copy.bat')
        if os.path.exists(self.copy_path):
            os.remove(self.copy_path)
        shutil.copy(self.bat_path, self.copy_path)
        pathstr = f'python -m notebook --notebook-dir={self.proj_path}'
        with open(self.copy_path, 'a') as f:
            f.writelines(['\n', pathstr, '\n'])
        command = f'{self.shell_path} && call {self.copy_path}'
        try:
            subprocess.Popen(f'start "" cmd.exe /c {command}', shell=True)
        except Exception as e:
            self.iface.messageBar().pushMessage(f'failed to launch Jupyter: {e}')

    def manageNotebooks(self):
        dialog = ManageNotebooksDialog(self.saved_books, self.proj_path)
        dialog.exec()
        if dialog.success is True:
            self.saved_books = dialog.saved_books
            with open(self.saved_path, 'wb') as f:
                pickle.dump(self.saved_books, f)
