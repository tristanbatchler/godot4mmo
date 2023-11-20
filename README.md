This is a reboot of the original 
[Godot Python MMO](https://tbat.me/projects/godot-python-mmo-tutorial-series) project. This time, 
I will be using everything I have learned, as well as community suggestions, to make a better 
version of the game using Godot 4 for the front end, and more modern Python frameworks for the 
backend.

## Quick Start
1. **Install Python.** Preferably the latest version from the [official website](https://www.python.org/downloads/). Windows users should avoid the Microsoft Store version of Python at all costs.

1. **Clone the repository.**
    ```bash
    git clone https://github.com/tristanbatchler/godot4mmo
    ```
    ```bash
    cd godot4mmo
    ```

1. **Move into the server directory.**
    ```bash
    cd server
    ```

1. **Setup the Python virtual environment for the backend.**
    ```bash
    python -m venv server/venv
    ```

1. **Activate the virtual environment.** If you are using Windows, you will need to run the following command:
    ```powershell
    # Windows ONLY
    server\venv\Scripts\activate
    ```

    For everyone else:
    ```bash
    # Linux / MacOS
    source server/venv/bin/activate
    ```

1. **Install the Python dependencies.**
    ```bash
    pip install -r server/requirements.txt
    ```

1. **Run the server.**
    ```bash
    python -m server
    ```