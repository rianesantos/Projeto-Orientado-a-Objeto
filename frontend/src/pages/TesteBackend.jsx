import { useEffect, useState } from "react";
import axios from "axios";

function TesteBackend() {
  const [msg, setMsg] = useState("Conectando...");

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/ping") // use 127.0.0.1 em vez de localhost
      .then(res => setMsg(res.data.message))
      .catch(err => {
        console.error("Erro ao conectar com o backend:", err);
        setMsg("Erro ao conectar com o backend");
      });
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white">Teste de conexão:</h1>
      <p className="text-purple-400 mt-2">{msg}</p>
    </div>
  );
}

export default TesteBackend;
