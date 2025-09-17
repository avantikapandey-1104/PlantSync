import React from 'react';
import HomePage from './components/HomePage';
import UploadImagePage from './components/UploadImagePage';
import PlantManagement from './components/PlantManagement';
import Notifications from './components/Notifications';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-green-50">
        <nav className="bg-green-600 text-white p-4">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold">🌿 PlantSync</h1>
            <div className="space-x-4">
              <Link to="/" className="hover:text-green-200">Home</Link>
              <Link to="/upload" className="hover:text-green-200">Upload Image</Link>
            </div>
          </div>
        </nav>

        <main className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/upload" element={<UploadImagePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
