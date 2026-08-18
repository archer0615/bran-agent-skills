[CmdletBinding()] param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$scenarioPath=Join-Path $root 'references/skill-scenarios.md'
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
if($errors.Count) {$errors | Write-Error; exit 1}
Write-Output "Validated $($routeLines.Count) scenario routes and $($skillNames.Count) skills."
