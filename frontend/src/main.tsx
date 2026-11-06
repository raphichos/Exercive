/**
 * Frontend entry point: mounts the React app into the `#root` element of index.html.
 *
 * StrictMode runs extra checks in development only (for example, it renders components
 * twice to surface side effects). It has no effect on the production build.
 */
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import App from './App';
import './styles/index.css';

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error('index.html is missing the #root element');
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
