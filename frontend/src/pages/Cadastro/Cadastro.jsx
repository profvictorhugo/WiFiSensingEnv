import "./Cadastro.css";
import logo from "../../assets/logo.svg";
import sensingFI from "../../assets/SensingFI.svg";

const Cadastro = () => {
  return (
    <div className="cartao-cadastro">
      <div className="logo">
        <img src={logo} alt="Logo" />
        <img src={sensingFI} alt="SensingFI" />
      </div>
      <form className="formulario-cadastro">
        <div className="nome-email-cadastro">
          <input type="text" name="nome" placeholder="Nome" />
          <input type="email" name="email" placeholder="E-mail" />
        </div>
        <div className="barrinha-verde"></div>
        <div className="senha-confirmar-cadastro">
          <input type="password" name="senha" placeholder="Senha" />
          <input
            type="password"
            name="confirmacao"
            placeholder="Confirmar senha"
          />
        </div>
      </form>
      <div>
        <button className="botao-cadastro">Cadastrar</button>
      </div>
    </div>
  );
};
export default Cadastro;
