
import datetime
import os
import platform
import shutil
import sys

DIVIDER = "=" * 70  # A string divider for cleaner output formatting
OUTPUT_FILENAME = "util_about.txt"  # File name for saving the info

build_date, compiler = platform.python_build()
implementation = platform.python_implementation()
architecture = platform.architecture()[0]
user_home = os.path.expanduser("~")


def get_terminal_info():
    """Determine the terminal and environment."""
    term_program = os.environ.get("TERM_PROGRAM", "")
    term_program_version = os.environ.get("TERM_PROGRAM_VERSION", "").lower()

    if term_program == "vscode":
        environment = "VS Code"
        if "powershell" in term_program_version:
            current_shell = "powershell"
        else:
            current_shell = (
                os.environ.get("SHELL", os.environ.get("ComSpec", ""))
                .split(os.sep)[-1]
                .lower()
            )
    else:
        environment = "Native Terminal"
        current_shell = (
            os.environ.get("SHELL", os.environ.get("ComSpec", ""))
            .split(os.sep)[-1]
            .lower()
        )

    return environment, current_shell


def get_source_directory_path():
   
    dir = os.path.dirname(os.path.abspath(__file__))
    return dir


def is_git_in_path():

    return shutil.which("git") is not None


def get_preferred_command():

    if os.name == "nt":  # Checks if the OS is Windows.
        return "python"
    return "python3"


def is_preferred_command_available():

    preferred_command = get_preferred_command()
    is_available = shutil.which(preferred_command) is not None
    return is_available


def print_info_to_file(filename, content):

    with open(filename, "w") as f:
        f.write(content)


def get_header(fn):

    environment, current_shell = get_terminal_info()

    return f"""
{DIVIDER}
{DIVIDER}

 Welcome to the NW Python Debugging Information Utility!
 Date and Time: {datetime.date.today()} at {datetime.datetime.now().strftime("%I:%M %p")}
 Operating System: {os.name} {platform.system()} {platform.release()}
 System Architecture: {architecture}
 Number of CPUs: {os.cpu_count()}
 Machine Type: {platform.machine()}
 Python Version: {platform.python_version()}
 Python Build Date and Compiler: {build_date} with {compiler}
 Python Implementation: {implementation}
 Active pip environment:   {os.environ.get('PIP_DEFAULT_ENV', 'None')}
 Active conda environment: {os.environ.get('PIP_DEFAULT_ENV', 'None')}
 Path to Interpreter:         {sys.executable}
 Path to virtual environment: {sys.prefix}
 Current Working Directory:   {os.getcwd()}
 Path to source directory:    {get_source_directory_path()}
 Path to script file:         {fn}
 User's Home Directory:       {user_home}
 Terminal Environment:        {environment}
 Terminal Type:               {current_shell}
 Preferred command:           {get_preferred_command()}
 Is {get_preferred_command()} available in PATH:   {is_preferred_command_available()}
 Is git available in PATH:      {is_git_in_path()} 
{DIVIDER}
{DIVIDER}

if __name__ == "__main__":
    debug_info = get_header(__file__)
    print(debug_info)

    print_info_to_file(OUTPUT_FILENAME, debug_info)


"""

import datetime
import logging
import os
import sys


OUTPUT_FILENAME = "aboutenv.txt"
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.FileHandler(OUTPUT_FILENAME, mode="w"), logging.StreamHandler()],
)


DIVIDER = "=" * 70  # A string divider for cleaner output formatting
CREATE_COMMAND = "python -m venv .venv"
ACTIVATE_COMMAND_WINDOWS = ".venv\\Scripts\\activate"
ACTIVATE_COMMAND_MAC_LINUX = "source .venv/bin/activate"
UPGRADE_COMMAND = "python -m pip install --upgrade pip"
INSTALL_COMMAND = "python -m pip install"
SUCCESS_MESSAGE = "All checks passed successfully! Your environment is set up correctly.\nIf it asks you to upgrade pip, please do so using the suggested command."



