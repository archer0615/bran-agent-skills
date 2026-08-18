[CmdletBinding()] param()
$ErrorActionPreference='Stop'; $root=Split-Path -Parent $PSScriptRoot; $errors=@()
Get-ChildItem $root -Recurse -Filter *.md | ForEach-Object {
  $lines=Get-Content $_.FullName; $fences=($lines | Where-Object {$_ -match '^\s*```'}).Count
  if($fences % 2){$errors += "$($_.FullName): unbalanced fenced code blocks"}
  foreach($line in $lines) {
    foreach($m in [regex]::Matches($line,'\[[^\]]+\]\(([^)]+)\)')) {
      $target=$m.Groups[1].Value
      if($target -notmatch '^(https?://|#|mailto:)' -and -not (Test-Path (Join-Path (Split-Path $_.FullName) $target))) {$errors += "$($_.FullName): missing local link '$target'"}
    }
  }
}
if($errors.Count){$errors | Write-Error; exit 1}
Write-Output 'Validated Markdown fences and local links.'
