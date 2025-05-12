import "./Cadastro.css";
import cadastroSubtitulo from "../../assets/cadastroSubtitulo.svg";
import PropTypes from "prop-types";

const Cadastro = ({ onFechar }) => {
  return (
    <div>
      <div className="backdrop" onClick={onFechar}></div>
      <div className="cartao-cadastro modal-cadastro">
        <div className="subtitulo-cadastro">
          <img src={cadastroSubtitulo} alt="Subtítulo" />
        </div>

        <form className="formulario-cadastro">
          <div className="inputs-cadastro">
            <input type="text" name="nome" placeholder="nome" />
            <input type="email" name="email" placeholder="e-mail" />
            <input type="password" name="senha" placeholder="senha" />
            <input type="password" name="confirmacao" placeholder="confirmar senha" />
          </div>
        </form>
        <div>
          <button className="botao-cadastro">Cadastrar</button>
          <button onClick={onFechar} className="fechar-cadastro">X</button>
        </div>
      </div>
    </div>
  );
};

Cadastro.propTypes = {
  onFechar: PropTypes.func.isRequired,
};

export default Cadastro;
