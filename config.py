# Configuration File for Secure Authentication System
# Toggle between Production and Demo modes

# =============================================================================
# MODE CONFIGURATION
# =============================================================================

# Set to True for production deployment (hides demo TOTP display)
# Set to False for demo/testing (shows TOTP on screen)
PRODUCTION_MODE = False

# =============================================================================
# TOTP CONFIGURATION
# =============================================================================

# TOTP Secret Key (shared with Google Authenticator or other TOTP apps)
# IMPORTANT: In production, this should be unique per user and stored securely
TOTP_SECRET = "MY_SUPER_SECRET_KEY"

# Application Details for Google Authenticator
APP_NAME = "SecureAuthSystem"
ISSUER = "SecureAuth"
ACCOUNT_NAME = "admin"

# =============================================================================
# SECURITY SETTINGS
# =============================================================================

# Maximum login attempts before account lockout
MAX_LOGIN_ATTEMPTS = 5

# TOTP window in seconds (strict validation)
TOTP_WINDOW_SECONDS = 30

# =============================================================================
# NOTES
# =============================================================================
# 
# Production Mode vs Demo Mode:
# ------------------------------
# Demo Mode (PRODUCTION_MODE = False):
#   - Shows current TOTP code on screen
#   - Displays "Copy Demo TOTP" button
#   - Useful for testing and demonstrations
#
# Production Mode (PRODUCTION_MODE = True):
#   - Hides TOTP code display
#   - Requires Google Authenticator or compatible app
#   - Shows setup instructions window on first run
#   - More secure for real deployments
#
# Google Authenticator Setup:
# ----------------------------
# 1. Set PRODUCTION_MODE = True
# 2. Run the application
# 3. Click "Setup Authenticator" button
# 4. Scan QR code with Google Authenticator app
# 5. Enter the 6-digit code to authenticate
#
