// src/App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { NavBar } from './components/layout/NavBar';
import { Footer } from './components/layout/Footer';
import { Landing } from './pages/Landing';
import { Simulate } from './pages/Simulate';
import { Results } from './pages/Results';
import { About } from './pages/About';
import { NotFound } from './pages/NotFound';

export function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-[#111125] text-[#e2e0fc]">
        <NavBar />
        <div className="flex-1">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/simulate" element={<Simulate />} />
            <Route path="/simulate/:jobId" element={<Results />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </BrowserRouter>
  );
}
