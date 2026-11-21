param()
$ErrorActionPreference = 'Stop'
$script = Join-Path $PSScriptRoot 'project_checks.py'
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 $script
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $script
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python $script
} else {
    throw 'Python 3.10+ is required for portable repository checks.'
}
exit $LASTEXITCODE
