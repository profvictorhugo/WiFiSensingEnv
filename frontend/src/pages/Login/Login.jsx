import "./Login.css";
import { useState } from "react";
import Cadastro from "../../components/Cadastro/Cadastro";
import tituloLogo from "../../assets/titulo-logo.svg";
import userCircle from "../../assets/user-circle.svg";
import lockClosed from "../../assets/lock-closed.svg";

const Login = () => {
  const [mostrarCadastro, setMostrarCadastro] = useState(false);
  return (
    <div>
      <div className="cartao-login">
        <div className="logo">
          <img src={tituloLogo} alt="Logo" />
        </div>
        <form>
          <div className="email-senha">
            <span className="icon">
              <img src={userCircle} alt="User Icon" />
            </span>
            <input type="email" name="email" placeholder="e-mail" />
          </div>
          <div className="email-senha">
            <span className="icon">
              <img src={lockClosed} alt="Lock Icon" />
            </span>
            <input type="password" name="senha" placeholder="senha" />
          </div>
          <div>
            <button type="submit" className="botao-login">
              Entrar
            </button>
          </div>
          <div>
            <span className="usuario-novo">Usuário novo? </span>
            <a className="cadastro" onClick={() => setMostrarCadastro(true)}>
              Cadastre-se
            </a>
            
          </div>
        </form>
        <div className="esqueceu-senha">
          <a href="#" className="esqueceu-senha">
            Esqueceu sua senha?
          </a>
        </div>
      </div>
      {mostrarCadastro && 
        <Cadastro onFechar={() => setMostrarCadastro(false)} />
      }
    </div>
  );
};

export default Login;
