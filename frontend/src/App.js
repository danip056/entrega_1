import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import Login from './pages/Login';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './pages/Navbar'
import { SingUp } from './pages/SingUp';
import { Tasks } from './pages/Tasks'
import SingOut from './pages/SingOut';

function App() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setToken(token);
  }, []);

  const updateToken = (newToken) => {
    setToken(newToken);
    localStorage.setItem('token', newToken);
  };

  return (
    <Router>
      <Navbar />
      <div>
        <Routes>
          <Route exact path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/singup" element={<SingUp />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/singout" element={<SingOut />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
