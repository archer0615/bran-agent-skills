[CmdletBinding()] param(
  [Parameter(Mandatory=$true)][ValidatePattern('^v\d+\.\d+\.\d+$')][string]$Version
)
$ErrorActionPreference='Stop'; $root=Split-Path -Parent $PSScriptRoot
& (Join-Path $PSScriptRoot 'validate-skills.ps1')
& (Join-Path $PSScriptRoot 'validate-scenarios.ps1')
& (Join-Path $PSScriptRoot 'validate-library.ps1')
& (Join-Path $PSScriptRoot 'validate-powershell.ps1')
& (Join-Path $PSScriptRoot 'validate-markdown.ps1')
& (Join-Path $PSScriptRoot 'validate-consistency.ps1')
Write-Output "Release checks passed for $Version."
Write-Output "Suggested next steps: review git diff, update CHANGELOG.md, commit, push, then create tag $Version after approval."
