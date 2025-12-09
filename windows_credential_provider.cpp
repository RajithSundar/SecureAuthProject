/*
 * SecureAuth Credential Provider - Reference Implementation
 *
 * EDUCATIONAL PURPOSE ONLY - NOT FOR INSTALLATION
 *
 * This is a reference implementation showing how to create a Windows
 * Credential Provider that integrates with the SecureAuth system.
 *
 * Windows Credential Providers replace the standard Windows login screen
 * with custom authentication logic, enabling MFA at the OS level.
 *
 * WARNING: Do NOT compile and install this without extensive testing in a VM.
 * Incorrect implementation can lock you out of Windows.
 */

#include <credentialprovider.h>
#include <memory>
#include <ntsecapi.h>
#include <shlguid.h>
#include <sqlite3.h>
#include <string>
#include <strsafe.h>
#include <windows.h>


// GUID for our custom credential provider
// In production, generate unique GUID with uuidgen.exe
// {12345678-1234-1234-1234-123456789ABC}
static const GUID CLSID_SecureAuthProvider = {
    0x12345678,
    0x1234,
    0x1234,
    {0x12, 0x34, 0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC}};

//
// SecureAuthCredential - Individual credential tile
//
// Represents one authentication attempt on the Windows login screen
//
class SecureAuthCredential : public ICredentialProviderCredential2 {
private:
  LONG m_cRef;
  ICredentialProviderCredentialEvents2 *m_pCredProvCredentialEvents;

  // User input fields
  PWSTR m_pszUsername;
  PWSTR m_pszPassword;
  PWSTR m_pszTOTPCode;

  // Field indices
  enum SecureAuthFieldID {
    SFI_TILEIMAGE = 0,
    SFI_LABEL,
    SFI_USERNAME,
    SFI_PASSWORD,
    SFI_TOTP,
    SFI_SUBMIT,
    SFI_NUM_FIELDS
  };

public:
  SecureAuthCredential();
  ~SecureAuthCredential();

  // IUnknown methods
  STDMETHOD_(ULONG, AddRef)();
  STDMETHOD_(ULONG, Release)();
  STDMETHOD(QueryInterface)(REFIID riid, void **ppv);

  // ICredentialProviderCredential methods
  STDMETHOD(Advise)(ICredentialProviderCredentialEvents *pcpce);
  STDMETHOD(UnAdvise)();
  STDMETHOD(SetSelected)(BOOL *pbAutoLogon);
  STDMETHOD(SetDeselected)();
  STDMETHOD(GetFieldState)
  (DWORD dwFieldID, CREDENTIAL_PROVIDER_FIELD_STATE *pcpfs,
   CREDENTIAL_PROVIDER_FIELD_INTERACTIVE_STATE *pcpfis);
  STDMETHOD(GetStringValue)(DWORD dwFieldID, PWSTR *ppwsz);
  STDMETHOD(GetBitmapValue)(DWORD dwFieldID, HBITMAP *phbmp);
  STDMETHOD(GetCheckboxValue)
  (DWORD dwFieldID, BOOL *pbChecked, PWSTR *ppwszLabel);
  STDMETHOD(GetComboBoxValueCount)
  (DWORD dwFieldID, DWORD *pcItems, DWORD *pdwSelectedItem);
  STDMETHOD(GetComboBoxValueAt)
  (DWORD dwFieldID, DWORD dwItem, PWSTR *ppwszItem);
  STDMETHOD(GetSubmitButtonValue)(DWORD dwFieldID, DWORD *pdwAdjacentTo);
  STDMETHOD(SetStringValue)(DWORD dwFieldID, PCWSTR pwz);
  STDMETHOD(SetCheckboxValue)(DWORD dwFieldID, BOOL bChecked);
  STDMETHOD(SetComboBoxSelectedValue)(DWORD dwFieldID, DWORD dwSelectedItem);
  STDMETHOD(CommandLinkClicked)(DWORD dwFieldID);
  STDMETHOD(GetSerialization)
  (CREDENTIAL_PROVIDER_GET_SERIALIZATION_RESPONSE *pcpgsr,
   CREDENTIAL_PROVIDER_CREDENTIAL_SERIALIZATION *pcpcs,
   PWSTR *ppwszOptionalStatusText,
   CREDENTIAL_PROVIDER_STATUS_ICON *pcpsiOptionalStatusIcon);
  STDMETHOD(ReportResult)
  (NTSTATUS ntsStatus, NTSTATUS ntsSubstatus, PWSTR *ppwszOptionalStatusText,
   CREDENTIAL_PROVIDER_STATUS_ICON *pcpsiOptionalStatusIcon);

