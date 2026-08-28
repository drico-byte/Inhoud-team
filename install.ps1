<#
    Wolkskool content pipeline - one-shot setup for a new Windows 11 machine.

    Run this from inside the cloned repository. It does not clone: that needs an
    interactive login, and by the time you can run this file you have already
    cloned.

    Everything here is safe to run twice. Each step checks before it acts, so a
    re-run after fixing one problem does not reinstall the things that worked.
#>

# NOT 'Stop'. In PowerShell 5.1 a native command writing to stderr becomes a
# terminating error, so probing for a missing module would kill the script.
# Every step below checks $LASTEXITCODE explicitly instead.
$ErrorActionPreference = 'Continue'
$script:Problems = @()

# --- output -----------------------------------------------------------------

function Say-Head($text) {
    Write-Host ''
    Write-Host $text -ForegroundColor Cyan
    Write-Host ('-' * $text.Length) -ForegroundColor DarkCyan
}
function Say-Ok($text)   { Write-Host '  ok    ' -ForegroundColor Green -NoNewline; Write-Host $text }
function Say-Do($text)   { Write-Host '  ...   ' -ForegroundColor DarkGray -NoNewline; Write-Host $text }
function Say-Warn($text) { Write-Host '  note  ' -ForegroundColor Yellow -NoNewline; Write-Host $text }
function Say-Bad($text)  {
    Write-Host '  FAIL  ' -ForegroundColor Red -NoNewline; Write-Host $text
    $script:Problems += $text
}

# Installers write to the machine PATH, but this shell was started with the old
# one. Without this, a tool installed a moment ago is still "not recognised".
function Refresh-Path {
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user    = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = ($machine, $user | Where-Object { $_ }) -join ';'
}

function Have($name) { [bool](Get-Command $name -ErrorAction SilentlyContinue) }

# --- 0. where are we --------------------------------------------------------

Say-Head 'Wolkskool content pipeline - setup'

$Repo = $PSScriptRoot
if (-not (Test-Path (Join-Path $Repo 'bin\opstel.py'))) {
    Say-Bad "this script must sit in the repository root; bin\opstel.py is not next to it"
    Write-Host ''
    exit 1
}
Set-Location $Repo
Say-Ok "repository: $Repo"

if (-not (Have 'winget')) {
    Say-Bad 'winget is not available - this needs Windows 11 or a current Windows 10'
    Write-Host '        Install the prerequisites by hand instead; see SETUP.html.'
    Write-Host ''
    exit 1
}

# --- 1. Python --------------------------------------------------------------
# Windows 11 ships a stub python.exe in WindowsApps whose only job is to
# advertise the Microsoft Store. It exists, so "is there a python command" says
# yes, and then every call prints "Python was not found". So Python is proved by
# running it, never by the command existing.

function Test-PythonExe($exe) {
    if (-not $exe) { return $false }
    try {
        $out = & $exe -c "import sys; sys.stdout.write('okpy')" 2>&1
        return ($LASTEXITCODE -eq 0 -and "$out" -match 'okpy')
    } catch { return $false }
}

function Find-Python {
    foreach ($c in 'python', 'py') {
        $cmd = Get-Command $c -ErrorAction SilentlyContinue
        if (-not $cmd) { continue }
        if ($cmd.Source -like '*\WindowsApps\*') { continue }   # the store stub
        if (Test-PythonExe $cmd.Source) { return $cmd.Source }
    }
    # PATH can be stale or shadowed by the stub, so look where it actually lands.
    $roots = @(
        (Join-Path $env:LOCALAPPDATA 'Programs\Python'),
        (Join-Path $env:LOCALAPPDATA 'Python'),
        (Join-Path $env:ProgramFiles 'Python312'),
        (Join-Path $env:ProgramFiles 'Python311'),
        (Join-Path $env:ProgramFiles 'Python310')
    )
    foreach ($r in $roots) {
        if (-not (Test-Path $r)) { continue }
        $exe = Join-Path $r 'python.exe'
        if ((Test-Path $exe) -and (Test-PythonExe $exe)) { return $exe }
        foreach ($d in (Get-ChildItem $r -Directory -ErrorAction SilentlyContinue | Sort-Object Name -Descending)) {
            $exe = Join-Path $d.FullName 'python.exe'
            if ((Test-Path $exe) -and (Test-PythonExe $exe)) { return $exe }
        }
    }
    return $null
}

Say-Head '1. Python'

$Py = Find-Python

if (-not $Py) {
    Say-Do 'installing Python'
    winget install --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Refresh-Path
    $Py = Find-Python
}

if (-not $Py) {
    Say-Bad 'Python is still not usable'
    Write-Host ''
    Write-Host '        Almost always the Microsoft Store alias. Turn it off:' -ForegroundColor Yellow
    Write-Host '          Settings > Apps > Advanced app settings > App execution aliases'
    Write-Host '          switch OFF python.exe and python3.exe'
    Write-Host ''
    Write-Host '        Then close this window, open a new one, and run install.bat again.'
    Write-Host ''
    exit 1
}

Say-Ok "Python: $Py  ($(& $Py --version 2>&1))"

# --- 2. Python packages -----------------------------------------------------

Say-Head '2. Python packages'

foreach ($mod in 'pyphen', 'spylls') {
    $null = & $Py -c "import $mod" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Say-Ok "$mod"
    } else {
        Say-Do "installing $mod"
        $null = & $Py -m pip install --quiet --disable-pip-version-check $mod 2>&1
        $null = & $Py -c "import $mod" 2>&1
        if ($LASTEXITCODE -eq 0) { Say-Ok "$mod" } else { Say-Bad "could not install $mod" }
    }
}

# --- 3. Tesseract and Poppler ----------------------------------------------

