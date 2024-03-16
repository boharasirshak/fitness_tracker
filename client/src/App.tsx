import { useEffect } from 'react';
import './App.css';

function App() {
  useEffect(() => {
    let accessToken = localStorage.getItem("access_token");
    let refreshToken = localStorage.getItem("refresh_token");

    if (!accessToken || !refreshToken) {
      window.location.href = "/login";
    }
  
  });
  useEffect(() => {});

  return <></>
}

export default App