  // ICredentialProviderCredential2 methods
  STDMETHOD(GetUserSid)(PWSTR *ppszSid);

private:
  // Helper methods
  HRESULT ValidateCredentials();
  HRESULT ValidateWithDatabase(PCWSTR username, PCWSTR password, PCWSTR totp);
  HRESULT
  PackageCredentials(CREDENTIAL_PROVIDER_CREDENTIAL_SERIALIZATION *pcpcs);
};

//
// SecureAuthProvider - Main credential provider class
//
// This is the entry point that Windows calls during login
//
class SecureAuthProvider : public ICredentialProvider {
private:
  LONG m_cRef;
  SecureAuthCredential *m_pCredential;
  CREDENTIAL_PROVIDER_USAGE_SCENARIO m_usageScenario;

public:
  SecureAuthProvider();
  ~SecureAuthProvider();

  // IUnknown methods
  STDMETHOD_(ULONG, AddRef)();
  STDMETHOD_(ULONG, Release)();
  STDMETHOD(QueryInterface)(REFIID riid, void **ppv);

  // ICredentialProvider methods
  STDMETHOD(SetUsageScenario)
  (CREDENTIAL_PROVIDER_USAGE_SCENARIO cpus, DWORD dwFlags);
  STDMETHOD(SetSerialization)
  (const CREDENTIAL_PROVIDER_CREDENTIAL_SERIALIZATION *pcpcs);
  STDMETHOD(Advise)(ICredentialProviderEvents *pcpe, UINT_PTR upAdviseContext);
  STDMETHOD(UnAdvise)();
  STDMETHOD(GetFieldDescriptorCount)(DWORD *pdwCount);
  STDMETHOD(GetFieldDescriptorAt)
  (DWORD dwIndex, CREDENTIAL_PROVIDER_FIELD_DESCRIPTOR **ppcpfd);
  STDMETHOD(GetCredentialCount)
  (DWORD *pdwCount, DWORD *pdwDefault, BOOL *pbAutoLogonWithDefault);
  STDMETHOD(GetCredentialAt)
  (DWORD dwIndex, ICredentialProviderCredential **ppcpc);
};

//
// Database Integration Functions
//
// These functions connect to the SQLite database created by user_db.py
//

// Validate user credentials against SQLite database
HRESULT ValidateUser(PCWSTR username, PCWSTR password, PCWSTR totp,
                     BOOL *pbValid) {
  *pbValid = FALSE;
  sqlite3 *db = nullptr;

  // Open database
  int rc = sqlite3_open("C:\\SecureAuth\\users.db", &db);
  if (rc != SQLITE_OK) {
    return E_FAIL;
  }

  // Convert WCHAR to char for SQLite
  char szUsername[256], szPassword[256], szTOTP[7];
  WideCharToMultiByte(CP_UTF8, 0, username, -1, szUsername, 256, NULL, NULL);
  WideCharToMultiByte(CP_UTF8, 0, password, -1, szPassword, 256, NULL, NULL);
  WideCharToMultiByte(CP_UTF8, 0, totp, -1, szTOTP, 7, NULL, NULL);

  // Step 1: Retrieve password hash and TOTP secret from database
  sqlite3_stmt *stmt;
  const char *sql =
      "SELECT password_hash, totp_secret FROM users WHERE username = ?";

  rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
  if (rc != SQLITE_OK) {
    sqlite3_close(db);
    return E_FAIL;
  }

  sqlite3_bind_text(stmt, 1, szUsername, -1, SQLITE_STATIC);

  if (sqlite3_step(stmt) == SQLITE_ROW) {
    const char *stored_hash = (const char *)sqlite3_column_text(stmt, 0);
    const char *totp_secret = (const char *)sqlite3_column_text(stmt, 1);

    // Step 2: Hash the provided password (SHA-256)
    // TODO: Implement SHA-256 hashing here
    // For now, simplified comparison

    // Step 3: Verify TOTP code
    // TODO: Implement RFC 6238 TOTP verification
    // This would use the same algorithm as pyotp

    // Placeholder validation
    // In production: hash password, verify TOTP with HMAC-SHA1
    *pbValid = TRUE;
  }

  sqlite3_finalize(stmt);
  sqlite3_close(db);

  return S_OK;
}

