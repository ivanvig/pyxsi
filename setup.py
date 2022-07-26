import sys, os
import shutil

from pybind11 import get_cmake_dir
# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.0.1"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

xilinx_path = None
while(True):
    print("---> Looking for Vivado install in VIVADO_PATH env var", end=' ')
    if "VIVADO_PATH" in os.environ:
        print("[FOUND]")
        xilinx_path = os.environ["VIVADO_PATH"]
        break
    else:
        print("[NO]")

    print("---> Looking for xelab location", end=' ')
    xelab_path = shutil.which('xelab')
    if xelab_path:
        print("[FOUND]")
        xilinx_path = os.path.abspath(os.path.join(os.path.dirname(xelab_path), '..'))
        break
    else:
        print("[NO]")
        break

if xilinx_path is None:
    print("Error: Could not find Vivado installation path, please set VIVADO_PATH environment variable and try again")
    exit(1)

xilinix_include_path = os.path.join(xilinx_path, 'data/xsim/include')
xilinix_lib_path = os.path.join(xilinx_path, 'lib/lnx64.o')

ext_modules = [
    Pybind11Extension("pyxsi",
        ["src/pybind.cpp", "src/xsi_loader.cpp"],
        define_macros = [('SV_SRC', None)],
        include_dirs=['src', xilinix_include_path],
        extra_compile_args = ['-fPIC', '-shared', '-static-libstdc++'],
        libraries=['fmt', 'dl'],
        runtime_library_dirs=[xilinix_lib_path]
        ),
]

setup(
    name="pyxsi",
    version=__version__,
    long_description="",
    ext_modules=ext_modules,
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
)
