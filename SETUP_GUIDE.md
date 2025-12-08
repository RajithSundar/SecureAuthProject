# Google Authenticator Setup Guide

## 📱 What is Google Authenticator?

Google Authenticator is a free app that generates time-based one-time passwords (TOTP) for two-factor authentication. It provides an extra layer of security by requiring a 6-digit code that changes every 30 seconds.

## 📥 Download the App

### iOS (iPhone/iPad)
1. Open App Store
2. Search for "Google Authenticator"
3. Download and install the app

### Android
1. Open Google Play Store
2. Search for "Google Authenticator"
3. Download and install the app

Download link: https://support.google.com/accounts/answer/1066447

## 🔧 Setup Instructions

### Method 1: Scan QR Code (Recommended)

1. Run the Secure Authentication System
2. Click the **"⚙️ Setup Authenticator"** button
3. Open Google Authenticator app on your phone
4. Tap the **"+"** button in the app
5. Choose **"Scan a QR code"**
6. Point your camera at the QR code displayed
7. The account will be added automatically!

### Method 2: Manual Entry

If you can't scan the QR code:

1. Run the Secure Authentication System
2. Click the **"⚙️ Setup Authenticator"** button
3. Note the **Secret Key** shown in the manual entry section
4. Open Google Authenticator app
5. Tap the **"+"** button
6. Choose **"Enter a setup key"**
7. Enter the following details:
   - **Account**: admin
   - **Key**: `MY_SUPER_SECRET_KEY` (or the key shown in app)
   - **Type of key**: Time based
8. Tap **"Add"**

## 🔐 Using the App for Login

### Step 1: Login with Password
- Enter your username and password
- Click **Sign In**

### Step 2: Enter TOTP Code
1. Open Google Authenticator app
2. Find "SecureAuthSystem (admin)" account
3. You'll see a 6-digit code (refreshes every 30 seconds)
4. Enter this code in the verification field
5. Click **Verify Code**

**Important**: The code expires every 30 seconds! If the timer is almost up, wait for the next code.

## 🔀 Switching Between Demo and Production Mode

### Demo Mode (Default)
- Shows TOTP code on screen (yellow banner)
- No Google Authenticator needed
- Good for testing and demonstrations

**To enable**: In `config.py`, set:
```python
PRODUCTION_MODE = False
```

### Production Mode
- Hides TOTP code display
- Requires Google Authenticator app
- More secure for real deployments

**To enable**: In `config.py`, set:
```python
PRODUCTION_MODE = True
```

## 🛠️ Troubleshooting

### "Invalid or expired TOTP code"
- **Time Sync Issue**: Make sure your phone's time is set to automatic
  - iOS: Settings → General → Date & Time → Set Automatically
  - Android: Settings → System → Date & time → Automatic date & time
- **Old Code**: The code changes every 30 seconds. Make sure you're using the current code.
- **Typo**: Double-check you entered all 6 digits correctly

### "Can't scan QR code"
- Ensure good lighting
- Hold phone steady at proper distance
- Use manual entry method instead

### "Code not showing in app"
- Restart Google Authenticator app
- Check that account was added successfully
- Try removing and re-adding the account

### "Setup button not showing"
- Make sure `PRODUCTION_MODE = True` in `config.py`
- Restart the application after changing config

## 🔒 Security Best Practices

1. **Backup Codes**: Screenshot the QR code or save the secret key in a secure password manager
2. **Phone Lock**: Always use a PIN/password on your phone
3. **Multiple Devices**: You can add the same account to multiple devices using the same QR code
4. **Lost Phone**: If you lose your phone, you can re-setup using the same secret key

## 📝 Alternative TOTP Apps

Google Authenticator isn't the only option! These apps also work:
- **Microsoft Authenticator**
- **Authy**
- **1Password**
- **LastPass Authenticator**

All of them use the same TOTP standard, so the QR code will work with any of them.

## 💡 Tips

- The secret key is: `MY_SUPER_SECRET_KEY`
- This is hardcoded for demo purposes
- In production, each user should have a unique secret
- Codes are exactly 6 digits (may have leading zeros)
- A new code is generated every 30 seconds
- The countdown timer shows time remaining for current code

## 📞 Support

For issues specific to Google Authenticator app, visit:
https://support.google.com/accounts/answer/1066447

---

**Made with ❤️ for the Secure Authentication System**
