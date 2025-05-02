# PowerShell script to guide you through pushing to GitHub
# Run this script after you have Git installed and GitHub repository created

$ErrorActionPreference = "Stop"

function Show-Step {
    param (
        [string]$Step,
        [string]$Description
    )
    Write-Host "`n==============================================" -ForegroundColor Cyan
    Write-Host "STEP $Step`: $Description" -ForegroundColor Cyan
    Write-Host "=============================================="
}

Write-Host "Complete Healthcare System - GitHub Push Guide" -ForegroundColor Green
Write-Host "-----------------------------------------------"
Write-Host "This script will help you push your project to GitHub." -ForegroundColor Yellow
Write-Host "Make sure you have already created a GitHub repository named 'Complete-Healthcare-System'." -ForegroundColor Yellow

# Check for Git and add to path if needed
Write-Host "`nChecking for Git installation..." -ForegroundColor Gray
$gitFound = $false

try {
    $gitVersion = git --version
    $gitFound = $true
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
}
catch {
    Write-Host "Git not found in PATH. Looking for Git installation..." -ForegroundColor Yellow
    
    # Common Git installation paths
    $possiblePaths = @(
        "C:\Program Files\Git\bin",
        "C:\Program Files (x86)\Git\bin",
        "${env:ProgramFiles}\Git\bin",
        "${env:ProgramFiles(x86)}\Git\bin",
        "${env:LOCALAPPDATA}\Programs\Git\bin"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path "$path\git.exe") {
            Write-Host "Git found at: $path" -ForegroundColor Green
            $env:Path += ";$path"
            $gitFound = $true
            
            try {
                $gitVersion = git --version
                Write-Host "Git version: $gitVersion" -ForegroundColor Green
            }
            catch {
                Write-Host "Added Git to path but still can't execute it. Please restart PowerShell after installation." -ForegroundColor Red
            }
            
            break
        }
    }
    
    if (-not $gitFound) {
        Write-Host "Git is not installed or not found!" -ForegroundColor Red
        Write-Host "Please download and install Git from https://git-scm.com/downloads" -ForegroundColor Red
        Write-Host "After installation, close and reopen PowerShell, then run this script again." -ForegroundColor Red
        exit 1
    }
}

# STEP 1: Configure Git
Show-Step "1" "Configure Git"
$name = Read-Host "Enter your name for Git configuration"
$email = Read-Host "Enter your email for Git configuration"

git config --global user.name "$name"
git config --global user.email "$email"
Write-Host "Git configured successfully!" -ForegroundColor Green

# STEP 2: Initialize repository
Show-Step "2" "Initialize the repository"
git init
Write-Host "Git repository initialized!" -ForegroundColor Green

# STEP 3: Add files to staging
Show-Step "3" "Add files to staging area"
git add .
Write-Host "Files added to staging area!" -ForegroundColor Green

# STEP 4: Commit changes
Show-Step "4" "Commit changes"
$message = Read-Host "Enter a commit message (default: 'Initial commit')"
if ([string]::IsNullOrWhiteSpace($message)) {
    $message = "Initial commit"
}
git commit -m "$message"
Write-Host "Changes committed!" -ForegroundColor Green

# STEP 5: Set up remote repository
Show-Step "5" "Set up remote repository"
$username = Read-Host "Enter your GitHub username"
$repoName = Read-Host "Enter your exact repository name (default: Complete-Healthcare-System)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "Complete-Healthcare-System"
}

git branch -M main
git remote add origin "https://github.com/$username/$repoName.git"
Write-Host "Remote repository configured!" -ForegroundColor Green

# STEP 6: Push to GitHub
Show-Step "6" "Push to GitHub"
Write-Host "You will be prompted to enter your GitHub credentials." -ForegroundColor Yellow
Write-Host "Note: For security, you might need to use a personal access token instead of your password." -ForegroundColor Yellow
Write-Host "Create one at: https://github.com/settings/tokens" -ForegroundColor Yellow
git push -u origin main

Write-Host "`n==============================================================" -ForegroundColor Green
Write-Host "Success! Your Complete Healthcare System has been pushed to GitHub!" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green
Write-Host "`nYour repository is now available at: https://github.com/$username/$repoName" -ForegroundColor Cyan
Write-Host "`nNotes:`n- You might need to refresh the page to see your files.`n- If you want to make changes, commit and push again using:`n  git add .`n  git commit -m 'your message'`n  git push" -ForegroundColor Gray 