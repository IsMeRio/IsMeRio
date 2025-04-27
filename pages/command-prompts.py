# main.py
import streamlit as st
import requests

st.set_page_config(page_title="Command Prompt GUI", layout="wide")

# Styling
st.markdown("""
    <style>
    .terminal {
        background-color: black;
        color: #00FF00;
        font-family: monospace;
        padding: 10px;
        border-radius: 10px;
        height: 400px;
        overflow-y: auto;
        white-space: pre-wrap;
    }
    .directory-info {
        background-color: #222;
        color: #00FF00;
        font-family: monospace;
        padding: 5px 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🖥️ Command Prompt GUI")

# Session State
if "connected" not in st.session_state:
    st.session_state.connected = False
if "terminal_history" not in st.session_state:
    st.session_state.terminal_history = ""
if "current_directory" not in st.session_state:
    st.session_state.current_directory = "Unknown"

# Inputs
ip_address = st.text_input("Enter ngrok Server IP (e.g., http://abc123.ngrok.io) ngrok command to open (ngrok http 8000)")

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Connect"):
        if ip_address:
            try:
                # Try ping server first
                response = requests.post(f"{ip_address}/connect", json={"command": "connect"}, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.connected = True
                    st.session_state.current_directory = data.get("current_directory", "Unknown")
                    st.session_state.terminal_history += "Connected to server.\n"
                    st.success("Connected!")

                else:
                    # If server answers weird, show error
                    st.error("Could not connect to server. Is your rec.py running?")
                    st.session_state.connected = False
                    # Scroll down hint
                    st.markdown('<a href="#download-rec" style="color:red;font-weight:bold;">⬇️ Scroll down to Download Receive.py</a>', unsafe_allow_html=True)

            except Exception as e:
                # If cannot reach server at all
                st.error(f"Connection failed: {e}")
                st.session_state.connected = False
                # Scroll down hint
                st.markdown('<a href="#download-rec" style="color:red;font-weight:bold;">⬇️ Scroll down to Download Receive.py</a>', unsafe_allow_html=True)

        else:
            st.warning("Please enter the server IP.")


with col2:
    if st.button("Disconnect"):
        if ip_address:
            try:
                response = requests.post(f"{ip_address}/connect", json={"command": "disconnect"})
                st.session_state.connected = False
                st.success("Disconnected!")
                st.session_state.terminal_history += "Disconnected from server.\n"
            except Exception as e:
                st.error(f"Disconnection error: {e}")
        else:
            st.warning("Please enter the server IP.")

# Show Current Directory from Server
st.markdown(f'<div class="directory-info">Current Directory: {st.session_state.current_directory}</div>', unsafe_allow_html=True)

# Terminal output
st.markdown(f'<div class="terminal">{st.session_state.terminal_history}</div>', unsafe_allow_html=True)


# Command Input
if st.session_state.connected:
    command = st.text_input("Enter your command")

    if st.button("Execute Command"):
        if command:
            try:
                # Before sending command, check if server is alive
                ping_check = requests.post(f"{ip_address}/connect", json={"command": "connect"}, timeout=5)

                if ping_check.status_code == 200:
                    # If server responds OK, continue normal
                    cmd = command.strip()

                    response = requests.post(f"{ip_address}/command", json={"command": cmd}, timeout=10)
                    data = response.json()

                    output = data.get("output", "No output")
                    new_dir = data.get("current_directory", st.session_state.current_directory)

                    # Update server directory
                    st.session_state.current_directory = new_dir

                    # Handle "call" command differently
                    if cmd.lower() == "call":
                        # Parse output lines
                        st.session_state.terminal_history += f"> {command}\n"
                        items = output.split("\n")
                        for item in items:
                            st.session_state.terminal_history += f"{item}\n"
                        st.rerun()

                    else:
                        # Normal commands
                        st.session_state.terminal_history += f"> {command}\n{output}\n"
                        st.rerun()

                else:
                    st.session_state.connected = False
                    st.error("Server not responding. Disconnected!")
                    st.session_state.terminal_history += "Server not responding. Disconnected.\n"
                    st.rerun()

            except Exception as e:
                # If any error (timeout, disconnect, etc)
                st.session_state.connected = False
                st.error(f"Disconnected: {e}")
                st.session_state.terminal_history += f"Disconnected: {e}\n"
                st.rerun()
else:
    st.warning("Please connect to a server first.")


# Footer
st.markdown("---")
st.markdown('<h3 id="download-rec">Download Receive.py</h3>', unsafe_allow_html=True)
st.link_button("📥 Download Receive.py", "https://github.com/IsMeRio/ismerio-command-prompts-streamlit/blob/ea1bbf9c6760cc6fbe43931a7eb0e9cd2859df43/rec.py")
st.caption("Version 0.2 (Alpha) | Report bugs to ismerio on Discord")

