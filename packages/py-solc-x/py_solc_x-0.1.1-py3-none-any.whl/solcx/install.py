"""
Install solc
"""
from io import BytesIO
import os
import requests
import shutil
import stat
import subprocess
import sys
import tarfile
import zipfile

DOWNLOAD_BASE = "https://github.com/ethereum/solidity/releases/download/{}/{}"
API = "https://api.github.com/repos/ethereum/solidity/releases/latest"

sep = "\\" if sys.platform == "win32" else "/"
solc_version = None


def get_solc_folder():
    return __file__[:__file__.rindex(sep)] + sep + "bin" + sep


def get_executable(version = None):
    if not version:
        version = solc_version
    solc_bin = "{}solc-{}".format(get_solc_folder(), version)
    if sys.platform == "win32":
        return solc_bin + sep + "solc.exe"
    return solc_bin


def set_solc_version(version = None):
    version = _check_version(version)
    if not os.path.exists(get_executable(version)):
        install_solc(version)
    global solc_version
    solc_version = version


def get_installed_solc_versions():
    return sorted([i[5:] for i in os.listdir(get_solc_folder()) if 'solc-v' in i])


def install_solc(version = None):
    version = _check_version(version)
    if sys.platform.startswith('linux'):
        _install_solc_linux(version)
    elif sys.platform == 'darwin':
        _install_solc_osx(version)
    elif sys.platform == 'win32':
        _install_solc_windows(version)
    else:
        raise KeyError("Unknown platform: {}".format(sys.platform))
    binary_path = get_executable(version)
    _check_subprocess_call(
        [binary_path, '--version'],
        message="Checking installed executable version @ {}".format(binary_path)
    )
    print("solc {} successfully installed at: {}".format(version, binary_path))


def _check_version(version):
    if not version:
        return requests.get(API).json()['tag_name']
    version = "v0." + version.lstrip("v0.")
    if version.count('.') != 2:
        raise ValueError("solc version must be in the format v0.x.x")
    v = [int(i) for i in version[1:].split('.')]
    if v[1] < 4 or (v[1] == 4 and v[2] < 11):
        raise ValueError("py-solc-x does not support solc versions <0.4.11")
    return version


def _check_subprocess_call(command, message=None, verbose=True, **proc_kwargs):
    if message:
        print(message)
    print("Executing: {0}".format(" ".join(command)))

    return subprocess.check_call(
        command,
        stderr=subprocess.STDOUT if verbose else subprocess.DEVNULL,
        **proc_kwargs
    )


def _chmod_plus_x(executable_path):
    current_st = os.stat(executable_path)
    os.chmod(executable_path, current_st.st_mode | stat.S_IEXEC)


def _wget(url, path):
    try:
        _check_subprocess_call(
            ["wget", url, "-O", path],
            "Downloading solc from {}".format(url)
        )
    except subprocess.CalledProcessError:
        if os.path.exists(path):
            os.remove(path)
        raise


def _install_solc_linux(version):
    download = DOWNLOAD_BASE.format(version, "solc-static-linux")
    binary_path = get_solc_folder()+"solc-{}".format(version)
    if os.path.exists(binary_path):
        print("solc {} already installed at: {}".format(version, binary_path))
        return
    _wget(download, binary_path)
    _chmod_plus_x(binary_path)


def _install_solc_windows(version):
    download = DOWNLOAD_BASE.format(version, "solidity-windows.zip")
    zip_path = get_solc_folder() + 'solc_{}.zip'.format(version[1:])
    install_folder = get_solc_folder()+"solc-{}".format(version)
    if os.path.exists(install_folder):
        print("solc {} already installed at: {}".format(version, install_folder))
        return
    print("Downloading solc {} from {}".format(version, download))
    request = requests.get(download)
    with zipfile.ZipFile(BytesIO(request.content)) as zf:
        zf.extractall(install_folder)


def _install_solc_osx(version):
    tar_path = get_solc_folder() + "solc-{}.tar.gz".format(version)
    source_folder = get_solc_folder() + "solidity_{}".format(version[1:])
    download = DOWNLOAD_BASE.format(version, "solidity_{}.tar.gz".format(version[1:]))
    binary_path = get_solc_folder()+"solc-{}".format(version)
    
    if os.path.exists(binary_path):
        print("solc {} already installed at: {}".format(version, binary_path))
        return

    _wget(download, tar_path)

    with tarfile.open(tar_path, "r") as tar:
        tar.extractall(get_solc_folder())
    os.remove(tar_path)

    _check_subprocess_call(
        ["sh", source_folder+'/scripts/install_deps.sh'],
        message="Running dependency installation script `install_deps.sh` @ {}".format(tar_path)
    )

    original_path = os.getcwd()
    os.mkdir(source_folder+'/build') 
    os.chdir(source_folder+'/build')
    try:
        for cmd in (["cmake", ".."], ["make"]):
            _check_subprocess_call(cmd, message="Running {}".format(cmd[0]))
        os.chdir(original_path)
        os.rename(source_folder+'/build/solc/solc', binary_path)
    except subprocess.CalledProcessError as e:
        raise OSError(
            "{} returned non-zero exit status {}".format(cmd[0], e.returncode) +
            " while attempting to build solc from the source. This is likely " +
            "due to a missing or incorrect version of an external dependency."
        )
    finally:
        os.chdir(original_path)
        shutil.rmtree(source_folder)

    _chmod_plus_x(binary_path)


if __name__ == "__main__":
    try:
        version = sys.argv[1]
    except IndexError:
        print("Invocation error.  Should be invoked as `./install_solc.py <release-tag>`")
        sys.exit(1)

    install_solc(version)
