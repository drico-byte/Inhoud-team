<#
    Wolkskool content pipeline - one-shot setup for a new Windows 11 machine.

    Run this from inside the cloned repository. It does not clone: that needs an
    interactive login, and by the time you can run this file you have already
    cloned.

    Everything here is safe to run twice. Each step checks before it acts, so a
    re-run after fixing one problem does not reinstall the things that worked.
#>

$ErrorActionPreference = 'Stop'
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

Say-Head '1. Python'

if (-not (Have 'python')) {
    if (Have 'py') {
        Say-Ok 'Python present through the py launcher'
        $Py = 'py'
    } else {
        Say-Do 'installing Python'
        winget install --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements | Out-Null
        Refresh-Path
        if (Have 'python')   { $Py = 'python' }
        elseif (Have 'py')   { $Py = 'py' }
        else {
            Say-Bad 'Python installed but is still not on PATH - close this window, open a new one, and run this script again'
            Write-Host ''
            exit 1
        }
        Say-Ok "installed Python ($(& $Py --version 2>&1))"
    }
} else {
    $Py = 'python'
    Say-Ok "Python $(& $Py --version 2>&1)"
}

# --- 2. Python packages -----------------------------------------------------

Say-Head '2. Python packages'

foreach ($mod in 'pyphen', 'spylls') {
    & $Py -c "import $mod" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Say-Ok "$mod"
    } else {
        Say-Do "installing $mod"
        & $Py -m pip install --quiet --disable-pip-version-check $mod
        & $Py -c "import $mod" 2>$null
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
