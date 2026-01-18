$ErrorActionPreference = "Stop"

Write-Host "=== AI-Vision-Relay Setup ===" -ForegroundColor Cyan

# 1. Check for Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Error "Python is not installed or not in PATH. Please install Python 3.10+ before running setup."
    exit 1
}

# 2. Check/Create Virtual Environment
$venvPath = Join-Path $PSScriptRoot "..\.venv"
if (Test-Path $venvPath) {
    Write-Host "Virtual environment already exists at $venvPath"
}
else {
    Write-Host "Creating virtual environment..."
    python -m venv $venvPath
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# 3. Install Dependencies
Write-Host "Installing dependencies..."
$pipExec = Join-Path $venvPath "Scripts\pip.exe"
if (-not (Test-Path $pipExec)) {
    Write-Error "pip not found in venv. Creation might have failed."
    exit 1
}

$reqFile = Join-Path $PSScriptRoot "..\requirements.txt"
& $pipExec install --upgrade pip
& $pipExec install -r $reqFile

Write-Host "Dependencies installed successfully." -ForegroundColor Green

# 4. Prompt for Service Installation
$response = Read-Host "Do you want to install/update the Windows Service now? (y/n)"
if ($response -eq 'y') {
    $installScript = Join-Path $PSScriptRoot "install_service.ps1"
    Write-Host "Running service installer..."
    & $installScript
}
else {
    Write-Host "Service installation skipped."
    Write-Host "You can run 'scripts\install_service.ps1' later to install the service." -ForegroundColor Yellow
}

Write-Host "Setup complete!" -ForegroundColor Cyan
