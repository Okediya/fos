# fos (freedom of speech)
A peer-to-peer chat app using WebRTC and a Python signaling server.

## Setup
1. Install Python 3.7+ and `aiohttp`: `pip install aiohttp`
2. Run the signaling server: `python server.py`
3. Serve the frontend: `python -m http.server 8000`
4. Open `http://localhost:8000` in two Chrome tabs.
5. Enter peer’s client ID to connect and chat.