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
    if($ref -ne $name -and $ref -notin @('planned','attempted','verified','blocked','deferred','unverified','name','smoke','targeted','affected-area','full','pass','fail','partial','ready','not-ready')) {
      if(-not $skills.ContainsKey($ref) -and -not (Test-Path (Join-Path $skillRoot "*\$ref\SKILL.md"))) {$warnings += "$($_.FullName): unresolved Skill reference '$ref'"}
    }
  }
}
$descriptions=@{}
foreach($path in $skills.Values) {
  $text=Get-Content -Raw $path
  $name=[regex]::Match($text,'(?m)^name:\s*([^\r\n]+)').Groups[1].Value.Trim()
  $descriptions[$name]=[regex]::Match($text,'(?m)^description:\s*([^\r\n]+)').Groups[1].Value.Trim()
  $version=[regex]::Match($text,'(?m)^version:\s*([^\r\n]+)').Groups[1].Value.Trim()
  $status=[regex]::Match($text,'(?m)^status:\s*([^\r\n]+)').Groups[1].Value.Trim()
  $reviewed=[regex]::Match($text,'(?m)^last_reviewed:\s*([^\r\n]+)').Groups[1].Value.Trim()
  if($version -notmatch '^\d+\.\d+$') {$errors += "${path}: invalid version metadata"}
  if($status -notin @('active','experimental','deprecated','retired')) {$errors += "${path}: invalid status metadata '$status'"}
  if($reviewed -notmatch '^\d{4}-\d{2}-\d{2}$') {$errors += "${path}: invalid last_reviewed metadata"}
  if($status -in @('deprecated','retired') -and $text -notmatch '(?i)migrat|replacement|替代|遷移') {$errors += "${path}: deprecated or retired Skill needs migration or replacement guidance"}
  if($text -notmatch '(?m)^## Decision rules\s*$') {$errors += "${path}: missing Decision rules"}
  if($text -notmatch '(?m)^## Inputs\s*$') {$errors += "${path}: missing Inputs contract"}
  foreach($field in @('Required:','Optional:','Preconditions:','Missing information:','Output artifact:')) {
    if($text -notmatch [regex]::Escape($field)) {$errors += "${path}: Inputs missing '$field'"}
  }
}
$requiredInputs=@('personal-ai-task-router','requirement-refinement','existing-project-takeover','implementation-validator','decision-researcher','quality-gate')
foreach($required in $requiredInputs) {
  if(-not $skills.ContainsKey($required)) { $errors += "Required core Skill missing: $required"; continue }
  $text=Get-Content -Raw $skills[$required]
  if($text -notmatch '(?m)^## Inputs\s*$') { $errors += "${required}: missing Inputs contract" }
  foreach($field in @('Required:','Optional:','Preconditions:','Missing information:','Output artifact:')) {
    if($text -notmatch [regex]::Escape($field)) { $errors += "${required}: Inputs missing '$field'" }
  }
}
$handoffChecks=@{
  'option-comparison'='decision-researcher'; 'decision-researcher'='option-comparison';
  'prompt-evaluation'='prompt-curator'; 'prompt-curator'='prompt-evaluation';
  'implementation-validator'='quality-gate'; 'quality-gate'='implementation-validator';
  'closed-loop-task-solver'='personal-ai-task-router'; 'personal-ai-task-router'='closed-loop-task-solver'
}
foreach($from in $handoffChecks.Keys) {
  $text=Get-Content -Raw $skills[$from]
  $to=$handoffChecks[$from]
  if($text -notmatch [regex]::Escape($to)) { $errors += "Handoff boundary missing: $from -> $to" }
}
$matrixPath=Join-Path $root 'references/capability-matrix.md'
if(-not (Test-Path $matrixPath)) { $errors += "Missing capability matrix: $matrixPath" }
else {
  $matrix=Get-Content -Raw $matrixPath
  foreach($name in $skills.Keys) { $token='`' + $name + '`'; if($matrix -notmatch [regex]::Escape($token)) { $errors += "Capability matrix missing Skill: $name" } }
  $matrixRows=@([regex]::Matches($matrix,'(?m)^\| `[^`]+` \|')).Count
  if($matrixRows -ne $skills.Count) { $errors += "Capability matrix row count $matrixRows does not match Skill count $($skills.Count)" }
  foreach($line in (Get-Content $matrixPath | Where-Object {$_ -match '^\| `[^`]+` \|'})) {
    $cells=$line.Trim('|').Split('|') | ForEach-Object { $_.Trim() }
    if($cells.Count -ne 5 -or ($cells | Where-Object {[string]::IsNullOrWhiteSpace($_)}).Count -gt 0) { $errors += "Capability matrix row is incomplete: $line"; continue }
    foreach($ref in [regex]::Matches($cells[4],'`([^`]+)`')) { if(-not $skills.ContainsKey($ref.Groups[1].Value) -and $ref.Groups[1].Value -notin @('implementation owner','quality-gate','主要執行 Skill')) { $errors += "Capability matrix has unknown handoff: $($ref.Groups[1].Value)" } }
  }
}
$duplicateDescriptions=$descriptions.GetEnumerator() | Group-Object Value | Where-Object Count -gt 1
foreach($group in $duplicateDescriptions) {$errors += "Duplicate descriptions: $($group.Group.Name -join ', ')"}
if($errors.Count){$errors | Write-Error; if($warnings.Count){$warnings | Write-Warning}; exit 1}
if($warnings.Count){$warnings | Write-Warning}
Write-Output "Validated library boundaries for $($skills.Count) skills."
