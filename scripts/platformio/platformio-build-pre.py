# Copyright 2019-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import distutils.sysconfig as sysconfig
from distutils.sysconfig import get_python_inc

from SCons.Script import AlwaysBuild


Import("env")


def generate_cmake_list(builders):

    zephyr_setup_dir = os.path.join(env.subst("$PROJECT_DIR"), "zephyr")
    cmake_temp_dir = os.path.join(env.subst("$BUILD_DIR"), "builder_config")
    try:
        shutil.rmtree(cmake_temp_dir)
    except Exception:
        pass
    shutil.copytree(zephyr_setup_dir, cmake_temp_dir)

    with open(os.path.join(cmake_temp_dir, "CMakeLists.txt"), "w") as cmakeList:

        with open(os.path.join(zephyr_setup_dir, "CMakeLists.txt"), "r") as user_cmake:
            copy_lines = user_cmake.readlines()
            written = 0
            for index, line in enumerate(copy_lines):
                if line.startswith("target_sources(app PRIVATE ../src/main.cpp)"):
                    line = line.replace("../src", "../../../../src")
                cmakeList.write(line)
                if "cmake_minimum_required" in line:
                    written = index +1
                    break

            for line in copy_lines[written:]:
                if line.startswith("target_sources(app PRIVATE ../src/main.cpp)"):
                    line = line.replace("../src", "../../../../src")
                cmakeList.write(line)
            cmakeList.write("\n")
        
        dep = []
        for builder in env["PIOBUILDFILES"]:
            try:
                builder[0]
            except Exception:
                builder = [builder]
            for node in builder:
                if not str(node).endswith("main.o"):
                    dep.append(node)
                    cmakeList.write(f'target_link_libraries(app PUBLIC {str(node)})')
                    cmakeList.write('\n')

        includepaths = set()

        for library in env["__PIO_LIB_BUILDERS"]:
            for path in library.get_include_dirs():
                includepaths.add(path)
        
        cmakeList.writelines(['include_directories(%s)\n'% str(include) for include in includepaths])
        cmakeList.write('\n')
    return dep
    
def ZephyrBuildProgram(env):
    env["LDSCRIPT_PATH"] = None
    env.ProcessProgramDeps()
    env.ProcessProjectDeps()

    # append into the beginning a main LD script
    env.Prepend(LINKFLAGS=["-T", "$LDSCRIPT_PATH"])

    # enable "cyclic reference" for linker
    if env.get("LIBS") and env.GetCompilerType() == "gcc":
        env.Prepend(_LIBFLAGS="-Wl,--start-group ")
        env.Append(_LIBFLAGS=" -Wl,--end-group")

    workingdir = os.getcwd()
    complieLibCmd = [
        "cd /run/media/kappy/d/programms/zephyr/testproject/zephyr &&"
        "west",
        "build",
        "-b",
        env["__ZEPHYR_BOARD"],
        "-d",
        os.path.join(env.subst("$BUILD_DIR"), "builder_output "),
        os.path.join(env.subst("$BUILD_DIR"), "builder_config"),
        "&&",
        "cd",
        workingdir,

    ]
    
    print(" ".join(complieLibCmd))
    compileDast = env.Command(
        [os.path.join("$BUILD_DIR", "builder_output", "zephyr", "zephyr.elf")],
        [],
        env.VerboseAction(" ".join(complieLibCmd), "Generating file $TARGET")
    )
    deps = generate_cmake_list(env["LIBS"])
    env.Depends(compileDast, deps)
    program = compileDast

    env.Replace(PIOMAINPROG=program)

    AlwaysBuild(
        env.Alias(
            "checkprogsize",
            os.path.join("$BUILD_DIR", "builder_output", "zephyr", "zephyr.elf"),
            env.VerboseAction(env.CheckUploadSize, "Checking size $PIOMAINPROG"),
        )
    )
    [print(str(f)) for f in env["PIOBUILDFILES"]]
    return program

env.AddMethod(ZephyrBuildProgram, "BuildProgram")
