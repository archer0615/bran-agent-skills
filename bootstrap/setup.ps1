[CmdletBinding()]
param([string[]]$Categories = @('core','coding','research','knowledge','composite'), [string]$CodexHome = $(if ($env:CODEX_HOME) {$env:CODEX_HOME} else {Join-Path $HOME '.codex'}))
$ErrorActionPreference = 'Stop'; $root = Split-Path -Parent $PSScriptRoot; $target = Join-Path $CodexHome 'skills'; $allowed = @('core','coding','research','knowledge','composite')
if ($Categories.Count -eq 1 -and $Categories[0] -match ',') { $Categories = $Categories[0].Split(',') | ForEach-Object { $_.Trim() } }
foreach ($category in $Categories) { if ($allowed -notcontains $category) { throw "Unknown category: $category" }; Get-ChildItem (Join-Path $root "skills/$category") -Directory | ForEach-Object { $dest=Join-Path $target $_.Name; New-Item -ItemType Directory -Force -Path $target | Out-Null; if (Test-Path -LiteralPath $dest) { $i=Get-Item -LiteralPath $dest -Force; if (-not ($i.Attributes -band [IO.FileAttributes]::ReparsePoint)) { return }; Remove-Item -LiteralPath $dest -Force }; New-Item -ItemType SymbolicLink -Path $dest -Target $_.FullName | Out-Null } }
Write-Output "Installed categories: $($Categories -join ', ')"
