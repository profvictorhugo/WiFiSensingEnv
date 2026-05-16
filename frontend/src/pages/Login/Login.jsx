import "./Login.css";
import { useState } from "react";
import Cadastro from "../../components/Cadastro/Cadastro";
import tituloLogo from "../../assets/titulo-logo.svg";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLock, faUser } from "@fortawesome/free-solid-svg-icons";

const Login = () => {
  const [mostrarCadastro, setMostrarCadastro] = useState(false);
  return (
    <div className="login-page">
      <div className="login-shell">
        <section className="login-hero">
          <div className="login-hero-content">
            <div className="login-hero-badge">
              <img src={tituloLogo} alt="SensingFI" />
            </div>
            <h1 className="login-hero-title">Gerenciamento de dados</h1>
            <p className="login-hero-subtitle">
              Visualize presença e movimentação em tempo real com análise de sinais Wi-Fi.
            </p>
            <ul className="login-hero-list">
              <li>Monitore suas capturas</li>
              <li>Alinhe seus dados em um único lugar</li>
            </ul>
          </div>
          <div className="login-hero-glow" aria-hidden="true" />
        </section>
        <section className="login-panel">
          <div className="login-panel-header reveal-1">
            <span className="login-panel-eyebrow">Acesso seguro</span>
            <h2 className="login-title">Acesse sua conta</h2>
            <p className="login-subtitle">Entre com seus dados para continuar.</p>
          </div>
          <form className="login-form reveal-2">
            <label className="input-group">
              <span className="input-icon">
                <FontAwesomeIcon icon={faUser} aria-hidden="true" />
              </span>
              <input className="login-input" type="email" name="email" placeholder="E-mail" />
            </label>
            <label className="input-group">
              <span className="input-icon">
                <FontAwesomeIcon icon={faLock} aria-hidden="true" />
              </span>
              <input className="login-input" type="password" name="senha" placeholder="Senha" />
            </label>
            <button type="submit" className="botao-login">
              Entrar
            </button>
          </form>
          <div className="login-links reveal-3">
            <span className="usuario-novo">Usuario novo?</span>
            <button
              type="button"
              className="cadastro"
              onClick={() => setMostrarCadastro(true)}
            >
              Cadastre-se
            </button>
          </div>
          <a href="#" className="esqueceu-senha reveal-4">
            Esqueceu sua senha?
          </a>
        </section>
      </div>
      {mostrarCadastro && <Cadastro onFechar={() => setMostrarCadastro(false)} />}
    </div>
  );
};

export default Login;
