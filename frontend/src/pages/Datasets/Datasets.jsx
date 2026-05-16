import "./Datasets.css";
import { Link } from "react-router-dom";
import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faTrashCan } from "@fortawesome/free-solid-svg-icons";
import logo from "../../assets/logo.svg";

const criarSlug = (texto = "") =>
  texto
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");

const Datasets = () => {
  const [mostrarModal, setMostrarModal] = useState(false);
  const [nomeDataset, setNomeDataset] = useState("");
  const [datasets, setDatasets] = useState([
    {
      nome: "Sinal ambiente abril",
      slug: "sinal-ambiente-abril",
      atualizado: "Há 2 dias",
      arquivos: 6
    },
    {
      nome: "Movimentos corredor",
      slug: "movimentos-corredor",
      atualizado: "Há 4 dias",
      arquivos: 4
    },
    {
      nome: "Presença sala reunião",
      slug: "presenca-sala-reuniao",
      atualizado: "Há 8 dias",
      arquivos: 3
    }
  ]);

  const handleExcluirDataset = (slug) => {
    const dataset = datasets.find((item) => item.slug === slug);
    if (!dataset) return;
    const confirmado = window.confirm(`Deseja realmente excluir o dataset "${dataset.nome}"?`);
    if (confirmado) {
      setDatasets((prev) => prev.filter((item) => item.slug !== slug));
    }
  };

  return (
    <div className="dataset-page">
      <div className="dataset-shell">
        <header className="dataset-header">
          <div className="dataset-brand">
            <div className="dataset-badge">
              <img src={logo} alt="SensingFI" />
            </div>
            <div className="dataset-brand-text">
              <span className="dataset-eyebrow">Datasets cadastrados</span>
              <h1 className="dataset-title">Datasets</h1>
              <p className="dataset-subtitle">
                Acompanhe coleções de dados enviados.
              </p>
            </div>
          </div>
          <div className="dataset-header-actions">
            <Link to="/home" className="dataset-secondary-button">
              Voltar para a página principal
            </Link>
            <button
              type="button"
              className="dataset-primary-button"
              onClick={() => setMostrarModal(true)}
            >
              Adicionar dataset
            </button>
          </div>
        </header>
        <section className="dataset-card">
          <div className="dataset-card-header">
            <h2>Lista de datasets</h2>
          </div>
          <div className="dataset-table">
            <table className="dataset-table-grid">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Arquivos</th>
                  <th>Atualizado</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {datasets.map((dataset) => (
                  <tr key={dataset.slug}>
                    <td>
                      <div className="dataset-name">
                        <strong>{dataset.nome}</strong>
                        <small>Slug: {dataset.slug}</small>
                      </div>
                    </td>
                    <td>{dataset.arquivos}</td>
                    <td>{dataset.atualizado}</td>
                    <td>
                      <div className="dataset-actions-cell">
                        <Link
                          className="icon-button view-button"
                          to={`/datasets/${dataset.slug}`}
                          aria-label="Visualizar dataset"
                          title="Visualizar"
                        >
                          <FontAwesomeIcon icon={faEye} className="dataset-icon" />
                        </Link>
                        <button
                          type="button"
                          className="icon-button delete-button"
                          aria-label="Excluir dataset"
                          title="Excluir dataset"
                          onClick={() => handleExcluirDataset(dataset.slug)}
                        >
                          <FontAwesomeIcon icon={faTrashCan} className="dataset-icon" />
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
          <div className="dataset-modal-backdrop" role="dialog" aria-modal="true">
            <div className="dataset-modal">
              <header className="dataset-modal-header">
                <div>
                  <p className="dataset-modal-kicker">Cadastro</p>
                  <h2 className="dataset-modal-title">Adicionar dataset</h2>
                  <p className="dataset-modal-helper">
                    Informe o nome do dataset para criar a base de dados.
                  </p>
                </div>
              </header>
              <form
                className="dataset-modal-form"
                onSubmit={(event) => {
                  event.preventDefault();
                  const nomeLimpo = nomeDataset.trim();
                  if (!nomeLimpo) {
                    return;
                  }
                  const slugBase = criarSlug(nomeLimpo) || "dataset";
                  let slug = slugBase;
                  let contador = 2;
                  while (datasets.some((item) => item.slug === slug)) {
                    slug = `${slugBase}-${contador}`;
                    contador += 1;
                  }
                  const novoDataset = {
                    nome: nomeLimpo,
                    slug,
                    atualizado: "Agora",
                    arquivos: 0
                  };
                  setDatasets((prev) => [novoDataset, ...prev]);
                  setNomeDataset("");
                  setMostrarModal(false);
                }}
              >
                <label className="dataset-modal-field">
                  <span>Nome do dataset</span>
                  <input
                    type="text"
                    placeholder="Ex: Sinal ambiente abril"
                    value={nomeDataset}
                    onChange={(event) => setNomeDataset(event.target.value)}
                    required
                  />
                </label>
                <div className="dataset-modal-actions">
                  <button
                    type="button"
                    className="dataset-secondary-button"
                    onClick={() => setMostrarModal(false)}
                  >
                    Cancelar
                  </button>
                  <button type="submit" className="dataset-primary-button">
                    Criar dataset
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

export default Datasets;