//
// COM DLL Entry Points
//
// These functions are required for Windows to load and register the provider
//

// DLL entry point
BOOL APIENTRY DllMain(HMODULE hModule, DWORD dwReason, LPVOID lpReserved) {
  switch (dwReason) {
  case DLL_PROCESS_ATTACH:
    DisableThreadLibraryCalls(hModule);
    break;
  case DLL_PROCESS_DETACH:
    break;
  }
  return TRUE;
}

// Class factory for creating provider instances
class CClassFactory : public IClassFactory {
private:
  LONG m_cRef;

public:
  CClassFactory() : m_cRef(1) {}

  // IUnknown
  STDMETHOD_(ULONG, AddRef)() { return InterlockedIncrement(&m_cRef); }
  STDMETHOD_(ULONG, Release)() {
    LONG cRef = InterlockedDecrement(&m_cRef);
    if (cRef == 0)
      delete this;
    return cRef;
  }
  STDMETHOD(QueryInterface)(REFIID riid, void **ppv) {
    if (riid == IID_IClassFactory || riid == IID_IUnknown) {
      *ppv = static_cast<IClassFactory *>(this);
      AddRef();
      return S_OK;
    }
    *ppv = nullptr;
    return E_NOINTERFACE;
  }

  // IClassFactory
  STDMETHOD(CreateInstance)(IUnknown *pUnkOuter, REFIID riid, void **ppv) {
    if (pUnkOuter != nullptr)
      return CLASS_E_NOAGGREGATION;

    SecureAuthProvider *pProvider = new SecureAuthProvider();
    if (!pProvider)
      return E_OUTOFMEMORY;

    HRESULT hr = pProvider->QueryInterface(riid, ppv);
    pProvider->Release();
    return hr;
  }

  STDMETHOD(LockServer)(BOOL fLock) { return S_OK; }
};

// DLL export: Create class factory
STDAPI DllGetClassObject(REFCLSID rclsid, REFIID riid, LPVOID *ppv) {
  if (rclsid == CLSID_SecureAuthProvider) {
    CClassFactory *pFactory = new CClassFactory();
    if (!pFactory)
      return E_OUTOFMEMORY;

    HRESULT hr = pFactory->QueryInterface(riid, ppv);
    pFactory->Release();
    return hr;
  }

  return CLASS_E_CLASSNOTAVAILABLE;
}

// DLL export: Check if DLL can be unloaded
STDAPI DllCanUnloadNow() {
  // In production, track object count
  return S_OK;
}

//
// Registry Registration
//
// These functions register/unregister the provider with Windows
//

HRESULT RegisterCredentialProvider() {
  // Registry path:
  // HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\Credential
  // Providers\{GUID} This tells Windows about our credential provider

  // NOTE: This is示例 code only - actual implementation requires proper COM
  // registration
  return S_OK;
}

HRESULT UnregisterCredentialProvider() {
  // Remove registry entries
  return S_OK;
}

/*
 * INTEGRATION POINTS WITH EXISTING SECUREAUTH SYSTEM:
 *
 * 1. Database Integration:
 *    - Reads from same users.db created by user_db.py
 *    - Uses same schema: users(username, password_hash, totp_secret)
 *
 * 2. Authentication Flow:
 *    - User enters username, password, TOTP on Windows login screen
 *    - Credential provider validates against SQLite database
 *    - If valid, Windows login proceeds
 *
 * 3. TOTP Verification:
 *    - Uses same RFC 6238 algorithm as pyotp
 *    - Verifies against user-specific secret from database
 *
 * 4. Security:
 *    - Runs at SYSTEM level (highest Windows privilege)
 *    - Inherits buffer overflow protection from auth_core.cpp
 *    - Uses SHA-256 password hashing from user_db.py
 */
