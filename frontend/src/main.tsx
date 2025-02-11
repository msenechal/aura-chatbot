import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import '@neo4j-ndl/base/lib/neo4j-ds-styles.css';

const allowedReferrer = "https://sites.google.com";

if (!document.referrer || !document.referrer.startsWith(allowedReferrer)) {
  document.body.innerHTML = "<h1>Access Forbidden</h1>";
  throw new Error("Access Forbidden");
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
