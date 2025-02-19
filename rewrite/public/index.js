import { render } from 'https://cdn.skypack.dev/preact'
import { html } from 'https://cdn.skypack.dev/htm/preact'

const App = () => html`
  <div>
    <h1>Hello World</h1>
  </div>
`

render(html`<${App} />`, document.getElementById('app'))