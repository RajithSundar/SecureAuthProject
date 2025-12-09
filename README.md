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
- **Sign-Up Flow** - User-friendly registration with QR code setup

### 🗄️ Database & User Management
- **SQLite Database** - Persistent user storage in `users.db`
- **User Registration** - Create new accounts with username and password
- **Per-User TOTP Secrets** - Each user gets unique authenticator secret
- **Password Requirements** - Minimum 3-char username, 6-char password
- **Duplicate Detection** - Prevents duplicate usernames

### 🔒 Security Features
- **Two-Factor Authentication** - Time-based One-Time Passwords (TOTP)
- **Google Authenticator Support** - RFC 6238 compliant TOTP with QR code setup
- **Per-User Secrets** - Unique TOTP secret for each registered user
- **Password Hashing** - SHA-256 for credential storage
- **Production/Demo Modes** - Toggle between Google Auth and visible codes
- **Buffer Overflow Protection** - Secure string handling in C++
- **Account Lockout** - Automatic lock after 5 failed attempts
- **Input Validation** - Real-time validation with user feedback
- **Strict TOTP Verification** - 30-second window with ±1 tolerance

### 📱 Production & Demo Modes

**Production Mode** (Google Authenticator):
- Uses RFC 6238 standard TOTP (`pyotp` library)
- Requires Google Authenticator app on phone
- Secure - codes never displayed on screen
- Professional deployment ready

**Demo Mode** (Visible Codes):
- Uses simplified C++ TOTP algorithm
- Codes displayed on screen (yellow banner)
- Copy-to-clipboard button available
- Perfect for testing and demonstrations

**Switch modes** by editing `config.py`:
```python
PRODUCTION_MODE = True   # Google Authenticator mode
PRODUCTION_MODE = False  # Demo mode (default)
```

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

# Install Python dependencies
pip install qrcode[pil] pyotp

# Build and run (compiles C++ library and launches GUI)
python build.py
# OR run GUI directly (Python-only mode)
python main_gui.py
```

**Note**: The C++ library is now optional - the application works with Python-only authentication using SQLite database.

That's it! The system will:
1. Initialize the SQLite database (`users.db`) if needed
2. Launch the modern glass UI
3. Display the login/sign-up screens

## 📱 Google Authenticator Setup

### Step 1: Download the App
- **iOS**: App Store → "Google Authenticator"
- **Android**: Play Store → "Google Authenticator"
- **Alternatives**: Microsoft Authenticator, Authy, 1Password

### Step 2: Enable Production Mode
Edit `config.py`:
```python
PRODUCTION_MODE = True
```

### Step 3: Scan QR Code
1. Run `python build.py`
2. Click the **"⚙️ Setup Authenticator"** button (blue banner at bottom)
3. A window will pop up showing a QR code
4. Open Google Authenticator app on your phone
5. Tap **+** → **Scan QR code**
6. Point camera at the QR code
7. Account "SecureAuth (admin)" will be added!

### Step 4: Get Your Codes
- Open Google Authenticator app
- Find "SecureAuth (admin)" entry
- You'll see a 6-digit code that changes every 30 seconds
- Use this code for MFA verification!

### Manual Entry Option
If you can't scan the QR code:
- In Google Auth: Tap **+** → **Enter a setup key**
- Account: `admin`
- Key: `JBSWY3DPEHPK3PXP`
- Type: Time based

## 🔑 Getting Started

### First Time Setup - Create an Account

1. **Launch the application**:
   ```bash
   python main_gui.py
   ```

2. **Click "Create Account"** on the login screen

3. **Sign Up**:
   - Enter username (min 3 characters)
   - Enter password (min 6 characters)
   - Watch the password strength meter update

4. **Scan QR Code**:
   - A QR code will appear for Google Authenticator
   - Open Google Authenticator app on your phone
   - Tap **+** → **Scan QR code**
   - Point camera at the QR code on screen
   - Your account is now added!

5. **Login**:
   - Click "Done - Go to Login"
   - Enter your username and password
   - Enter the 6-digit TOTP code from Google Authenticator
   - Success!

### Password Strength Testing
Try different passwords to see the strength meter in action:
- `weak` → 🔴 Red (Weak)
- `Pass123` → 🟡 Yellow (Good)
- `Pass123!@#` → 🟢 Green (Very Strong)

## 🎯 How to Use

### Sign Up Flow

**Step 1: Create Account**
1. Click **"Create Account"** on login screen
2. Enter desired username (min 3 characters)
3. Enter password (min 6 characters)
4. Watch password strength meter update in real-time
5. Click **"Sign Up"**

**Step 2: Setup Google Authenticator**
1. QR code screen appears automatically
2. Open Google Authenticator app
3. Scan the displayed QR code
4. Your account is added to the app!
5. Click **"Done - Go to Login"**

### Login Flow

**Step 1: Login**
1. Enter your username
2. Enter your password
3. Press `Enter` or click **Sign In →**

**Step 2: MFA Verification**
1. Open Google Authenticator app on your phone
2. Find your SecureAuth account entry
3. See the 6-digit code (changes every 30 seconds)
4. Enter this code in the verification field
5. Press `Enter` or click **Verify Code ✓**

**Step 3: Success!**
✓ Authentication Complete - Access Granted!

## 🔍 How Google Authenticator Works

### The Technology: RFC 6238 TOTP

**TOTP** = Time-based One-Time Password

1. **Shared Secret**: Both the server and Google Auth share a secret key (`JBSWY3DPEHPK3PXP`)
2. **Time Synchronization**: Both use the current time divided into 30-second windows
3. **HMAC-SHA1**: The secret and time counter are combined using HMAC-SHA1 cryptographic hash
4. **Code Generation**: A 6-digit code is extracted from the hash result
5. **Matching**: Server generates the same code and compares with your input

