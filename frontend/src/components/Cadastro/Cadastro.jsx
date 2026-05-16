import "./Cadastro.css";
import cadastroSubtitulo from "../../assets/cadastroSubtitulo.svg";
import PropTypes from "prop-types";

const Cadastro = ({ onFechar }) => {
  return (
    <div className="cadastro-layer" role="dialog" aria-modal="true">
      <div className="backdrop" onClick={onFechar} />
      <div className="cartao-cadastro modal-cadastro">
        <button type="button" onClick={onFechar} className="fechar-cadastro" aria-label="Fechar cadastro">
          X
        </button>
        <div className="cadastro-header">
          <div className="subtitulo-cadastro">
            <img src={cadastroSubtitulo} alt="Cadastro" />
          </div>
          <h2 className="cadastro-title">Criar conta</h2>
          <p className="cadastro-subtitle">Preencha os campos para comecar.</p>
        </div>
        <form className="formulario-cadastro">
          <div className="inputs-cadastro">
            <input type="text" name="nome" placeholder="Nome" />
            <input type="email" name="email" placeholder="E-mail" />
            <input type="password" name="senha" placeholder="Senha" />
            <input type="password" name="confirmacao" placeholder="Confirmar senha" />
          </div>
          <button type="submit" className="botao-cadastro">Cadastrar</button>
        </form>
      </div>
    </div>
  );
};

Cadastro.propTypes = {
  onFechar: PropTypes.func.isRequired,
};

export default Cadastro;
