# SecureAuth - Windows Credential Provider Build Instructions

⚠️ **EDUCATIONAL/REFERENCE ONLY - DO NOT BUILD FOR PRODUCTION USE**

## Overview

This directory contains a Windows Credential Provider reference implementation
that demonstrates how SecureAuth can integrate with Windows OS authentication.

## Files

- `windows_credential_provider.cpp` - Main C++ implementation
- `provider.def` - DLL export definitions
- `WINDOWS_OS_INTEGRATION.md` - Technical architecture documentation
- `BUILD_INSTRUCTIONS.md` - This file

## Prerequisites

**DO NOT ATTEMPT TO BUILD/INSTALL without extensive knowledge of:**
- Windows internals
- COM programming
- Credential Provider API
- System-level debugging

**Requirements (if building for educational purposes in a VM):**
1. Windows 10/11 SDK
2. Visual Studio 2019 or later
3. SQLite3 development libraries
4. Virtual Machine for testing (MANDATORY)

## Build Steps (VM Only!)

### 1. Install Dependencies

Download SQLite amalgamation from https://www.sqlite.org/download.html:
- sqlite3.h
- sqlite3.c
- sqlite3.lib (or compile from source)

### 2. Compile Command

```cmd
cl /c /EHsc /std:c++17 windows_credential_provider.cpp
link /DLL /OUT:SecureAuthProvider.dll ^
     windows_credential_provider.obj ^
     /DEF:provider.def ^
     advapi32.lib ole32.lib sqlite3.lib ^
     /SUBSYSTEM:WINDOWS
```

### 3. Register (ONLY IN VM!)

```cmd
:: Run as Administrator
regsvr32 SecureAuthProvider.dll

:: Add to credential providers registry
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers\{12345678-1234-1234-1234-123456789ABC}" ^
    /v "(Default)" /t REG_SZ /d "SecureAuth MFA Provider" /f
```

### 4. Configure Database Path

The provider expects to find `users.db` at:
```
C:\SecureAuth\users.db
```

Copy your existing database or create users via the Python GUI.

### 5. Restart Windows (IN VM!)

The credential provider will load on next boot.

## Safety Checklist

Before even considering building this:

- [ ] Running in a **Virtual Machine** (VM)
- [ ] Have VM snapshot/backup before changes
- [ ] Understand COM programming
- [ ] Understand Windows Security architecture
- [ ] Know how to boot Windows in Safe Mode
- [ ] Have Administrator account backup
- [ ] Tested code thoroughly in debugger
- [ ] Have rollback plan

## Uninstallation (If installed in VM)

```cmd
:: Disable provider
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers\{12345678-1234-1234-1234-123456789ABC}" /f

:: Unregister DLL
regsvr32 /u SecureAuthProvider.dll

:: Restart Windows
shutdown /r /t 0
```

## For Course Submission

**RECOMMENDED APPROACH:**

DO NOT build or install this code. Instead:

1. **Show the code** (`windows_credential_provider.cpp`)
2. **Reference the documentation** (`WINDOWS_OS_INTEGRATION.md`)
3. **Explain the architecture** in your report/presentation
4. **Demonstrate understanding** of Windows authentication

This proves you understand OS integration without risking your system.

## Alternative: Demo Video

If you want to show it working:
1. Use a VM
2. Record screen during:
   - Installation
   - Windows login screen showing custom provider
   - Successful MFA authentication
   - Uninstallation
3. Include video in presentation

## References

- [Microsoft Credential Provider Samples](https://github.com/microsoft/Windows-classic-samples/tree/master/Samples/CredentialProvider)
- [Credential Provider Technical Reference](https://docs.microsoft.com/en-us/windows/win32/secauthn/credential-providers-in-windows)
- [COM Development Guide](https://docs.microsoft.com/en-us/windows/win32/com/)

## License

Educational use only. Not for production deployment.

---

**Remember: Incorrectly implemented credential providers can lock you out of Windows permanently. Always test in a VM with snapshots.**
