import express from 'express'
import fs from 'fs/promises'
import path from 'path'

import { sendRequestFile } from './src/files.mjs'
import { sendHTMLPage } from './src/template.mjs'

import {
  MODULE_MAP,
  PAGE_TITLE_MAP,
  PROJECT_FOLDER_PATTERN,
} from './src/consts.mjs'

const app = express()
const __dirname = path.resolve()

async function start() {
  try {
    const configRaw = await fs.readFile('config.json', 'utf-8')
    const config = JSON.parse(configRaw)

    app.route('/api/projects').get((req, res) => {
      fs.readdir(config.root)
        .then((files) =>
          files.filter((file) => {
            return fs
              .stat(path.join(config.root, file))
              .then((stat) => stat.isDirectory())
          })
        )
        .then((files) =>
          files.filter((file) => PROJECT_FOLDER_PATTERN.test(file))
        )
        .then((files) => res.json({ projects: files }))
        .catch((err) => {
          res.status(500).send('Internal Server Error')
        })
    })

    app.route('/api/config').post(express.json(), (req, res) => {
      const { current } = req.body
      fs.writeFile('config.json', JSON.stringify({ ...config, current })).then(
        () => {
          config.current = current
          res.json(config)
        }
      )
    })

    app.route('/api/project').get((req, res) => {
      res.json({ id: config.current })
    })

    const sendPage = sendHTMLPage(PAGE_TITLE_MAP)
    const sendFile = sendRequestFile(path.join(__dirname, 'public'))

    app.get('/*', (req, res) => {
      if (req.path === '/') {
        if (!config.current) {
          res.redirect('/projects.html')
          return
        }
        sendPage(req, res)
      } else if (req.path.endsWith('.html')) {
        sendPage(req, res)
      } else {
        sendFile(req, res)
      }
    })

    app.listen(config.port, () => {
      console.log(`Example app listening at http://localhost:${config.port}`)
    })
  } catch (err) {
    console.error(err)
  }
}

start()
