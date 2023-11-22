# Godot 4 MMO Project Reboot

Welcome to the reboot of the [Godot Python MMO](https://tbat.me/projects/godot-python-mmo-tutorial-series) project! This enhanced version aims to build upon the original project, incorporating valuable community input and the latest technological advancements. The game is now powered by Godot 4 for the frontend and a modern Python framework for the backend, promising an even more robust and engaging gaming experience.

## Server Quick Start Guide

### 1. Install Python
> **Recommended:** Download the latest version from the [official Python website](https://www.python.org/downloads/)

> *Note for Windows Users:* avoid the Microsoft Store version of Python

### 2. Clone the Repository
```bash
git clone https://github.com/tristanbatchler/godot4mmo
```

### 3. Navigate to the Server Directory
```bash
cd godot4mmo/server
```

### 4. Setup the Python Virtual Environment**
```bash
python -m venv server/venv
```

### 5. Activate the Virtual Environment
* **Windows users:**
    ```powershell
    server\venv\Scripts\activate
    ```

* **Everyone else:**
    ```bash
    source server/venv/bin/activate
    ```

### 6. Install the Python Dependencies
```bash
pip install -r server/requirements.txt
```

### 7. Generate the Packet Definitions 
> For more information, see the [shared README](shared/README.md).
```bash
protoc -I="shared" --python_out="server/net" --mypy_out="server/net" "shared/packets.proto"
```

### 8. Run the Server
```bash
python -m server
```

## Client Quick Start
### 1. Install Godot 4
> Download the latest version from the [official website](https://godotengine.org/download)

### 2. Install the Godobuf Plugin 
> Instructions on the [Godobuf repository](https://github.com/oniksan/godobuf)

### 3. Generate the Packet Definitions
> For more information, see the [shared README](shared/README.md)

1. Open the project in Godot.
1. Open the Godobuf tab. Note this tab will only appear if you have installed the Godobuf plugin. It may be hidden because it is the last tab.
    ![Godobuf tab](https://github.com/oniksan/godobuf/raw/master/readme-images/7.png)
1. Choose the "Input protobuf file" to be the `shared/packets.proto` file.
1. Choose the "Output GDScript file" to be `client/packets.gd`.
1. Click "Compile"

### 4. Run the Game
> Press the play button in the top right corner of the Godot editor

## To Add a New Packet
To add a new packet, there are a few places you need to make changes:
1. Add the packet definition to `shared/packets.proto`
    > *Note:* all packets must have at least one field, even if it is a dummy field
1. Generate the packet definitions for the server and client
    * For the server: `protoc -I="shared" --python_out="server/net" --mypy_out="server/net" "shared/packets.proto"`
    * For the client: click the "Compile" button in the Godobuf tab
1. (Optional, but recommended) Add a helper function to `server/net/__init__.py` to allow for easy creation of the packet
1. Add the default packet handler to the protocol state abstract class in `server/protocol/states/protocol_state.py`
1. Implement any specific packet handling in whichever protocol state is appropriate, e.g. `server/protocol/states/entry.py`, etc.

## Todo
* [ ] Add helper functions for packet creation client-side
* [ ] Handle packets that have no fields (e.g. OK packet)