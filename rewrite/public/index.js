import { render } from 'https://cdn.skypack.dev/preact'
import { html } from 'https://cdn.skypack.dev/htm/preact'
import { fetchProjectData, header } from './js/common.js'

const App = ({ project }) => html`
  <div>
    <${header} project=${project} />
    <ul>
      <li><a href="/projects.html">Change Current Project</a></li>
      <li><a href="/open-folder.html">Open Folder In Explorer</a></li>
      <li><a href="/rename-files.html">Rename Videos</a></li>
      <li><a href="/generate-csv.html">Create Edit Data</a></li>
      <li><a href="/edit-csv.html">Edit Data</a></li>
      <li><a href="/trim-videos.html">Trim Videos</a></li>
      <li>
        <a href="/move-trimmed-to-upscaled.html"
          >Bypass Upscale (Or AI Upscale Videos into /upscale)</a
        >
      </li>
      <li><a href="/combine-videos.html">Combine into Final Video</a></li>
      <li><a href="/inject-video.html">Inject Metadata</a></li>
    </ul>
  </div>
`
fetchProjectData()
  .then(project => render(html`<${App} project=${project}/>`, document.getElementById('app')))
