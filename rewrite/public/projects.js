import { render, Component } from 'https://cdn.skypack.dev/preact'
import { html } from 'https://cdn.skypack.dev/htm/preact'
import { fetchProjectData, header } from './js/common.js'

class App extends Component {
  constructor() {
    super()
    this.state = {
      projects: []
    }
  }

  componentDidMount() {
    fetch('/api/projects')
    .then(res => res.json())
    .then(({ projects }) => this.setState({ projects }))
  }

  setProject(project) {
    fetch('/api/config', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ current: project })
    }).then(() => {
      window.location.href = '/'
    })
  }

  render() {
    return html`
      <${header} project=${this.props.project} />
      <div>
        <ul>
          ${this.state.projects.map(project => html`
            <li onClick=${() => this.setProject(project)}>
            ${project}
            </li>
          `)}
        </ul>
      </div>
    `
  }
}

fetchProjectData()
  .then(project => render(html`<${App} project=${project} />`, document.getElementById('app')))