**Why It's Secure:**
- ✅ Codes change every 30 seconds
- ✅ Old codes cannot be reused
- ✅ Secret never transmitted (stays on phone and server)
- ✅ Even if someone intercepts a code, it expires quickly
- ✅ Works offline (no internet needed on phone)

**In This Project:**
- **Production Mode**: Uses standard RFC 6238 implementation via `pyotp` library
- **Demo Mode**: Uses simplified algorithm in C++ (for demonstration purposes)

## 📂 Project Structure

```
SecureAuthProject/
│
├── config.py                  # Production/Demo mode configuration
├── user_db.py                 # SQLite user database module (NEW)
├── auth_core.cpp              # C++ security backend (optional/legacy)
├── main_gui.py                # Python GUI with glass effects
├── build.py                   # Automated build script
├── users.db                   # SQLite database (auto-created)
├── .gitignore                 # Git ignore file
├── README.md                  # This file
├── SETUP_GUIDE.md             # Google Authenticator guide
├── TECHNICAL_DOCUMENTATION.txt # Comprehensive docs
└── ALL_SOURCE_CODE.txt        # Complete source listing
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

### Database (SQLite)
- **user_db.py** - User database management module
- **users.db** - Auto-created SQLite database file
- **Schema**: `users(username TEXT PRIMARY KEY, password_hash TEXT, totp_secret TEXT)`
- **SHA-256 Hashing** - Password storage
- **Base32 Secrets** - TOTP secret generation using `pyotp.random_base32()`
- **Validation Functions** - Credential verification, TOTP verification

### Backend (C++) - Optional/Legacy
- **DJB2 Hashing** - Legacy password verification  
- **TOTP Generation (Demo)** - Simplified algorithm for demo mode
- **Buffer Protection** - Secure string copy functions
- **Cross-platform** - Compiled as .dll (Windows) or .so (Linux/Mac)

### Frontend (Python)
- **tkinter** - GUI framework
- **SQLite3** - Built-in database (no installation needed)
- **pyotp** - RFC 6238 TOTP implementation
- **qrcode** - QR code generation for Google Authenticator
- **hashlib** - SHA-256 password hashing
- **Glass Effect** - Simulated with stipple patterns
- **Animations** - Math-based gradient animation
- **Windows 11 Theme** - Segoe UI font, modern colors

### How Production Mode Works
1. **User Registration**: Generates unique Base32 TOTP secret
2. **QR Code Generation**: Creates `otpauth://` URI with user-specific secret
3. **TOTP Algorithm**: Uses HMAC-SHA1 (RFC 6238 standard via pyotp)
4. **Time Windows**: 30-second intervals
5. **Verification**: Checks current window ±1 for time drift tolerance
6. **Database Storage**: Encrypted storage in SQLite3

### Colors
- **Primary Blue**: `#0078D4` (Windows accent)
- **Background**: `#FAFAFA` (Soft white)
- **Success**: `#107C10` (Green)
- **Warning**: `#FFA500` (Orange)
- **Error**: `#D83B01` (Red)

## 🛡️ Security Notes

> **⚠️ Educational Purpose**: This project demonstrates MFA concepts. For production use:
> - ✅ Uses SHA-256 password hashing (better than DJB2)
> - ✅ Per-user TOTP secrets (unique for each account)
> - ✅ RFC 6238 compliant TOTP
> - ⚠️ Consider bcrypt/Argon2 for password hashing
> - ⚠️ Add persistent rate limiting beyond session
> - ⚠️ Implement password reset functionality
> - ⚠️ Add email verification
> - ⚠️ Store database encrypted at rest

**What's Production-Ready:**
- ✅ RFC 6238 TOTP (industry standard)
- ✅ Google Authenticator compatible
- ✅ Per-user TOTP secrets
- ✅ SQLite database persistence
- ✅ SHA-256 password hashing
- ✅ Buffer overflow protection (C++ optional)
- ✅ Account lockout mechanism
- ✅ Input validation

**What's For Demo/Learning:**
- ⚠️ SHA-256 (not as strong as bcrypt/Argon2)
- ⚠️ No password reset
- ⚠️ No email verification
- ⚠️ Database not encrypted at rest

## 📖 Documentation

For detailed technical information, see:
- **README.md** - This file (quick start guide)
- **SETUP_GUIDE.md** - Complete Google Authenticator setup guide
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
✅ **Production mode with Google Authenticator** 📱  
✅ **RFC 6238 compliant TOTP**  
✅ **QR code setup for easy configuration**  
✅ **User Sign-Up System** 👤  
✅ **SQLite Database Persistence** 🗄️  
✅ **Per-User TOTP Secrets** 🔐  
✅ **Demo mode with visible codes**  
✅ Login attempt tracking (max 5)  
✅ Copy-to-clipboard with visual confirmation  
✅ Keyboard shortcuts  
✅ Auto-focus inputs  
✅ Enhanced validation  
✅ Color-coded feedback  

## 🔮 Future Enhancements

- [ ] Dark mode toggle
- [ ] Password reset functionality
- [ ] Email verification
- [ ] Session management with timeout
- [ ] Biometric authentication simulation
- [ ] Multi-language support
- [ ] Export authentication logs
- [ ] Database encryption at rest

## 👨‍💻 Author

**Rajith Sundar**
- GitHub: [@RajithSundar](https://github.com/RajithSundar)

## 📝 License

This project is for educational purposes. Feel free to use and modify as needed.

## 🤝 Contributing

This is an educational project, but suggestions and improvements are welcome!

---

**Made with ❤️ using Windows 11 Design Principles**
