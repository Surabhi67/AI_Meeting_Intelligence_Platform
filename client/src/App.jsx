import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import { Dashboard } from './pages/Dashboard'
import { Meetingcard } from './components/Meetingcard'
import { Login } from './pages/Login'

function App() {

  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path = "/dashboard" element = { <Dashboard />}/>
      <Route path = "/meeting" element = {<Meeting/> }/>
    </Routes>
  )
}

export default App
