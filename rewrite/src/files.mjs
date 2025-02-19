import fs from 'fs/promises'
import path from 'path'

export const sendFile = async (filePath, res) => {
  console.log(`Sending file: ${filePath}`)
  try {
    await fs
      .access(filePath)
      .then(() => {
        res.sendFile(filePath)
      })
      .catch(() => {
        res.status(404).send('File Not found')
      })
  } catch (err) {
    console.error(err)
    res.status(500).send('Internal Server Error')
  }
}

export const sendRequestFile = (root) => async (req, res) => {
  const requestPath = req.path === '/' ? '/index.html' : req.path
  const filePath = path.join(
    path.normalize(root),
    requestPath
  )

  sendFile(filePath, res)  
}
