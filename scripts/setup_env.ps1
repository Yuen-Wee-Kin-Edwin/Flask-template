# Check and copy environment files in Windows PowerShell

# Set working directory to project root (parent of scripts)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location (Join-Path $ScriptDir "..")

# Define mappings of target to source
$files = @{
    ".env" = ".env.example"
    ".env.production" = ".env.production.example"
}

foreach ($target in $files.Keys)
{
    $source = $files[$target]

    if (Test-Path $target)
    {
        Write-Host "$target already exists. Skipping creation."
    }
    elseif (Test-Path $source)
    {
        Copy-Item -Path $source -Destination $target
        Write-Host "Created $target from $source."
    }
    else
    {
        Write-Error "Error: $source not found. Cannot create $target."
    }
}