# Check status of Streamlit and Next.js processes (PowerShell)

Write-Host "Checking Streamlit processes..."
Get-Process python* -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*streamlit*" } | Format-Table Id, ProcessName, CPU, StartTime -AutoSize

Write-Host "`nChecking Next.js (node) processes..."
Get-Process node* -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*next*" } | Format-Table Id, ProcessName, CPU, StartTime -AutoSize

Write-Host "`nList of listening ports (useful to see services)"
Get-NetTCPConnection -State Listen | Select-Object LocalAddress, LocalPort, OwningProcess | Sort-Object LocalPort | Format-Table -AutoSize
