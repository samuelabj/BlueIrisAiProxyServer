# SpeciesNet AI Proxy Service Installer

# Check for Administrator privileges
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "You do not have Administrator rights to this machine. Log on as an Administrator and re-run this script."
    exit 1
}

$ServiceName = "BlueIrisAiProxy"
$PythonPathRaw = Resolve-Path (Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe")
$ScriptPathRaw = Resolve-Path (Join-Path $PSScriptRoot "..\server.py")
$AppDirectoryRaw = Resolve-Path (Join-Path $PSScriptRoot "..")

$PythonPath = $PythonPathRaw.Path
$ScriptPath = $ScriptPathRaw.Path
$AppDirectory = $AppDirectoryRaw.Path

Write-Host "Debug: PythonPath   = $PythonPath"
Write-Host "Debug: ScriptPath   = $ScriptPath"
Write-Host "Debug: AppDirectory = $AppDirectory"

# Check for NSSM
$NssmPath = Join-Path $PSScriptRoot "nssm.exe"
if (-not (Test-Path $NssmPath)) {
    # Fallback to checking PATH
    if (Get-Command "nssm.exe" -ErrorAction SilentlyContinue) {
        $NssmPath = "nssm.exe"
    }
    else {
        Write-Error "NSSM.exe not found in scripts folder or PATH."
        exit 1
    }
}

Write-Host "Installing $ServiceName Service..."
# Pass paths directly without manual quote escaping. PowerShell and NSSM handle this.
& $NssmPath install $ServiceName $PythonPath $ScriptPath
& $NssmPath set $ServiceName AppDirectory $AppDirectory
& $NssmPath set $ServiceName Description "SpeciesNet AI Proxy for Blue Iris"
& $NssmPath set $ServiceName AppStdout ("$AppDirectory\service.log")
& $NssmPath set $ServiceName AppStderr ("$AppDirectory\service.log")
& $NssmPath set $ServiceName AppRotateFiles 1
& $NssmPath set $ServiceName AppRotateOnline 1
& $NssmPath set $ServiceName AppRotateSeconds 86400
& $NssmPath set $ServiceName AppRotateBytes 5242880

Write-Host "Service installed successfully."

# Verify Configuration
Write-Host "--- Service Configuration ---"
& $NssmPath get $ServiceName Application
& $NssmPath get $ServiceName AppParameters
& $NssmPath get $ServiceName AppDirectory
Write-Host "-----------------------------"

Write-Host "You can start it with: nssm start $ServiceName"