def get_activate_command():
    """Returns the command to activate the virtual environment."""
    if sys.platform == "win32":
        return ACTIVATE_COMMAND_WINDOWS
    else:
        return ACTIVATE_COMMAND_MAC_LINUX


def check_for_dotvenv_folder():
    """Checks if the .venv folder exists."""
    if os.path.exists(".venv"):
        error_code = 0
        message = "YAY! .venv directory exists."
    else:
        error_code = 1
        message = f"ERROR: Missing .venv directory. Create it (may take a while) using: {CREATE_COMMAND}"
    return error_code, message


def check_dotvenv_is_active():
    """Checks if the .venv virtual environment is active."""
    venv_path = os.environ.get("VIRTUAL_ENV")

    if venv_path and ".venv" in venv_path:
        error_code = 0
        message = "YAY! The .venv virtual environment is active."
    else:
        ACTIVATE_COMMAND = get_activate_command()
        error_code = 1
        message = (
            f"ERROR: Activate the .venv virtual environment using: {ACTIVATE_COMMAND}"
        )
    return error_code, message


def get_search_path_string():
    paths = "\n".join(sys.path)
    return f"""
Python's package search paths:
{"-" * 40}
{paths}
{"-" * 40}
"""


def read_dependencies():
    """Read dependencies from requirements.txt and return a list of package names."""
    dependency_list = []
    if not os.path.exists("requirements.txt"):
        logging.warning("No requirements.txt file found.")
        return dependency_list

    with open("requirements.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            package_name = line.split("==")[0].strip()
            dependency_list.append(package_name)

    return dependency_list


def check_dependencies_installed_in_dotvenv():
    """Checks if dependencies are installed in the virtual environment."""
    logging.debug(get_search_path_string())

    DEPENDENCIES_LIST = read_dependencies()

    for dependency in DEPENDENCIES_LIST:
        try:
            __import__(dependency)
        except ImportError as e:
            logging.error(e)
            message = f"ERROR: {dependency} is not installed in .venv. Install it by running: {INSTALL_COMMAND} {dependency}"
            return (1, message)

    message = "YAY! All dependencies are installed in the .venv."
    return 0, message


def log_with_divider(message):
    """Logs a message and the DIVIDER."""
    logging.info(message)
    logging.info(DIVIDER)


def verify_environment():
    """Verify the environment step by step."""

    log_with_divider(f"{DIVIDER}")

    checks = [
        check_for_dotvenv_folder,
        check_dotvenv_is_active,
        check_dependencies_installed_in_dotvenv,
    ]

    for check in checks:
        error_code, message = check()
        log_with_divider(message)

        if error_code:
            sys.exit()

    log_with_divider(f"\n{SUCCESS_MESSAGE}\n")


if __name__ == "__main__":
    logging.info(DIVIDER)
    logging.info("Welcome to the Python Debugging Information Utility ABOUTENV.PY")
    logging.info(
        f"Date and Time: {datetime.date.today()} at {datetime.datetime.now().strftime('%I:%M %p')}"
    )
    verify_environment()


import logging
import pathlib
import platform
import sys
import os
import datetime


DIVIDER = "=" * 50 


def setup_logger(current_file):
    logs_dir = pathlib.Path("logs")
    logs_dir.mkdir(exist_ok=True)

    module_name = pathlib.Path(current_file).stem
    log_file_name = logs_dir.joinpath(module_name + ".log")

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)  # Set the root logger level.

    file_handler = logging.FileHandler(log_file_name, "w")
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s.%(name)s.%(levelname)s %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    python_version_string = platform.python_version()
    today = datetime.date.today()

    logger.info(f"{DIVIDER}")
    logger.info(f"Today is {today} at {datetime.datetime.now().strftime('%I:%M %p')}")
    logger.info(f"Running on: {os.name} {platform.system()} {platform.release()}")
    logger.info(f"Python version:  {python_version_string}")
    logger.info(f"Python path: {sys.prefix}")
    logger.info(f"Working dir: {os.getcwd()}")
    logger.info(f"{DIVIDER}")

    return logger, log_file_name

