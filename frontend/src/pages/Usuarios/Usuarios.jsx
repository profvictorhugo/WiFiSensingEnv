import './Usuarios.css';
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPenToSquare, faTrashCan } from '@fortawesome/free-solid-svg-icons';
import logo from '../../assets/logo.svg';

const Usuarios = () => {
  const [usuarios, setUsuarios] = useState([
    { nome: 'Teste', email: 'teste@gmail.com', permissao: 'Admin' }
  ]);
  const [mostrarModal, setMostrarModal] = useState(false);
  const [formValues, setFormValues] = useState({
    nome: '',
    email: '',
    permissao: 'Admin'
  });
  const [editIndex, setEditIndex] = useState(null);
  const [editValues, setEditValues] = useState({ nome: '', permissao: 'Admin' });
  const usuarioAtual = { permissao: 'Admin' };

  const permissoes = ['Admin', 'Editor', 'Visualizador'];

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormValues((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setMostrarModal(false);
  };

  const iniciarEdicao = (index) => {
    if (usuarioAtual.permissao !== 'Admin') {
      return;
    }
    const usuario = usuarios[index];
    setEditIndex(index);
    setEditValues({ nome: usuario.nome, permissao: usuario.permissao });
  };

  const salvarEdicao = (index) => {
    setUsuarios((prev) =>
      prev.map((usuario, idx) =>
        idx === index
          ? { ...usuario, nome: editValues.nome, permissao: editValues.permissao }
          : usuario
      )
    );
    setEditIndex(null);
  };

  const cancelarEdicao = () => {
    setEditIndex(null);
    setEditValues({ nome: '', permissao: 'Admin' });
  };

  const handleEditKeyDown = (event, index) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      salvarEdicao(index);
    }
    if (event.key === 'Escape') {
      event.preventDefault();
      cancelarEdicao();
    }
  };

  useEffect(() => {
    if (editIndex === null) {
      return undefined;
    }
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        cancelarEdicao();
      }
      if (event.key === 'Enter') {
        event.preventDefault();
        salvarEdicao(editIndex);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [editIndex, editValues]);

  return (
    <div className="usuarios-page">
      <div className="usuarios-shell">
        <header className="usuarios-header">
          <div className="usuarios-brand">
            <div className="usuarios-logo-badge">
              <img src={logo} alt="SensingFI" className="usuarios-logo" />
            </div>
            <div>
              <p className="usuarios-kicker">Painel de controle</p>
              <h1 className="usuarios-title">Usuários</h1>
              <p className="usuarios-subtitle">
                Gerencie acessos, permissões e níveis de segurança.
              </p>
            </div>
          </div>
          <div className="usuarios-header-actions">
            <Link className="usuarios-secondary-button" to="/home">
              Voltar para a página principal
            </Link>
            <button className="usuarios-primary-button" onClick={() => setMostrarModal(true)}>
              Criar usuário
            </button>
          </div>
        </header>
        <section className="usuarios-card">
          <div className="usuarios-table">
            <table className="tabela">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>E-mail</th>
                  <th>Permissão</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {usuarios.map((u, idx) => (
                  <tr key={idx} className={`usuarios-row usuarios-row-${u.permissao.toLowerCase()}`}>
                    <td>
                      {editIndex === idx ? (
                        <input
                          className="usuarios-edit-input"
                          name="nome"
                          type="text"
                          value={editValues.nome}
                          onChange={(event) =>
                            setEditValues((prev) => ({ ...prev, nome: event.target.value }))
                          }
                          onKeyDown={(event) => handleEditKeyDown(event, idx)}
                        />
                      ) : (
                        u.nome
                      )}
                    </td>
                    <td>{u.email}</td>
                    <td>
                      {editIndex === idx ? (
                        <select
                          className="usuarios-edit-select"
                          name="permissao"
                          value={editValues.permissao}
                          onChange={(event) =>
                            setEditValues((prev) => ({ ...prev, permissao: event.target.value }))
                          }
                          onKeyDown={(event) => handleEditKeyDown(event, idx)}
                        >
                          {permissoes.map((permissao) => (
                            <option key={permissao} value={permissao}>
                              {permissao}
                            </option>
                          ))}
                        </select>
                      ) : (
                        <span className={`badge badge-${u.permissao.toLowerCase()}`}>{u.permissao}</span>
                      )}
                    </td>
                    <td>
                      <div className="usuarios-actions">
                        {editIndex === idx ? (
                          <button
                            className="usuarios-save-button"
                            type="button"
                            onClick={() => salvarEdicao(idx)}
                          >
                            Salvar
                          </button>
                        ) : (
                          <button
                            className="icon-button"
                            aria-label="Editar usuário"
                            type="button"
                            onClick={() => iniciarEdicao(idx)}
                            disabled={usuarioAtual.permissao !== 'Admin'}
                            title="Editar usuário"
                          >
                            <FontAwesomeIcon icon={faPenToSquare} className="usuarios-icon" />
                          </button>
                        )}
                        <button
                          className="icon-button"
                          aria-label="Excluir usuário"
                          type="button"
                          title="Excluir usuário"
                          disabled={editIndex === idx}
                          onClick={() => {
                            const confirmado = window.confirm(
                              'Essa ação irá excluir o usuário. Você quer continuar?'
                            );
                            if (confirmado) {
                              setUsuarios((prev) => prev.filter((_, itemIndex) => itemIndex !== idx));
                            }
                          }}
                        >
                          <FontAwesomeIcon icon={faTrashCan} className="usuarios-icon" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
        {mostrarModal && (
          <div className="usuarios-modal-backdrop" role="dialog" aria-modal="true">
            <div className="usuarios-modal">
              <header className="usuarios-modal-header">
                <div>
                  <p className="usuarios-modal-kicker">Cadastro</p>
                  <h2 className="usuarios-modal-title">Novo usuário</h2>
                  <p className="usuarios-modal-helper">
                    Enviaremos um e-mail para este endereço para que o novo usuário crie a senha
                    e acesse a conta com as permissões definidas.
                  </p>
                </div>
              </header>
              <form className="usuarios-modal-form" onSubmit={handleSubmit}>
                <label className="usuarios-modal-field">
                  <span>Nome</span>
                  <input
                    name="nome"
                    type="text"
                    placeholder="Nome completo"
                    value={formValues.nome}
                    onChange={handleChange}
                    required
                  />
                </label>
                <label className="usuarios-modal-field">
                  <span>E-mail</span>
                  <input
                    name="email"
                    type="email"
                    placeholder="nome@exemplo.com"
                    value={formValues.email}
                    onChange={handleChange}
                    required
                  />
                </label>
                <label className="usuarios-modal-field">
                  <span>Permissão</span>
                  <select name="permissao" value={formValues.permissao} onChange={handleChange}>
                    {permissoes.map((permissao) => (
                      <option key={permissao} value={permissao}>
                        {permissao}
                      </option>
                    ))}
                  </select>
                </label>
                <div className="usuarios-modal-actions">
                  <button
                    type="button"
                    className="usuarios-secondary-button"
                    onClick={() => setMostrarModal(false)}
                  >
                    Cancelar
                  </button>
                  <button type="submit" className="usuarios-primary-button">
                    Salvar usuário
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Usuarios;