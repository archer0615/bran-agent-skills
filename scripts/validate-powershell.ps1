[CmdletBinding()] param()
$ErrorActionPreference='Stop'
$errors=@()
Get-ChildItem (Join-Path (Split-Path -Parent $PSScriptRoot) 'scripts') -Filter *.ps1 | ForEach-Object {
  $tokens=$null; $parseErrors=$null
  [System.Management.Automation.Language.Parser]::ParseFile($_.FullName,[ref]$tokens,[ref]$parseErrors) | Out-Null
  if($parseErrors.Count){$errors += "$($_.FullName): $($parseErrors -join '; ')"}
}
if($errors.Count){$errors | Write-Error; exit 1}
Write-Output 'Validated PowerShell syntax.'
