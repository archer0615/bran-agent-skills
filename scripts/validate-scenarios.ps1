[CmdletBinding()] param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$scenarioPath=Join-Path $root 'references/skill-scenarios.md'
$casePath=Join-Path $root 'references/scenario-test-cases.json'
$skillNames=@{}
Get-ChildItem (Join-Path $root 'skills') -Recurse -Filter SKILL.md | ForEach-Object {$skillNames[$_.Directory.Name]=$true}
$lines=Get-Content $scenarioPath
$routeLines=$lines | Where-Object {$_ -match '^\s*`[^`]+`' -and $_ -notmatch '^\s*#'}
$errors=@()
$scenarioHeadings=@($lines | Where-Object {$_ -match '^## \d+\. '})
if ($scenarioHeadings.Count -eq 0) {$errors += 'No numbered scenarios found'}
foreach($heading in $scenarioHeadings) {
  $index=[array]::IndexOf($lines,$heading); $next=$lines.Count
  for($i=$index+1; $i -lt $lines.Count; $i++) { if($lines[$i] -match '^## \d+\. ') {$next=$i; break} }
  $block=$lines[$index..($next-1)] -join "`n"
  foreach($required in @('### Prompt','### Expected route','### Required behavior')) { if($block -notmatch [regex]::Escape($required)) {$errors += "$heading missing $required"} }
}
foreach($line in $routeLines) { foreach($match in [regex]::Matches($line,'`([^`]+)`')) { $name=$match.Groups[1].Value; if(-not $skillNames.ContainsKey($name)) {$errors += "Unknown skill in scenario route: $name"} } }
if(-not (Test-Path $casePath)) {$errors += "Missing scenario test data: $casePath"} else {
  try {$cases=@(Get-Content -Raw $casePath | ConvertFrom-Json)} catch {$errors += "Invalid scenario test JSON: $($_.Exception.Message)"}
  $ids=@()
  foreach($case in $cases) {
    foreach($field in @('id','input','expected','failure')) { if([string]::IsNullOrWhiteSpace([string]$case.$field)) {$errors += "Scenario case missing '$field': $($case.id)"} }
    foreach($field in @('required','forbidden')) { if($null -eq $case.$field -or @($case.$field).Count -eq 0) {$errors += "Scenario case missing '$field' behavior contract: $($case.id)"} }
    if($case.id -in $ids) {$errors += "Duplicate scenario test case id: $($case.id)"} else {$ids += [string]$case.id}
    if(($null -eq $case.route -or @($case.route).Count -eq 0) -and $case.id -ne 'direct-answer') {$errors += "Scenario case has empty route: $($case.id)"}
    else { foreach($routeSkill in @($case.route)) { if(-not $skillNames.ContainsKey([string]$routeSkill)) {$errors += "Unknown Skill in scenario case $($case.id): $routeSkill"} } }
    if(@($case.route).Count -ne @($case.route | Select-Object -Unique).Count) {$errors += "Scenario route contains duplicate Skill: $($case.id)"}
  }
  if($cases.Count -lt 10) {$errors += "Expected at least 10 scenario test cases, found $($cases.Count)"}
  $caseDoc=Get-Content -Raw (Join-Path $root 'references/scenario-test-cases.md')
  if(@([regex]::Matches($caseDoc,'(?m)^## Case \d+: ')).Count -ne $cases.Count) {$errors += 'Scenario Markdown and JSON case counts differ'}
}
if($errors.Count) {$errors | Write-Error; exit 1}
Write-Output "Validated $($routeLines.Count) scenario routes and $($skillNames.Count) skills."
