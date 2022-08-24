import * as React from 'react';
import ErrorBoundary from '../error-boundary/error-boundary';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {

  return (
    <ErrorBoundary>
      <div>
        <Router>
          
        </Router>
      </div>
    </ErrorBoundary>
  )
}

export default App;