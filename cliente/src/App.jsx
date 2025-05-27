import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ChatBot from './components/ChatBot';
import Agendamento from './pages/Agendamento';

function App() {
  return (
    <Routes>
      <Route path="/" element={<ChatBot />} />
      <Route path="/agendamento" element={<Agendamento />} />
      {/* Redireciona qualquer rota desconhecida para a home */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;