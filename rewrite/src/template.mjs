export const sendHTMLPage = (titleMap) => (req, res) => {
  const requestPath = req.path === '/' ? '/index.html' : req.path
  const pageName = requestPath.replace('/', '').replace('.html', '')
  res.send(`
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>VR180 Express Editor: ${titleMap[pageName]}</title>
        <link rel="stylesheet" href="css/styles.css" />
      </head>
      <body>
        <div id="app"></div>
        <script type="module" src="${pageName}.js"></script>
      </body>
    </html>
  `)
}