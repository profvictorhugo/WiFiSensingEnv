import "./Modelos.css";
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faPenToSquare,
  faTrashCan,
  faEye,
  faArrowLeft,
  faChartLine,
  faCircleInfo,
} from "@fortawesome/free-solid-svg-icons";
import logo from "../../assets/logo.svg";

const createSlug = (text = "") =>
  text
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");

const formatSlug = (slug = "") =>
  slug
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

const Modelos = () => {
  const { modeloId } = useParams();

  const [models, setModels] = useState([
    {
      name: "Modelo V3 - Treino Incremental",
      slug: "v3-treino-incremental",
      description:
        "Classificação de movimento baseado em sinais de Wi-Fi CSI com rede neural convolucional.",
      email: "ana.silva@sensingfi.com",
      version: "v3.2",
      status: "Ativo",
      accuracy: "94.8%",
    },
    {
      name: "Detecção de Presença Leve",
      slug: "deteccao-presenca-leve",
      description:
        "Modelo otimizado para inferência rápida em roteadores e dispositivos de borda.",
      email: "carlos.dev@sensingfi.com",
      version: "v1.0",
      status: "Ativo",
      accuracy: "91.2%",
    },
    {
      name: "Identificação de Gestos (Beta)",
      slug: "identificacao-gestos-beta",
      description:
        "Rede recorrente LSTM treinada com o dataset do laboratório 02 para gestos de mão.",
      email: "victor.hugo@sensingfi.com",
      version: "v0.8",
      status: "Treinando",
      accuracy: "88.5%",
    },
  ]);

  const [showModal, setShowModal] = useState(false);
  const [formValues, setFormValues] = useState({
    name: "",
    description: "",
    email: "",
    version: "v1.0",
    status: "Ativo",
    accuracy: "90.0%",
  });

  const [editIndex, setEditIndex] = useState(null);
  const [editValues, setEditValues] = useState({
    name: "",
    description: "",
    version: "v1.0",
    status: "Ativo",
    accuracy: "90.0%",
  });

  const statusOptions = ["Ativo", "Treinando", "Arquivado"];

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormValues((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const cleanName = formValues.name.trim();
    if (!cleanName) return;

    const baseSlug = createSlug(cleanName) || "modelo";
    let slug = baseSlug;
    let counter = 2;
    while (models.some((item) => item.slug === slug)) {
      slug = `${baseSlug}-${counter}`;
      counter += 1;
    }

    const newModel = {
      name: cleanName,
      slug,
      description: formValues.description.trim() || "Sem descrição.",
      email: formValues.email.trim() || "usuario@sensingfi.com",
      version: formValues.version.trim() || "v1.0",
      status: formValues.status,
      accuracy: formValues.accuracy.trim() || "85.0%",
    };

    setModels((prev) => [newModel, ...prev]);
    setFormValues({
      name: "",
      description: "",
      email: "",
      version: "v1.0",
      status: "Ativo",
      accuracy: "90.0%",
    });
    setShowModal(false);
  };

  const startEditing = (index) => {
    const model = models[index];
    setEditIndex(index);
    setEditValues({
      name: model.name,
      description: model.description,
      version: model.version,
      status: model.status,
      accuracy: model.accuracy,
    });
  };

  const saveEditing = (index) => {
    setModels((prev) =>
      prev.map((model, idx) =>
        idx === index
          ? {
              ...model,
              name: editValues.name,
              description: editValues.description,
              version: editValues.version,
              status: editValues.status,
              accuracy: editValues.accuracy,
            }
          : model,
      ),
    );
    setEditIndex(null);
  };

  const cancelEditing = () => {
    setEditIndex(null);
  };

  const handleEditKeyDown = (event, index) => {
    if (event.key === "Enter") {
      event.preventDefault();
      saveEditing(index);
    }
    if (event.key === "Escape") {
      event.preventDefault();
      cancelEditing();
    }
  };

  useEffect(() => {
    if (editIndex === null) return undefined;
    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        cancelEditing();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [editIndex]);

  if (modeloId) {
    const selectedModel = models.find((m) => m.slug === modeloId) || {
      name: formatSlug(modeloId),
      slug: modeloId,
      description: "Detalhes e histórico de execução desta versão de modelo.",
      email: "responsavel@sensingfi.com",
      version: "v1.0",
      status: "Ativo",
      accuracy: "90.0%",
    };

    return (
      <div className="models-page">
        <div className="models-shell">
          <header className="models-header">
            <div className="models-brand">
              <div className="models-logo-badge">
                <img src={logo} alt="SensingFI" className="models-logo" />
              </div>
              <div>
                <p className="models-kicker">Detalhes do Modelo</p>
                <h1 className="models-title">{selectedModel.name}</h1>
                <p className="models-subtitle">{selectedModel.description}</p>
              </div>
            </div>
            <div className="models-header-actions">
              <Link className="models-secondary-button" to="/modelos">
                Voltar para listagem
              </Link>
            </div>
          </header>

          <section className="models-detail-content">
            <div className="models-detail-grid">
              <div className="models-detail-card">
                <h3>
                  <FontAwesomeIcon
                    icon={faCircleInfo}
                    className="detail-icon"
                  />{" "}
                  Informações Principais
                </h3>
                <ul className="detail-list">
                  <li>
                    <strong>Responsável:</strong>{" "}
                    <span>{selectedModel.email}</span>
                  </li>
                  <li>
                    <strong>Versão:</strong>{" "}
                    <span>{selectedModel.version}</span>
                  </li>
                  <li>
                    <strong>Status Atual:</strong>{" "}
                    <span
                      className={`badge badge-${selectedModel.status.toLowerCase()}`}
                    >
                      {selectedModel.status}
                    </span>
                  </li>
                  <li>
                    <strong>Slug de Identificação:</strong>{" "}
                    <span>{selectedModel.slug}</span>
                  </li>
                </ul>
              </div>
              <div className="models-detail-card">
                <h3>
                  <FontAwesomeIcon icon={faChartLine} className="detail-icon" />{" "}
                  Desempenho e Métricas
                </h3>
                <div className="metric-box">
                  <span className="metric-label">Acurácia Validada</span>
                  <span className="metric-value">{selectedModel.accuracy}</span>
                </div>
                <p className="metric-helper">
                  Testado com o conjunto de validação de ambiente Wi-Fi Sensing.
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>
    );
  }

  return (
    <div className="models-page">
      <div className="models-shell">
        <header className="models-header">
          <div className="models-brand">
            <div className="models-logo-badge">
              <img src={logo} alt="SensingFI" className="models-logo" />
            </div>
            <div>
              <p className="models-kicker">Painel de controle</p>
              <h1 className="models-title">Modelos</h1>
              <p className="models-subtitle">
                Organize modelos de machine learning, acompanhe versões
                treinadas e métricas de avaliação.
              </p>
            </div>
          </div>
          <div className="models-header-actions">
            <Link className="models-secondary-button" to="/home">
              Voltar para a página principal
            </Link>
            <button
              className="models-primary-button"
              onClick={() => setShowModal(true)}
            >
              Novo modelo
            </button>
          </div>
        </header>

        <section className="models-card">
          <div className="models-card-header">
            <h2>Modelos Cadastrados</h2>
          </div>
          <div className="models-table">
            <table className="tabela">
              <thead>
                <tr>
                  <th>Nome e Descrição</th>
                  <th>Versão</th>
                  <th>Status</th>
                  <th>Acurácia</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {models.map((m, idx) => (
                  <tr
                    key={m.slug}
                    className={`models-row models-row-${m.status.toLowerCase()}`}
                  >
                    <td>
                      {editIndex === idx ? (
                        <div className="models-edit-fields">
                          <input
                            className="models-edit-input"
                            name="name"
                            type="text"
                            placeholder="Nome do modelo"
                            value={editValues.name}
                            onChange={(event) =>
                              setEditValues((prev) => ({
                                ...prev,
                                name: event.target.value,
                              }))
                            }
                            onKeyDown={(event) => handleEditKeyDown(event, idx)}
                          />
                          <input
                            className="models-edit-input"
                            name="description"
                            type="text"
                            placeholder="Descrição"
                            value={editValues.description}
                            onChange={(event) =>
                              setEditValues((prev) => ({
                                ...prev,
                                description: event.target.value,
                              }))
                            }
                            onKeyDown={(event) => handleEditKeyDown(event, idx)}
                          />
                        </div>
                      ) : (
                        <div className="models-name-desc">
                          <strong>{m.name}</strong>
                          <span className="models-desc">{m.description}</span>
                          <small className="models-author">
                            Resp: {m.email}
                          </small>
                        </div>
                      )}
                    </td>
                    <td>
                      {editIndex === idx ? (
                        <input
                          className="models-edit-input models-edit-short"
                          name="version"
                          type="text"
                          value={editValues.version}
                          onChange={(event) =>
                            setEditValues((prev) => ({
                              ...prev,
                              version: event.target.value,
                            }))
                          }
                          onKeyDown={(event) => handleEditKeyDown(event, idx)}
                        />
                      ) : (
                        <span className="models-version">{m.version}</span>
                      )}
                    </td>
                    <td>
                      {editIndex === idx ? (
                        <select
                          className="models-edit-select"
                          name="status"
                          value={editValues.status}
                          onChange={(event) =>
                            setEditValues((prev) => ({
                              ...prev,
                              status: event.target.value,
                            }))
                          }
                          onKeyDown={(event) => handleEditKeyDown(event, idx)}
                        >
                          {statusOptions.map((st) => (
                            <option key={st} value={st}>
                              {st}
                            </option>
                          ))}
                        </select>
                      ) : (
                        <span
                          className={`badge badge-${m.status.toLowerCase()}`}
                        >
                          {m.status}
                        </span>
                      )}
                    </td>
                    <td>
                      {editIndex === idx ? (
                        <input
                          className="models-edit-input models-edit-short"
                          name="accuracy"
                          type="text"
                          value={editValues.accuracy}
                          onChange={(event) =>
                            setEditValues((prev) => ({
                              ...prev,
                              accuracy: event.target.value,
                            }))
                          }
                          onKeyDown={(event) => handleEditKeyDown(event, idx)}
                        />
                      ) : (
                        <span className="models-accuracy">{m.accuracy}</span>
                      )}
                    </td>
                    <td>
                      <div className="models-actions">
                        {editIndex === idx ? (
                          <>
                            <button
                              className="models-save-button"
                              type="button"
                              onClick={() => saveEditing(idx)}
                            >
                              Salvar
                            </button>
                            <button
                              className="models-cancel-button"
                              type="button"
                              onClick={cancelEditing}
                            >
                              Cancelar
                            </button>
                          </>
                        ) : (
                          <>
                            <Link
                              className="icon-button view-button"
                              to={`/modelos/${m.slug}`}
                              title="Visualizar detalhes"
                              aria-label="Visualizar detalhes"
                            >
                              <FontAwesomeIcon
                                icon={faEye}
                                className="models-icon"
                              />
                            </Link>
                            <button
                              className="icon-button edit-button"
                              aria-label="Editar modelo"
                              type="button"
                              onClick={() => startEditing(idx)}
                              title="Editar modelo"
                            >
                              <FontAwesomeIcon
                                icon={faPenToSquare}
                                className="models-icon"
                              />
                            </button>
                            <button
                              className="icon-button delete-button"
                              aria-label="Excluir modelo"
                              type="button"
                              title="Excluir modelo"
                              onClick={() => {
                                const confirmed = window.confirm(
                                  `Você tem certeza que deseja excluir o modelo "${m.name}"?`,
                                );
                                if (confirmed) {
                                  setModels((prev) =>
                                    prev.filter(
                                      (_, itemIndex) => itemIndex !== idx,
                                    ),
                                  );
                                }
                              }}
                            >
                              <FontAwesomeIcon
                                icon={faTrashCan}
                                className="models-icon"
                              />
                            </button>
                          </>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {showModal && (
          <div
            className="models-modal-backdrop"
            role="dialog"
            aria-modal="true"
          >
            <div className="models-modal">
              <header className="models-modal-header">
                <div>
                  <p className="models-modal-kicker">Cadastro</p>
                  <h2 className="models-modal-title">Enviar novo modelo</h2>
                  <p className="models-modal-helper">
                    Cadastre um novo modelo de machine learning para avaliação
                    de sinais de Wi-Fi Sensing.
                  </p>
                </div>
              </header>
              <form className="models-modal-form" onSubmit={handleSubmit}>
                <label className="models-modal-field">
                  <span>Nome do modelo</span>
                  <input
                    name="name"
                    type="text"
                    placeholder="Ex: Modelo V4 - Rede Siamesa"
                    value={formValues.name}
                    onChange={handleChange}
                    required
                  />
                </label>
                <label className="models-modal-field">
                  <span>Descrição</span>
                  <input
                    name="description"
                    type="text"
                    placeholder="Resumo do objetivo e arquitetura"
                    value={formValues.description}
                    onChange={handleChange}
                    required
                  />
                </label>
                <label className="models-modal-field">
                  <span>E-mail do responsável</span>
                  <input
                    name="email"
                    type="email"
                    placeholder="responsavel@sensingfi.com"
                    value={formValues.email}
                    onChange={handleChange}
                    required
                  />
                </label>
                <div className="models-modal-row">
                  <label className="models-modal-field">
                    <span>Versão</span>
                    <input
                      name="version"
                      type="text"
                      placeholder="Ex: v1.0"
                      value={formValues.version}
                      onChange={handleChange}
                      required
                    />
                  </label>
                  <label className="models-modal-field">
                    <span>Acurácia Estimada</span>
                    <input
                      name="accuracy"
                      type="text"
                      placeholder="Ex: 92.5%"
                      value={formValues.accuracy}
                      onChange={handleChange}
                      required
                    />
                  </label>
                </div>
                <label className="models-modal-field">
                  <span>Status de Treinamento</span>
                  <select
                    name="status"
                    value={formValues.status}
                    onChange={handleChange}
                  >
                    {statusOptions.map((st) => (
                      <option key={st} value={st}>
                        {st}
                      </option>
                    ))}
                  </select>
                </label>
                <div className="models-modal-actions">
                  <button
                    type="button"
                    className="models-secondary-button"
                    onClick={() => setShowModal(false)}
                  >
                    Cancelar
                  </button>
                  <button type="submit" className="models-primary-button">
                    Salvar modelo
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

export default Modelos;
