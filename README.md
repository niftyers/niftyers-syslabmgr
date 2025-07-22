# 🛠 Samba Active Directory Management Web Application

**A centralized, web-based administration panel for Samba Active Directory environments.**  
Designed to simplify user, group, and policy management through a secure and user-friendly interface.

---

## 🎯 Purpose

This application provides IT administrators with an intuitive web interface to manage:

-  Users and groups
-  Access control policies
-  Client PC activity
-  Web filtering
-  Communication and session control

Built for LAN environments using Samba-based Active Directory (AD) servers on Linux.

---

## ✅ Features

### 👤 User Management

-  View non-system AD users
-  Add new users with group assignments
-  Reset user passwords
-  Enable / disable users
-  Remove users

### 👥 Group Management

-  View non-system AD groups
-  Create new groups
-  Delete groups
-  Assign/remove users from groups

### 🌐 Web Filtering

-  Manage domain blocklist
-  Define denied domains or keywords
-  (Planned) Integration with Squid/SquidGuard

### 💻 Client Monitoring & Control

-  View online/offline status of domain-joined PCs
-  Remotely shut down or sign off users
-  Monitor user logins and session details

### 📜 Logs & Activity

-  View user login/logout history
-  Track accessed websites (LAN proxy)
-  IP address and machine usage logs

### 💬 Realtime Chat

-  WebSocket-based internal messaging
-  Optional: Admin ↔ Client communication

## ⚙️ Technology Stack

### 🔧 Backend (API)

-  Flask
-  `ldap3` — LDAP access to Samba AD
-  (Planned) SQLite or PostgreSQL for internal state
-  (Planned) WebSocket support for control & chat

### 🎨 Frontend

-  [Vue 3](https://vuejs.org/) with [TypeScript](https://www.typescriptlang.org/)
-  [Tailwind CSS](https://tailwindcss.com/)
-  [Vite](https://vitejs.dev/) for fast dev & builds
-  Pinia (state management)
-  Vue Router (navigation)

---

## 🗂 Project Structure

```
samba-ad-management/
├── web/                        # Vue 3 frontend (SPA)
│   ├── public/                 # Static files (e.g., favicon)
│   ├── src/                    # Vue app source
│   │   ├── assets/             # Images, styles
│   │   ├── components/         # Reusable Vue components
│   │   ├── views/              # Page-level components
│   │   ├── router/             # Vue Router setup
│   │   ├── stores/             # Pinia stores (state management)
│   │   └── main.ts             # App entry point
│   ├── index.html              # Root HTML
│   ├── vite.config.ts          # Vite config (build to ../server)
│   └── tsconfig.json           # TypeScript config
├── server/                     # FastAPI backend
│   ├── app/                    # App package
│   │   ├── api/                # API routes
│   │   │   ├── users.py        # User-related endpoints
│   │   │   ├── groups.py       # Group-related endpoints
│   │   │   ├── auth.py         # Auth endpoints
│   │   │   └── __init__.py
│   │   ├── services/           # Business logic (LDAP, etc.)
│   │   ├── models/             # Pydantic models
│   │   ├── utils/              # Utility functions
│   │   ├── static/             # Vue build assets (dist/assets)
│   │   ├── templates/          # index.html (Vue build)
│   │   └── main.py             # FastAPI app entry point
│   ├── requirements.txt        # Python dependencies
│   └── README.md
├── .gitignore
├── README.md                   # Project description
└── LICENSE
```

The Vue frontend builds into the `server/` directory and is served directly by FastAPI as static files.

## 🚧 Status: Work in Progress

This project is under active development.

### Planned Enhancements:

-  Role-based access (admin, viewer, etc.)
-  Advanced web usage logs via Squid proxy integration
-  Audit logging and system notifications
-  User and group import/export

---

## 💡 Requirements

-  Ubuntu Server with Samba Active Directory (Domain Controller)
-  Python 3.7+ (for Flask backend)
-  Node.js 18+ (for Vue frontend)
-  Domain admin credentials for user/group management
-  Optional: Squid proxy server for web filtering

---

## 🤝 Contributing

Contributions, suggestions, and bug reports are **highly welcome**.  
Feel free to open a pull request or create an issue.

---

## 📄 License

[MIT License](LICENSE)
