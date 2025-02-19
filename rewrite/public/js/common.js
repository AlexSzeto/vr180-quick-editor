import { html } from 'https://cdn.skypack.dev/htm/preact'

export const fetchProjectData = async () => 
  fetch('/api/project')
  .then((res) => res.json())

export const header = ({ project }) => html`
  <header>
    <h1>Current Project</h1>
    <h2>${project.id}</h2>
  </header>
`