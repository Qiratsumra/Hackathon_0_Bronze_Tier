#!/usr/bin/env pwsh
# Quick Start Guide for Bronze Tier AI Employee

Write-Host "`n╔═══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Bronze Tier: Personal AI Employee Quick Start  ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Step 1: Install UV if not already installed
Write-Host "Step 1: Installing UV..." -ForegroundColor Yellow
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "UV not found. Installing..." -ForegroundColor Yellow
    pip install uv
}
else {
    Write-Host "UV is already installed" -ForegroundColor Green
}

# Step 2: Sync dependencies
Write-Host "`nStep 2: Syncing dependencies..." -ForegroundColor Yellow
uv sync

# Step 3: Create .env file
Write-Host "`nStep 3: Setting up configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host "  ⚠️  Please edit .env with your API keys:" -ForegroundColor Yellow
    Write-Host "     - ANTHROPIC_API_KEY" -ForegroundColor White
    Write-Host "     - GMAIL credentials (optional)" -ForegroundColor White
    Write-Host "     - WHATSAPP_API_KEY (optional)" -ForegroundColor White
}
else {
    Write-Host "✓ .env file already exists" -ForegroundColor Green
}

# Step 4: Verify Obsidian vault
Write-Host "`nStep 4: Obsidian vault setup..." -ForegroundColor Yellow
$vaultPath = ".\AI_Employee_Vault"
if (Test-Path $vaultPath) {
    Write-Host "✓ Obsidian vault exists at $vaultPath" -ForegroundColor Green
    Write-Host "  Instructions:" -ForegroundColor Cyan
    Write-Host "    1. Open Obsidian" -ForegroundColor White
    Write-Host "    2. Click 'Open folder as vault'" -ForegroundColor White
    Write-Host "    3. Select: $((Get-Item $vaultPath).FullName)" -ForegroundColor White
}
else {
    Write-Host "✗ Vault directory not found" -ForegroundColor Red
}

# Step 5: Ready to run
Write-Host "`nStep 5: Ready to start!" -ForegroundColor Yellow
Write-Host "`nTo run the agent:" -ForegroundColor Cyan
Write-Host "  uv run python src/main.py`n" -ForegroundColor Green

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Edit .env with your Gemini API key" -ForegroundColor White
Write-Host "  2. Open Obsidian vault at AI_Employee_Vault/" -ForegroundColor White
Write-Host "  3. Create your first skill in Skills/ directory" -ForegroundColor White
Write-Host "  4. Run the agent" -ForegroundColor White
Write-Host "  5. Check Brain/ for decision logs`n" -ForegroundColor White
