import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import { Dashboard } from './pages/Dashboard'
import { Login } from './pages/Login'
import { Meeting } from './pages/Meeting'
import { Route, Routes, Navigate } from 'react-router-dom'

function App() {

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path = "/dashboard" element = { <Dashboard />}/>
      <Route path = "/meeting" element = {<Meeting/> }/>
      <Route path = "/login" element = {<Login />} />
    </Routes>
  )
}

export default App
