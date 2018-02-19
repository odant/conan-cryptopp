find_path(CryptoPP_INCLUDE_DIR
    NAMES cryptopp/config.h
    PATHS ${CONAN_INCLUDE_DIRS_CRYPTOPP}
    NO_DEFAULT_PATH
)

find_library(CryptoPP_LIBRARY
    NAMES cryptopp cryptopp-static
    PATHS ${CONAN_LIB_DIRS_CRYPTOPP}
    NO_DEFAULT_PATH
)

if(CryptoPP_INCLUDE_DIR)
    file(STRINGS ${CryptoPP_INCLUDE_DIR}/cryptopp/config.h _config_version REGEX "CRYPTOPP_VERSION")
    string(REGEX MATCH "([0-9])([0-9])([0-9])" _match_version ${_config_version})
    set(CryptoPP_VERSION_MAJOR ${CMAKE_MATCH_1})
    set(CryptoPP_VERSION_MINOR ${CMAKE_MATCH_2})
    set(CryptoPP_VERSION_PATCH ${CMAKE_MATCH_3})
    set(CryptoPP_VERSION_STRING "${CryptoPP_VERSION_MAJOR}.${CryptoPP_VERSION_MINOR}.${CryptoPP_VERSION_PATCH}")
    set(CryptoPP_VERSION_COUNT 3)
endif()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(CryptoPP
    REQUIRED_VARS CryptoPP_INCLUDE_DIR CryptoPP_LIBRARY
    VERSION_VAR CryptoPP_VERSION_STRING
)

if(CryptoPP_FOUND AND NOT TARGET CryptoPP::CryptoPP)
    add_library(CryptoPP::CryptoPP UNKNOWN IMPORTED)
    set_target_properties(CryptoPP::CryptoPP PROPERTIES
        IMPORTED_LOCATION "${CryptoPP_LIBRARY}"
        INTERFACE_INCLUDE_DIRECTORIES "${CryptoPP_INCLUDE_DIR}"
    )
    
    mark_as_advanced(CryptoPP_INCLUDE_DIR CryptoPP_LIBRARY)
    set(CryptoPP_INCLUDE_DIRS ${CryptoPP_INCLUDE_DIR})
    set(CryptoPP_LIBRARIES ${CryptoPP_LIBRARY})
endif()
