import streamlit as st
import os
import requests

st.set_page_config(page_title="Command Prompt GUI", layout="wide")

st.markdown(
    """
    <style>
    .terminal {
        background-color: black;
        color: #00FF00;
        font-family: monospace;
        padding: 10px;
        border-radius: 10px;
        height: 500px;
        overflow-y: scroll;
        white-space: pre-wrap;
    }
    .terminal-input input {
        background-color: black;
        color: #00FF00;
        font-family: monospace;
        border: none;
        width: 100%;
    }
    .directory {
        background-color: #333;
        color: #00FF00;
        font-family: monospace;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🖥️ Ngrok Command Prompt GUI")

# Input for ngrok URL
ngrok_url = st.text_input("Enter Ngrok URL (e.g., http://abc123.ngrok.io)")

# Session states
if "connected" not in st.session_state:
    st.session_state.connected = False

if "terminal_history" not in st.session_state:
    st.session_state.terminal_history = ""

if "current_directory" not in st.session_state:
    st.session_state.current_directory = os.getcwd()  # Start at the current directory

# Buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Connect"):
        if ngrok_url:
            try:
                response = requests.post(f"{ngrok_url}/connect", json={"command": "connect"})
                st.session_state.connected = True
                st.success(f"Connected to {ngrok_url}")
                st.session_state.terminal_history += "Connected to server...\n"
            except Exception as e:
                st.error(f"Error connecting: {e}")
        else:
            st.warning("Please enter a valid Ngrok URL.")

with col2:
    if st.button("Disconnect"):
        if ngrok_url:
            try:
                response = requests.post(f"{ngrok_url}/connect", json={"command": "disconnect"})
                st.session_state.connected = False
                st.success(f"Disconnected from {ngrok_url}")
                st.session_state.terminal_history += "Disconnected from server...\n"
            except Exception as e:
                st.error(f"Error disconnecting: {e}")
        else:
            st.warning("Please enter a valid Ngrok URL.")

with col3:
    if st.button("Refresh"):
        # Just trigger re-rendering, nothing to reset
        st.rerun()

# Show Current Directory
st.markdown(f'<div class="directory">Current Directory: {st.session_state.current_directory}</div>', unsafe_allow_html=True)

# Show Terminal
st.markdown('<div class="terminal">' + st.session_state.terminal_history + '</div>', unsafe_allow_html=True)

# Terminal Input
if st.session_state.connected:
    command = st.text_input("Type your command", key="command_input")

    if st.button("Send Command"):
        if command:
            try:
                # Handle cd command (change directory)
                if command.startswith("cd "):
                    path = command[3:].strip()
                    if path == "" or path == ".":
                        result = f"Changed directory to {st.session_state.current_directory}\n"
                    elif path == "..":
                        # Go up one level in the directory
                        parent_dir = os.path.dirname(st.session_state.current_directory)
                        
                        # If we are at the root, we shouldn't go further up
                        if parent_dir == st.session_state.current_directory:
                            result = f"Already at the root directory: {st.session_state.current_directory}\n"
                        else:
                            st.session_state.current_directory = parent_dir
                            result = f"Changed directory to {st.session_state.current_directory}\n"
                    elif os.path.isdir(path):
                        # Change to a valid directory
                        st.session_state.current_directory = os.path.abspath(path)
                        result = f"Changed directory to {st.session_state.current_directory}\n"
                    else:
                        result = f"Directory {path} does not exist.\n"
                
                # Handle changing drives (for example, C: or D:)
                elif len(command) >= 2 and command[1] == ":" and command[2] == "\\":
                    # Switch to a new drive
                    drive = command[0].upper()  # Just take the first character (drive letter)
                    if os.path.exists(f"{drive}:\\"):
                        st.session_state.current_directory = f"{drive}:\\"
                        result = f"Changed to drive {drive}:\\\n"
                    else:
                        result = f"Drive {drive}: does not exist.\n"
                
                # Handle 'dir' command (list directory contents)
                elif command.strip().lower() == "dir":
                    try:
                        files = os.listdir(st.session_state.current_directory)
                        result = f"Directory of {st.session_state.current_directory}\n\n"
                        for f in files:
                            file_path = os.path.join(st.session_state.current_directory, f)
                            is_dir = "[DIR]" if os.path.isdir(file_path) else ""
                            result += f"{f} {is_dir}\n"
                    except Exception as e:
                        result = f"Error listing directory: {e}\n"

                else:
                    # For other commands (execute normally)
                    response = requests.post(f"{ngrok_url}/command", json={"command": command})
                    result = response.json().get("output", "No output")

                # Update terminal history
                st.session_state.terminal_history += f"> {command}\n{result}\n"
                st.rerun()  # Force refresh after sending command

            except Exception as e:
                st.session_state.terminal_history += f"Error sending command: {e}\n"
                st.rerun()


st.write("use ngrok ip to connect and use command prompts run ngrok commands as ngrok http 8000 and use recive python file to connect")
st.link_button("download recive.py","https://github.com/IsMeRio/ismerio-command-prompts-streamlit/blob/ea1bbf9c6760cc6fbe43931a7eb0e9cd2859df43/rec.py")
st.write("ver 0.1 (Alpha) found bug or error pleass report at ismerio on discord")