[CmdletBinding()] param()
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$schemaRoot = Join-Path $root 'orchestrator/schemas'
$errors = @()
$files = @(Get-ChildItem $schemaRoot -Filter '*.schema.json' -File)
foreach ($file in $files) {
  try { $schema = Get-Content -Raw $file.FullName | ConvertFrom-Json }
  catch { $errors += "$($file.Name): invalid JSON"; continue }
  foreach ($property in @('$schema', 'title', 'type', 'required', 'additionalProperties')) {
    if ($null -eq $schema.$property) { $errors += "$($file.Name): missing $property" }
  }
  if ($schema.type -ne 'object') { $errors += "$($file.Name): root type must be object" }
  if ($schema.additionalProperties -ne $false) { $errors += "$($file.Name): additionalProperties must be false" }
  if ($schema.required.Count -eq 0) { $errors += "$($file.Name): required must not be empty" }
}
if ($errors.Count) { $errors | Write-Error; exit 1 }
Write-Output "Validated $($files.Count) orchestrator schemas."
