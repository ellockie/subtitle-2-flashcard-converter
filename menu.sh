#!/bin/sh
# v. 0.1

# Copied from:  ~/Dropbox/____Scripts/___Python/__File_folder_operations/Project_menu

set -e  # Exit immediately if a command exits with a non-zero status.

if [ -z "$VIRTUAL_ENV_DIR" ]; then
    echo "Error: VIRTUAL_ENV_DIR environment variable is not set."
    exit 1
fi

# Check if the .project-name file exists and is readable
if [ ! -r .project-name ]; then
    echo "Error: .project-name file not found or not readable."
    exit 1
fi

# Check if the expected Python version is installed
if ! pyenv versions | grep -q "$python_version"; then
    echo "Error: Python $python_version is not installed. Please install it using pyenv."
    exit 1
fi

# Check if the .project-main-filename file exists and is readable
if [ ! -r .project-main-filename ]; then
    echo "Error: .project-main-filename file not found or not readable."
    exit 1
fi

# Read the project name from the .project-name file
project_name=$(cat .project-name)
venv_dir="$VIRTUAL_ENV_DIR/$project_name"
python_version=$(cat .python-version)
main_filename=$(cat .project-main-filename)
activate_path="$venv_dir/bin/activate"


setup_project() {
    # PYENV environment
    pyenv local "$python_version"  # set the python version for the project
    python -m venv "$venv_dir"  # venv will use the specified version

    if [ -d "$venv_dir" ]; then
        echo "Virtual environment, $venv_dir, already exists."
    else
        python3 -m venv "$venv_dir"
        echo "Virtual environment created: $venv_dir"
    fi

    source "$activate_path"
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    echo "Project setup / updated successfully."
}

activate_project() {
    # THIS SCRIPT ALSO NEEDS TO BE SOURCED! ( BUT IT CRASHES! )
    # source menu.sh
    # or
    # . menu.sh

    # This is a command built into bash and some other shells that automatically export any subsequently defined variables to the environment of child processes. Here, -a is a flag that stands for "allexport".
    # set -a

    # source is a bash shell built-in command that executes the content of the file passed as argument, in the current shell. .env is commonly used to hold a list of environment variables to be used by an application, with each line in the file being a key value pair in the form KEY=VALUE.
    # The source .env command reads the file named .env in the current directory and executes the commands in the current shell environment. Because set -a was called earlier, all variables defined in the .env file will be exported as environment variables, not just defined as shell variables.
    # You need to source the script instead of executing it. Sourcing runs the script within your current shell session, allowing any environment changes to persist after the script finishes.

    source "$activate_path"
    echo "Virtual environment activated: $venv_dir"
}

run_project() {
    source "$activate_path"
    python "$main_filename"
    deactivate
}



# Menu for user to choose which function to run
echo "Please choose an option:"
echo "1) Setup Project"
echo "2) Activate Project - THIS SCRIPT ALSO NEEDS TO BE SOURCED! ( but it crashes! )"
echo "3) Run Project"
echo "4) Exit"

printf "Enter choice [1-4]: : "
read choice < /dev/tty

case $choice in
    1)
        setup_project
        ;;
    2)
        activate_project
        ;;
    3)
        run_project
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
