$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add('http://localhost:8081/')
$listener.Start()
$root = 'D:\Application\AllToolsSet\Herb\Smart-Chinese-Herbal-Medicine-Recognition-App'
Write-Host "Server started at http://localhost:8081/"
while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    $rawUrl = $request.RawUrl
    if ($rawUrl -eq '/') { $rawUrl = '/index.html' }
    $path = Join-Path $root ($rawUrl -replace '^/', '')
    $safePath = [System.IO.Path]::GetFullPath($path)
    if (-not $safePath.StartsWith($root)) {
        $response.StatusCode = 403
        $response.Close()
        continue
    }
    if (Test-Path $safePath -PathType Leaf) {
        $content = [System.IO.File]::ReadAllBytes($safePath)
        $ext = [System.IO.Path]::GetExtension($safePath).ToLower()
        $mime = switch ($ext) {
            '.html' { 'text/html' }
            '.css'  { 'text/css' }
            '.js'   { 'application/javascript' }
            '.jpg'  { 'image/jpeg' }
            '.jpeg' { 'image/jpeg' }
            '.png'  { 'image/png' }
            '.mp4'  { 'video/mp4' }
            default { 'application/octet-stream' }
        }
        $response.ContentType = $mime
        $response.ContentLength64 = $content.Length
        $response.OutputStream.Write($content, 0, $content.Length)
    } else {
        $response.StatusCode = 404
    }
    $response.Close()
}
