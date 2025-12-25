# PowerShell Script to Run Population Generator on Frank (Windows 11 PC)
# This script sets up the environment and runs the generator

Write-Host "Starting Population Generator Setup on Frank..." -ForegroundColor Green

$RepoUrl = "https://github.com/Pass-The-Butter/willow.git"
$TargetDir = "$HOME\dev\willow"

# 0. Install Git (if missing)
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git not found. Installing via Winget..." -ForegroundColor Cyan
    winget install --id Git.Git -e --source winget
    Write-Host "Git installed. You may need to restart this script." -ForegroundColor Yellow
}

# 1. Check Python Installation
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python not found. Please install Python 3.11+" -ForegroundColor Red
    Exit
}

# 2. Clone or Pull Repository
if (-not (Test-Path $TargetDir)) {
    Write-Host "Cloning repository to $TargetDir..." -ForegroundColor Cyan
    if (-not (Test-Path "$HOME\dev")) { New-Item -ItemType Directory -Force -Path "$HOME\dev" | Out-Null }
    git clone $RepoUrl $TargetDir
} else {
    Write-Host "Updating repository in $TargetDir..." -ForegroundColor Cyan
    Push-Location $TargetDir
    git pull
    Pop-Location
}

Set-Location $TargetDir

# 3. Create Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv .venv
}

# 4. Activate Virtual Environment
Write-Host "Activating virtual environment..."
& .\.venv\Scripts\Activate.ps1

# 5. Install Dependencies
Write-Host "Installing dependencies..."
pip install -r requirements.txt

# 6. Setup OpenSSH Server (Optional but Recommended)
Write-Host "Checking OpenSSH Server..." -ForegroundColor Cyan
$ssh = Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH.Server*'
if ($ssh.State -ne 'Installed') {
    Write-Host "Installing OpenSSH Server..."
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
}

Write-Host "Configuring SSH Service..."
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

if (!(Get-NetFirewallRule -Name "OpenSSH-Server-In-TCP" -ErrorAction SilentlyContinue)) {
    Write-Host "Allowing SSH through Firewall..."
    New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22
}
Write-Host "SSH Server Ready!" -ForegroundColor Green

# 7. Run Generator
Write-Host "Starting Generator..." -ForegroundColor Cyan
Write-Host "Target: Xeon Server (bunny)"
Write-Host "Goal: 100,000,000 Entities"

python domains/population/remote_generator.py

Write-Host "Generation Complete!" -ForegroundColor Green
