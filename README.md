# 🔐 AES Encryption & Decryption Tool

A lightweight web application for text encryption and decryption using **AES-128 in CBC mode** with **PKCS7 padding**. Built with Python (Flask) and vanilla HTML/CSS/JS.

---

## ✨ Key Features

* **Dual-Panel UI**: Simultaneous encryption and decryption views (responsive tab layout on mobile).
* **Validation**: Live 16-character length validation for IV and Secret Key.
* **Fixed Spec**: Standardized parameters eliminate common configuration mismatches.
* **Server-side Crypto**: Processing powered by Flask and `cryptography`.
* **One-Click Utilities**: Rapid result copying to clipboard.

---

## ⚙️ Configuration

| Parameter | Value | Parameter | Value |
| --- | --- | --- | --- |
| **Algorithm** | AES | **Key Size** | 128 bits (16 chars) |
| **Mode** | CBC | **IV Size** | 128 bits (16 chars) |
| **Padding** | PKCS7 / PKCS5 | **IO Format** | Hexadecimal |

---

## 📁 Repository Structure

```text
aes-tool/
├── app.py           # Flask backend, routing, and AES logic
├── requirements.txt # Dependencies (Flask, cryptography)
└── templates/
    └── index.html   # Frontend layout and JS handling

```

---

## 🚀 Quickstart

```bash
# Clone repository
git clone https://github.com/usmanfarooq317/aes-tool.git
cd aes-tool

# Setup virtual environment & install dependencies
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Launch application
python app.py

```

App will run on `[http://127.0.0.1:5000](http://127.0.0.1:5000)`.

---

## 👤 Author

**Usman Farooq**

* GitHub: [@usmanfarooq317](https://github.com/usmanfarooq317)
* Email: usmanfarooq317@gmail.com

---

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE).