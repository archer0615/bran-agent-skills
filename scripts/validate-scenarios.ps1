[CmdletBinding()] param()
$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$scenarioPath=Join-Path $root 'references/skill-scenarios.md'
$skillNames=@{}
Get-ChildItem (Join-Path $root 'skills') -Recurse -Filter SKILL.md | ForEach-Object {$skillNames[$_.Directory.Name]=$true}
$lines=Get-Content $scenarioPath
$routeLines=$lines | Where-Object {$_ -match '^\s*`[^`]+`' -and $_ -notmatch '^\s*#'}
$errors=@()
foreach($line in $routeLines) { foreach($match in [regex]::Matches($line,'`([^`]+)`')) { $name=$match.Groups[1].Value; if(-not $skillNames.ContainsKey($name)) {$errors += "Unknown skill in scenario route: $name"} } }
if($errors.Count) {$errors | Write-Error; exit 1}
Write-Output "Validated $($routeLines.Count) scenario routes and $($skillNames.Count) skills."
