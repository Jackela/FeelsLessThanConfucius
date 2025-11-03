Param(
  [Parameter(Mandatory=$false)] [string]$Source = "specs/1-confucian-rag-agent/contracts/openapi.yaml",
  [Parameter(Mandatory=$false)] [string]$Out = "docs/openapi.yaml"
)

Write-Host "Syncing OpenAPI from $Source to $Out"
if (!(Test-Path $Source)) { throw "OpenAPI file not found: $Source" }
Copy-Item -Force $Source $Out
Write-Host "Done."

