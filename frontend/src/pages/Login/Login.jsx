import "./Login.css";
import logo from "../../assets/logo.svg";
import sensingFI from "../../assets/SensingFI.svg";
import userCircle from "../../assets/user-circle.svg";
import lockClosed from "../../assets/lock-closed.svg";

const Login = () => {
  return (
    <div className="cartao">
      <div className="logo">
        <img src={logo} alt="Logo" />
        <img src={sensingFI} alt="SensingFI" />
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
          <button type="submit" className="botao">
            Entrar
          </button>
        </div>
        <div>
          <span className="usuario-novo">Usuário novo? </span>
          <a href="/cadastro" className="cadastro">
            Cadastre-se
          </a>
        </div>
      </form>
      <div className="esqueceu-senha">
        <a href="#" className="esqueceu-senha">
          esqueceu sua senha?
        </a>
      </div>
    </div>
  );
};

export default Login;
