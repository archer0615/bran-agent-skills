[CmdletBinding()] param()
$ErrorActionPreference='Stop'; $root=Split-Path -Parent $PSScriptRoot; $errors=@()
$skillCount=@(Get-ChildItem (Join-Path $root 'skills') -Recurse -Filter SKILL.md).Count
$scenarioText=Get-Content -Raw (Join-Path $root 'references/skill-scenarios.md')
$scenarioCount=@([regex]::Matches($scenarioText,'(?m)^## \d+\. ')).Count
$casePath=Join-Path $root 'references/scenario-test-cases.json'
$caseCount=@(Get-Content -Raw $casePath | ConvertFrom-Json).Count
$cases=@(Get-Content -Raw $casePath | ConvertFrom-Json)
$caseDocCount=@([regex]::Matches((Get-Content -Raw (Join-Path $root 'references/scenario-test-cases.md')),'(?m)^## Case \d+: ')).Count
foreach($path in @((Join-Path $root 'README.md'),(Join-Path $root 'references/continuation-handoff.md'))) {
  $text=Get-Content -Raw $path
  if($text -notmatch "$skillCount 個 Skills") {$errors += "${path}: expected Skill count $skillCount"}
  if($text -notmatch "$scenarioCount 條") {$errors += "${path}: expected scenario count $scenarioCount"}
}
if($caseCount -lt 10) {$errors += "Scenario JSON has fewer than 10 cases: $caseCount"}
if($caseCount -ne $caseDocCount) {$errors += "Scenario JSON/Markdown case count mismatch: $caseCount vs $caseDocCount"}
foreach($case in $cases) { if(($null -eq $case.route -or @($case.route).Count -eq 0) -and $case.id -ne 'direct-answer') {$errors += "Scenario case has no route: $($case.id)"} }
if(-not (Test-Path (Join-Path $root 'references/capability-matrix.md'))) {$errors += 'Missing capability matrix'}
$workflow=Get-Content -Raw (Join-Path $root '.github/workflows/validate.yml')
foreach($script in @('validate-skills.ps1','validate-scenarios.ps1','validate-library.ps1','validate-powershell.ps1','validate-markdown.ps1','validate-consistency.ps1')) {
  if($workflow -notmatch [regex]::Escape($script)) {$errors += "CI does not run $script"}
}
if($errors.Count){$errors | Write-Error; exit 1}
Write-Output "Validated cross-document consistency for $skillCount skills, $scenarioCount scenarios, and $caseCount test cases."
