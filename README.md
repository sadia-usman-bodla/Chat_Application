# 🗨️ Advanced Chat Application

## 📘 Description
This is a real-time chat application built using **Flask**, **Flask-SocketIO**, and a simple **HTML/JavaScript client**.  
Users can join chat rooms, send and receive messages instantly, and view previous chat history.

---

## 🧩 Features
- Real-time messaging using **Socket.IO**
- Multiple chat rooms support
- Message history (stored in SQLite)
- User nickname selection
- System notifications (join/leave messages)
- Simple, clean browser-based chat interface

---

## 📁 Project Structure
```
Chat_Application_Advance_App/
│
├── server.py              # Flask + Socket.IO backend
├── chat_client.html       # Frontend client interface
├── chat.db                # SQLite database (auto-created)
└── uploads/               # Folder for media uploads (optional)
```

---

## ⚙️ Installation Steps

### 1. Install dependencies
Open PowerShell or Command Prompt in the project folder and run:
```bash
pip install flask flask-socketio flask-cors flask_sqlalchemy flask_jwt_extended eventlet
```

---

### 2. Run the server
```bash
python server.py
```
Expected output:
```
Server running on http://0.0.0.0:5000
```

---

### 3. Open the chat client
1. Open the file `chat_client.html` in your browser (Chrome, Edge, Firefox, etc.)  
2. Enter your **Username** and **Room name**  
3. Click **Join**  
4. Type messages and press **Send**

💡 Open multiple browser tabs or windows to simulate multiple users chatting in the same room.

---

## 🧠 Example Usage
1. User 1:
   - Username: `sadia`
   - Room: `main`
   - Message: `Hi everyone!`
2. User 2:
   - Username: `usman`
   - Room: `main`
   - Message: `Hello Sadia!`

Both users instantly see each other's messages.

---

## 🔒 Optional Enhancements
You can expand this project further by adding:
- 🔐 User authentication (login/signup)
- 🖼️ Multimedia sharing (images/videos)
- 💬 Emoji picker integration
- 🔔 Desktop or sound notifications
- 🔏 End-to-end encryption (AES/RSA)
- 🧠 AI chatbot integration using OpenAI API

---

## 🧰 Troubleshooting

| Issue | Cause | Fix |
|-------|--------|------|
| `WinError 10048` | Port already in use | Change port in `server.py` (e.g. 5050) |
| Messages duplicate | Join event firing twice | Use the fixed JS client with `joined` flag |
| No response in browser | Check if Flask server is running properly |
| “ModuleNotFoundError” | Missing library | Run `pip install` for the missing module |

---

## 👩‍💻 Author
**Sadia Usman**  
Simple real-time chat project using Flask + Socket.IO  
Built for learning networking, sockets, and real-time communication in Python.
