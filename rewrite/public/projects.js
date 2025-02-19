import { render, Component } from 'https://cdn.skypack.dev/preact'
import { html } from 'https://cdn.skypack.dev/htm/preact'

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

render(html`<${App} />`, document.getElementById('app'))