Say-Head '3. OCR tools'

if (Have 'tesseract') {
    Say-Ok "tesseract: $((Get-Command tesseract).Source)"
} else {
    Say-Do 'installing Tesseract (this one takes a minute)'
    winget install --id UB-Mannheim.TesseractOCR --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Refresh-Path
    if (Have 'tesseract') { Say-Ok "tesseract: $((Get-Command tesseract).Source)" }
    else { Say-Bad 'Tesseract installed but is not on PATH - reopen PowerShell and run this again' }
}

if ((Have 'pdftoppm') -and (Have 'pdfinfo')) {
    Say-Ok "poppler: $((Get-Command pdftoppm).Source)"
} else {
    Say-Do 'installing Poppler'
    winget install --id oschwartz10612.Poppler --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Refresh-Path
    if ((Have 'pdftoppm') -and (Have 'pdfinfo')) { Say-Ok 'poppler installed' }
    else { Say-Bad 'Poppler installed but pdftoppm/pdfinfo are not on PATH - reopen PowerShell and run this again' }
}

# --- 4. Tesseract language data --------------------------------------------
# The installer offers these as tickboxes and they are easy to miss, which is
# why they are fetched here rather than trusted.

Say-Head '4. Afrikaans language data'

if (Have 'tesseract') {
    $tessDir = Split-Path (Get-Command tesseract).Source -Parent
    $tessdata = Join-Path $tessDir 'tessdata'
    if (-not (Test-Path $tessdata)) { New-Item -ItemType Directory -Path $tessdata -Force | Out-Null }

    foreach ($lang in 'afr', 'osd') {
        $file = Join-Path $tessdata "$lang.traineddata"
        if (Test-Path $file) {
            Say-Ok "$lang"
        } else {
            Say-Do "downloading $lang"
            try {
                Invoke-WebRequest -UseBasicParsing `
                    -Uri "https://github.com/tesseract-ocr/tessdata/raw/main/$lang.traineddata" `
                    -OutFile $file
                Say-Ok "$lang"
            } catch {
                Say-Bad "could not download $lang.traineddata - put it in $tessdata by hand"
            }
        }
    }
} else {
    Say-Warn 'skipped, because Tesseract is not available yet'
}

# --- 5. the source documents ------------------------------------------------
# Textbooks and curriculum PDFs are deliberately not in git; they come off
# SharePoint and get copied in by hand. This only checks and reports, because
# a copy is a ten-second drag and a script that goes hunting through OneDrive
# is slow, and wrong the moment the library is reorganised.

Say-Head '5. Textbooks and curriculum documents'

$wantBronne = 17
$wantKaps   = 31

function Count-Files($path) {
    if (Test-Path $path) { (Get-ChildItem $path -Recurse -File -ErrorAction SilentlyContinue).Count } else { 0 }
}

$haveBronne = Count-Files (Join-Path $Repo 'bronne')
$haveKaps   = Count-Files (Join-Path $Repo 'kaps\dokumente')

if ($haveBronne -ge $wantBronne) {
    Say-Ok "textbooks: $haveBronne files"
} elseif ($haveBronne -eq 0) {
    Say-Bad "no textbooks yet - copy them from SharePoint into  $Repo\bronne\Intersen\  ($wantBronne PDFs)"
} else {
    Say-Warn "only $haveBronne of $wantBronne textbooks - OneDrive may still be downloading, or some are missing"
}

if ($haveKaps -ge $wantKaps) {
    Say-Ok "curriculum documents: $haveKaps files"
} elseif ($haveKaps -eq 0) {
    Say-Bad "no curriculum documents yet - copy them from SharePoint into  $Repo\kaps\dokumente\  (3 subfolders, $wantKaps PDFs)"
} else {
    Say-Warn "only $haveKaps of $wantKaps curriculum documents - OneDrive may still be downloading, or some are missing"
}

# --- 6. the project's own setup --------------------------------------------
# This is the step that links the content standard and the memory notes into
# the places Claude Code reads. Nothing errors without it; the work is just
# quietly done without the standard.

Say-Head '6. Linking the standard and the memory notes'

& $Py (Join-Path $Repo 'bin\opstel.py')
if ($LASTEXITCODE -ne 0) { Say-Bad 'bin\opstel.py reported a problem - read its output above' }

# --- 7. does the pipeline actually run --------------------------------------

Say-Head '7. Proving it works'

$out = & $Py (Join-Path $Repo 'bin\hardloop.py') `
    --vak 'Natuurwetenskappe en Tegnologie' --graad 4 `
    --subonderwerp 'Sterk raamstrukture' --les 1 2>&1 | Out-String

if ($out -match 'GEWEIER|Traceback') {
    Say-Bad 'the pipeline refused to run on an approved lesson'
    Write-Host ($out.Trim() -split "`n" | Select-Object -Last 8 | ForEach-Object { "        $_" }) -Separator "`n"
} else {
    Say-Ok 'the pipeline runs against an already-approved lesson'
}

# --- done -------------------------------------------------------------------

Write-Host ''
if ($script:Problems.Count -eq 0) {
    Write-Host '  Ready. Open Claude Code in this folder and read SETUP.html if anything surprises you.' -ForegroundColor Green
} else {
    Write-Host "  $($script:Problems.Count) thing(s) still need attention:" -ForegroundColor Yellow
    foreach ($p in $script:Problems) { Write-Host "    - $p" }
    Write-Host ''
    Write-Host '  Fix those and run this again - it skips whatever already worked.'
}
Write-Host ''

# Say plainly whether this worked. Without it the script inherits whatever exit
# code the last program happened to set, and reports failure after succeeding.
if ($script:Problems.Count -eq 0) { exit 0 } else { exit 1 }
