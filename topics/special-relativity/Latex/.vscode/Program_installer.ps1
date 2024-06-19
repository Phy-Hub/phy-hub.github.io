[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# Chocolatey installs
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.WebRequest]::Create("https://community.chocolatey.org/install.ps1").UseDefaultCredentials=[System.Net.WebRequest]::Create("https://community.chocolatey.org/install.ps1").UseDefaultCredentials=$true; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

choco install vscode -y
choco install python -y
choco install git -y

choco install miktex -y
choco install strawberryperl -y

choco install inkscape -y
choco install ghostscript -y

# pdf2svg install
git clone https://github.com/jalios/pdf2svg-windows.git pdf2svg
add C:\pdf2svg\dist-64bits; to PATH
