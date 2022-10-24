import * as React from 'react';
import { useState, useEffect } from 'react';
import ErrorBoundary from '../error-boundary/error-boundary';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import AppHeader from '../app-header/app-header';
import appStyles from './app.module.css';

function App() {
  const [ loggedIn, setLoggedIn ] = useState(null);

  // if (loggedIn === null) {
  //   return <div className={appStyles.loading}>Loading!!</div>
  // }

  return (
    <ErrorBoundary>
      <div>
        <Router>
          <AppHeader />
        </Router>
      </div>
    </ErrorBoundary>
  )
}

export default App;