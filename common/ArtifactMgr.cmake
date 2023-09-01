cmake_minimum_required(VERSION 3.14)

# Load the system's python interpretator.
find_package(PythonInterp REQUIRED)

# CMake functions don't know which file they are defined in so before a function can be called store where this file is
set(aftifact_current_list_dir ${CMAKE_CURRENT_LIST_DIR} CACHE INTERNAL "")

#    upload_on_install( TARGET <target>
#                       UPLOAD_PATH <group-id>
#                       VERSION <version>
#
# 
function(upload_on_install)
    set(one_value_keywords TARGET UPLOAD_PATH VERSION)
    cmake_parse_arguments(ARG "" "${one_value_keywords}" "" ${ARGN})

    # Install artifacts to known staging area
    set(staging_area ${CMAKE_BINARY_DIR}/deploy/${ARG_TARGET})
    INSTALL(TARGETS ${ARG_TARGET}
            LIBRARY DESTINATION ${staging_area}/lib
            PUBLIC_HEADER DESTINATION ${staging_area}/include
    )
    # perform upload after install
    INSTALL(CODE "execute_process( 
        COMMAND 
            ${PYTHON_EXECUTABLE} \"${aftifact_current_list_dir}/artifact_upload.py\"
                \"${ARG_TARGET}\"
                \"${staging_area}\"
                \"${ARG_UPLOAD_PATH}\"
                \"${ARG_VERSION}\"
        )"
    )
endfunction()

#
#    download_artifact( <target-name>
#                  REMOTE_PATH <path>
#                  VERSION <version>
#
#
function(download_artifact TARGET)
    set(one_value_keywords TARGET REMOTE_PATH VERSION )
    cmake_parse_arguments(ARG "" "${one_value_keywords}" "" ${ARGN})

    # Extract into the staging area
    set(staging_area ${CMAKE_BINARY_DIR}/deploy/${TARGET})
    execute_process(
        COMMAND
            ${PYTHON_EXECUTABLE} "${aftifact_current_list_dir}/artifact_download.py"
                ${TARGET}
                ${ARG_REMOTE_PATH}
                ${ARG_VERSION}
                ${staging_area}
        RESULT_VARIABLE ret
    )
    if(ret AND NOT ret EQUAL "0")
        message(FATAL_ERROR "artifact download failed")
    endif()

    # Link library
    add_library (${TARGET} SHARED IMPORTED)
    file(GLOB library_files "${staging_area}/lib/*.so")
    set_target_properties(${TARGET} PROPERTIES IMPORTED_LOCATION "${library_files}")
    target_include_directories(${TARGET} INTERFACE "${staging_area}/include")
endfunction()