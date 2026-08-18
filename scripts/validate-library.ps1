[CmdletBinding()] param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$skillRoot=Join-Path $root 'skills'
$skills=@{}
$errors=@(); $warnings=@()
Get-ChildItem $skillRoot -Recurse -Filter SKILL.md | ForEach-Object {
  $text=Get-Content -Raw $_.FullName
  $name=[regex]::Match($text,'(?m)^name:\s*([^\r\n]+)').Groups[1].Value.Trim()
  if($name){$skills[$name]=$_.FullName}
  foreach($match in [regex]::Matches($text,'`([a-z0-9-]+)`')) {
    $ref=$match.Groups[1].Value
    if($ref -ne $name -and $ref -notin @('planned','attempted','verified','blocked','deferred','unverified','name')) {
      if(-not $skills.ContainsKey($ref) -and -not (Test-Path (Join-Path $skillRoot "*\$ref\SKILL.md"))) {$warnings += "$($_.FullName): unresolved Skill reference '$ref'"}
    }
  }
}
$descriptions=@{}
foreach($path in $skills.Values) {
  $text=Get-Content -Raw $path
  $name=[regex]::Match($text,'(?m)^name:\s*([^\r\n]+)').Groups[1].Value.Trim()
  $descriptions[$name]=[regex]::Match($text,'(?m)^description:\s*([^\r\n]+)').Groups[1].Value.Trim()
  if($text -notmatch '(?m)^## Decision rules\s*$') {$errors += "${path}: missing Decision rules"}
}
$duplicateDescriptions=$descriptions.GetEnumerator() | Group-Object Value | Where-Object Count -gt 1
foreach($group in $duplicateDescriptions) {$errors += "Duplicate descriptions: $($group.Group.Name -join ', ')"}
if($errors.Count){$errors | Write-Error; if($warnings.Count){$warnings | Write-Warning}; exit 1}
if($warnings.Count){$warnings | Write-Warning}
Write-Output "Validated library boundaries for $($skills.Count) skills."
