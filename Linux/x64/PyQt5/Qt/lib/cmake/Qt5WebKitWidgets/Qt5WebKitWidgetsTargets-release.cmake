#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt5::WebKitWidgets" for configuration "Release"
set_property(TARGET Qt5::WebKitWidgets APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Qt5::WebKitWidgets PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Qt5::PrintSupport"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libQt5WebKitWidgets.so.5.212.0"
  IMPORTED_SONAME_RELEASE "libQt5WebKitWidgets.so.5"
  )

list(APPEND _IMPORT_CHECK_TARGETS Qt5::WebKitWidgets )
list(APPEND _IMPORT_CHECK_FILES_FOR_Qt5::WebKitWidgets "${_IMPORT_PREFIX}/lib/libQt5WebKitWidgets.so.5.212.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
