@echo off
call C:\OSGeo4W\bin\04w_env.bat
@echo off
PATH %OSGEO4W_ROOT%\apps\qgis\python;%PATH%
PATH %OSGEO4W_Root%\apps\qgis\bin;%PATH%
PATH %OSGEO4W_ROOT%\apps\Qt5\bin;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python312;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python312\Scripts;%PATH%
PATH %OSGEO4W_ROOT%\apps\qgis\python\plugins;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python312\DLLs;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python312\Lib;%PATH%
PATH %OSGEO4W_ROOT%\apps\Python312\Lib\site-packages;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python
@echo off
