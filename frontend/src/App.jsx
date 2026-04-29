import Login from "./pages/Login/Login.jsx";
import Home from "./pages/Home/Home.jsx";
import Usuarios from "./pages/Usuarios/Usuarios.jsx";
import Datasets from "./pages/Datasets/Datasets.jsx";
import DatasetDetalhe from "./pages/DatasetDetalhe/DatasetDetalhe.jsx";
import Modelos from "./pages/Modelos/Modelos.jsx";
import Configuracoes from "./pages/Configuracoes/Configuracoes.jsx";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/home" element={<Home />} />
        <Route path="/usuarios" element={<Usuarios />} />
        <Route path="/datasets" element={<Datasets />} />
        <Route path="/datasets/:datasetId" element={<DatasetDetalhe />} />
        <Route path="/modelos" element={<Modelos />} />
        <Route path="/modelos/:modeloId" element={<Modelos />} />
        <Route path="/configuracoes" element={<Configuracoes />} />
      </Routes>
    </div>
  );
}

export default App;
