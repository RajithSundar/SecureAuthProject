# 🔐 Secure Authentication System

A modern, secure authentication system featuring **Multi-Factor Authentication (MFA)** with a stunning **Windows 11-inspired glass UI**. Built with C++ backend for security and Python frontend for a premium user experience.

![Windows 11 Design](https://img.shields.io/badge/Design-Windows%2011-0078D4?style=flat-square)
![C++](https://img.shields.io/badge/Backend-C%2B%2B-00599C?style=flat-square&logo=cplusplus)
![Python](https://img.shields.io/badge/Frontend-Python-3776AB?style=flat-square&logo=python)
![Security](https://img.shields.io/badge/Security-MFA%20Enabled-success?style=flat-square)

## ✨ Features

### 🎨 Modern UI/UX
- **Glass Effect Panels** - Frosted acrylic design with Windows 11 aesthetics
- **Animated Gradient Background** - Smooth, multi-layered blue gradient
- **Real-time Password Strength Meter** - 4-level visual indicator with color coding
- **TOTP Countdown Timer** - Circular progress ring showing code expiry (strict 30-second validation)
- **Login Attempt Tracker** - Visual security warnings and account lockout (max 5 attempts)
- **Smooth Animations** - Micro-interactions and hover effects throughout

### 🔒 Security Features
- **Two-Factor Authentication** - Time-based One-Time Passwords (TOTP)
- **Buffer Overflow Protection** - Secure string handling in C++
- **Password Hashing** - DJB2 algorithm implementation
- **Account Lockout** - Automatic lock after 5 failed attempts
- **Input Validation** - Real-time validation with user feedback
- **Strict TOTP Validation** - 30-second window, old codes expire immediately

### ⌨️ Enhanced UX
- **Keyboard Shortcuts** - Press `Enter` to submit forms
- **Auto-Focus** - Automatic focus on input fields
- **Copy to Clipboard** - One-click TOTP copy with visual confirmation
- **Smart Validation** - Empty field detection, format enforcement
- **Status Indicators** - Color-coded system messages with icons

## 🚀 Quick Start

### Prerequisites
- **Python 3.x** installed
- **g++** compiler (MinGW on Windows, GCC on Linux/Mac)
- **tkinter** (usually comes with Python)

### Installation & Running

```bash
# Clone the repository
git clone https://github.com/RajithSundar/SecureAuthProject.git
cd SecureAuthProject

# Build and run (compiles C++ library and launches GUI)
python build.py
```

That's it! The system will:
1. Compile the C++ backend library
2. Launch the modern glass UI
3. Display the authentication screens

## 🔑 Test Credentials

| Field | Value |
|-------|-------|
| **Username** | `admin` |
| **Password** | `admin123` |
| **TOTP Code** | See yellow banner in app (changes every 30 seconds) |

### Password Strength Testing
Try different passwords to see the strength meter in action:
- `weak` → 🔴 Red (Weak)
- `Admin123` → 🟡 Yellow (Good)
- `Admin123!@#` → 🟢 Green (Strong)

## 🎯 How to Use

### Step 1: Login Screen
1. Enter username: `admin`
2. Enter password: `admin123`
3. Watch the password strength meter update in real-time
4. Press `Enter` or click **Sign In →**

### Step 2: MFA Verification
1. See the TOTP countdown timer (shows time remaining)
2. Copy the 6-digit code from the yellow banner
3. Or click **📋 Copy Demo TOTP** button (displays code in popup)
4. Enter the code in the verification field
5. Press `Enter` or click **Verify Code ✓**

### Step 3: Success!
✓ Authentication Complete - Access Granted!

## 📂 Project Structure

```
SecureAuthProject/
│
├── auth_core.cpp              # C++ security backend
├── main_gui.py                # Python GUI with glass effects
├── build.py                   # Automated build script
├── .gitignore                 # Git ignore file
├── TECHNICAL_DOCUMENTATION.txt # Comprehensive docs
├── ALL_SOURCE_CODE.txt        # Complete source listing
└── README.md                  # This file
```

## 🎨 UI Components

### Modern Glass Panel
- Semi-transparent backgrounds
- Subtle borders with highlights
- Layered depth perception

### Custom Widgets
- **ModernEntry** - Glass-styled input fields with focus effects
- **ModernButton** - Hover and active states with glass highlights
- **PasswordStrengthMeter** - 4-bar visual indicator
- **CircularProgress** - Animated countdown timer

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Submit current form |
| `Tab` | Navigate between fields |

## 🔧 Technical Details

### Backend (C++)
- **DJB2 Hashing** - Password verification
- **TOTP Generation** - 6-digit codes, strict 30-second windows
- **Buffer Protection** - Secure string copy functions
- **Cross-platform** - Compiled as .dll (Windows) or .so (Linux/Mac)

### Frontend (Python)
- **tkinter** - GUI framework
- **ctypes** - C++ library integration
- **Glass Effect** - Simulated with stipple patterns
- **Animations** - Math-based gradient animation
- **Windows 11 Theme** - Segoe UI font, modern colors

### Colors
- **Primary Blue**: `#0078D4` (Windows accent)
- **Background**: `#FAFAFA` (Soft white)
- **Success**: `#107C10` (Green)
- **Warning**: `#FFA500` (Orange)
- **Error**: `#D83B01` (Red)

## 🛡️ Security Notes

> **⚠️ Educational Purpose**: This project is for demonstration and learning. For production use:
> - Replace DJB2 with bcrypt/Argon2
> - Use HMAC-SHA1 for TOTP (RFC 6238)
> - Add persistent rate limiting
> - Implement secure credential storage
> - Use constant-time comparisons

## 📖 Documentation

For detailed technical information, see:
- **TECHNICAL_DOCUMENTATION.txt** - Full system documentation
  - Architecture diagrams
  - Algorithm explanations
  - Security mechanisms
  - UI/UX design details
  - Integration guide

## 🎯 Implemented Features

✅ Modern Windows 11 glass UI  
✅ Animated gradient background  
✅ Real-time password strength meter  
✅ TOTP countdown timer with strict validation  
✅ Login attempt tracking (max 5)  
✅ Copy-to-clipboard with visual confirmation  
✅ Keyboard shortcuts  
✅ Auto-focus inputs  
✅ Enhanced validation  
✅ Color-coded feedback  

## 🔮 Future Enhancements

- [ ] Dark mode toggle
- [ ] QR code for TOTP setup
- [ ] Session management
- [ ] Biometric authentication simulation
- [ ] Multi-language support
- [ ] Export authentication logs

## 👨‍💻 Author

**Rajith Sundar**
- GitHub: [@RajithSundar](https://github.com/RajithSundar)

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🤝 Contributing

This is an educational project, but suggestions and improvements are welcome!

---

**Made with ❤️ using Windows 11 Design Principles**
