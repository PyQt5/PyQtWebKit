#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Qt5::WebKit" for configuration "Release"
set_property(TARGET Qt5::WebKit APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Qt5::WebKit PROPERTIES
  IMPORTED_IMPLIB_RELEASE "${_IMPORT_PREFIX}/lib/Qt5WebKit.lib"
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Qt5::Quick;Qt5::WebChannel;Qt5::Positioning"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/bin/Qt5WebKit.dll"
  )

list(APPEND _IMPORT_CHECK_TARGETS Qt5::WebKit )
list(APPEND _IMPORT_CHECK_FILES_FOR_Qt5::WebKit "${_IMPORT_PREFIX}/lib/Qt5WebKit.lib" "${_IMPORT_PREFIX}/bin/Qt5WebKit.dll" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
