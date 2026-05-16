import "./DatasetDetalhe.css";
import { Link, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faEye, faTrashCan } from "@fortawesome/free-solid-svg-icons";
import logo from "../../assets/logo.svg";

const formatSlug = (slug = "") =>
  slug
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

const datasetCatalogo = {
  "sinal-ambiente-abril": {
    status: "Ativo",
    atualizado: "Há 2 dias",
    arquivos: 2,
    origem: "wifi-lab-01",
    descricao: "Capturas ambientais do laboratório principal."
  },
  "movimentos-corredor": {
    status: "Inativo",
    atualizado: "Há 4 dias",
    arquivos: 1,
    origem: "wifi-lab-02",
    descricao: "Sequências de movimento captadas no corredor central."
  },
  "presenca-sala-reuniao": {
    status: "Ativo",
    atualizado: "Há 8 dias",
    arquivos: 1,
    origem: "wifi-lab-01",
    descricao: "Dataset de presença para sala de reuniões."
  }
};

const datasetArquivos = {
  "sinal-ambiente-abril": [
    {
      nome: "captura-2024-04-18.csv",
      registros: 1200,
      origem: "wifi-lab-01",
      horario: "18/04/2024 14:22"
    },
    {
      nome: "captura-2024-04-17.csv",
      registros: 980,
      origem: "wifi-lab-01",
      horario: "17/04/2024 09:40"
    }
  ],
  "movimentos-corredor": [
    {
      nome: "mov-2024-04-15.csv",
      registros: 640,
      origem: "wifi-lab-02",
      horario: "15/04/2024 16:05"
    }
  ],
  "presenca-sala-reuniao": [
    {
      nome: "presenca-2024-04-10.csv",
      registros: 520,
      origem: "wifi-lab-01",
      horario: "10/04/2024 11:18"
    }
  ]
};

const contarLinhas = (texto = "") => {
  const linhas = texto.split(/\r\n|\r|\n/);
  if (linhas.length > 0 && linhas[linhas.length - 1] === "") {
    linhas.pop();
  }
  return linhas.length;
};

const DatasetDetalhe = () => {
  const { datasetId } = useParams();
  const datasetName = datasetId ? formatSlug(datasetId) : "Dataset";
  const datasetInfoBase = datasetCatalogo[datasetId] || {
    status: "Ativo",
    atualizado: "Hoje",
    arquivos: 0,
    origem: "Não informado",
    descricao: "Detalhes ainda não disponíveis para este dataset."
  };
  const [modoEdicao, setModoEdicao] = useState(false);
  const [detalhes, setDetalhes] = useState(datasetInfoBase);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [arquivoSelecionado, setArquivoSelecionado] = useState(null);
  const [arquivos, setArquivos] = useState(datasetArquivos[datasetId] || []);
  const statusKey = detalhes.status.toLowerCase();

  useEffect(() => {
    setDetalhes(datasetInfoBase);
    setModoEdicao(false);
    setArquivos(datasetArquivos[datasetId] || []);
  }, [datasetId, datasetInfoBase]);

  useEffect(() => {
    if (!modoEdicao) {
      return undefined;
    }

    const handleKeyDown = (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        setModoEdicao(false);
        return;
      }

      if (event.key === "Enter") {
        const isTextarea = event.target?.tagName === "TEXTAREA";
        if (isTextarea && !event.ctrlKey && !event.metaKey) {
          return;
        }
        event.preventDefault();
        setModoEdicao(false);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [modoEdicao]);

  const handleAbrirUpload = () => {
    setIsUploadOpen(true);
  };

  const handleFecharUpload = () => {
    setIsUploadOpen(false);
    setArquivoSelecionado(null);
  };

  const handleSubmitUpload = async (event) => {
    event.preventDefault();
    if (!arquivoSelecionado) {
      return;
    }
    let registros = 0;
    let conteudo = "";
    try {
      conteudo = await arquivoSelecionado.text();
      registros = contarLinhas(conteudo);
    } catch (error) {
      registros = 0;
    }
    const agora = new Date();
    const novoArquivo = {
      nome: arquivoSelecionado.name,
      registros,
      origem: detalhes.origem,
      horario: agora.toLocaleString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      })
    };

    if (datasetId && conteudo) {
      const storageKey = `dataset:${datasetId}:file:${arquivoSelecionado.name}`;
      sessionStorage.setItem(storageKey, conteudo);
    }
    setArquivos((prev) => [novoArquivo, ...prev]);
    setDetalhes((prev) => ({ ...prev, arquivos: prev.arquivos + 1 }));
    setIsUploadOpen(false);
    setArquivoSelecionado(null);
  };

  const handleRemoverArquivo = (nomeArquivo) => {
    const confirmado = window.confirm(`Deseja realmente excluir o arquivo "${nomeArquivo}"?`);
    if (confirmado) {
      setArquivos((prev) => prev.filter((item) => item.nome !== nomeArquivo));
      setDetalhes((prev) => ({ ...prev, arquivos: Math.max(0, prev.arquivos - 1) }));
      if (datasetId) {
        sessionStorage.removeItem(`dataset:${datasetId}:file:${nomeArquivo}`);
      }
    }
  };

  return (
    <div className="dataset-detail-page">
      <div className="dataset-detail-shell">
        <header className="dataset-detail-header">
          <div className="dataset-detail-brand">
            <div className="dataset-detail-badge">
              <img src={logo} alt="SensingFI" />
            </div>
            <div className="dataset-detail-text">
              <span className="dataset-detail-eyebrow">Detalhes do dataset</span>
              <h1 className="dataset-detail-title">{datasetName}</h1>
              <p className="dataset-detail-subtitle">
                Acompanhe status, arquivos e origem do dataset selecionado.
              </p>
            </div>
          </div>
          <div className="dataset-detail-actions">
            <Link className="dataset-detail-secondary" to="/datasets">
              Voltar para datasets
            </Link>
            <button
              type="button"
              className="dataset-detail-secondary dataset-detail-secondary--accent"
              onClick={handleAbrirUpload}
            >
              Enviar arquivo
            </button>
          </div>
        </header>

        <section className="dataset-detail-grid">
          <div className="dataset-detail-card">
            <div className="dataset-detail-card-header">
              <h2>Resumo</h2>
              <div className="dataset-detail-card-actions">
                {modoEdicao ? (
                  <select
                    className="dataset-detail-select"
                    value={detalhes.status}
                    onChange={(event) =>
                      setDetalhes((prev) => ({ ...prev, status: event.target.value }))
                    }
                  >
                    <option value="Ativo">Ativo</option>
                    <option value="Inativo">Inativo</option>
                  </select>
                ) : (
                  <span
                    className={`dataset-detail-status dataset-detail-status-${statusKey}`}
                  >
                    {detalhes.status}
                  </span>
                )}
                {modoEdicao ? (
                  <>
                    <button
                      type="button"
                      className="dataset-detail-primary dataset-detail-primary--save"
                      onClick={() => setModoEdicao(false)}
                    >
                      Salvar
                    </button>
                    <button
                      type="button"
                      className="dataset-detail-cancel"
                      onClick={() => {
                        setDetalhes(datasetInfoBase);
                        setModoEdicao(false);
                      }}
                    >
                      Cancelar
                    </button>
                  </>
                ) : (
                  <button
                    type="button"
                    className="dataset-detail-primary"
                    onClick={() => setModoEdicao(true)}
                  >
                    Editar
                  </button>
                )}
              </div>
            </div>
            {modoEdicao ? (
              <textarea
                className="dataset-detail-textarea"
                rows={3}
                value={detalhes.descricao}
                onChange={(event) =>
                  setDetalhes((prev) => ({ ...prev, descricao: event.target.value }))
                }
              />
            ) : (
              <p className="dataset-detail-description">{detalhes.descricao}</p>
            )}
            <div className="dataset-detail-stats">
              <div>
                <span>Origem</span>
                {modoEdicao ? (
                  <input
                    className="dataset-detail-input"
                    type="text"
                    value={detalhes.origem}
                    onChange={(event) =>
                      setDetalhes((prev) => ({ ...prev, origem: event.target.value }))
                    }
                  />
                ) : (
                  <strong>{detalhes.origem}</strong>
                )}
              </div>
              <div>
                <span>Arquivos</span>
                <strong>{detalhes.arquivos}</strong>
              </div>
              <div>
                <span>Atualizado</span>
                <strong>{detalhes.atualizado}</strong>
              </div>
            </div>
          </div>

          <div className="dataset-detail-card">
            <div className="dataset-detail-card-header">
              <h2>Arquivos recentes</h2>
            </div>
            <div className="dataset-detail-table">
              <table className="dataset-detail-table-grid">
                <thead>
                  <tr>
                    <th>Arquivo</th>
                    <th>Registros</th>
                    <th>Origem</th>
                    <th>Horário</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {arquivos.length === 0 ? (
                    <tr>
                      <td className="dataset-detail-empty" colSpan={5}>
                        Nenhuma captura registrada até o momento.
                      </td>
                    </tr>
                  ) : (
                    arquivos.map((item) => (
                      <tr key={item.nome}>
                        <td>
                          <Link
                            className="dataset-detail-file-link"
                            to={`/datasets/${datasetId}/arquivo/${encodeURIComponent(item.nome)}`}
                          >
                            {item.nome}
                          </Link>
                        </td>
                        <td>{item.registros}</td>
                        <td>{item.origem}</td>
                        <td>{item.horario}</td>
                        <td>
                          <div className="dataset-detail-actions-cell">
                            <Link
                              className="icon-button view-button"
                              to={`/datasets/${datasetId}/arquivo/${encodeURIComponent(item.nome)}`}
                              aria-label="Visualizar arquivo"
                              title="Visualizar arquivo"
                            >
                              <FontAwesomeIcon icon={faEye} className="dataset-detail-icon" />
                            </Link>
                            <button
                              type="button"
                              className="icon-button delete-button"
                              aria-label="Excluir arquivo"
                              title="Excluir arquivo"
                              onClick={() => handleRemoverArquivo(item.nome)}
                            >
                              <FontAwesomeIcon icon={faTrashCan} className="dataset-detail-icon" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>

      {isUploadOpen && (
        <div
          className="dataset-detail-modal-overlay"
          role="dialog"
          aria-modal="true"
          aria-labelledby="dataset-upload-title"
          onClick={handleFecharUpload}
        >
          <div
            className="dataset-detail-modal"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="dataset-detail-modal-header">
              <h2 id="dataset-upload-title">Enviar arquivo</h2>
              <button
                type="button"
                className="dataset-detail-modal-close"
                onClick={handleFecharUpload}
                aria-label="Fechar"
              >
                x
              </button>
            </div>
            <p className="dataset-detail-modal-subtitle">
              Selecione um arquivo para vincular ao dataset {datasetName}.
            </p>
            <form
              className="dataset-detail-modal-form"
              onSubmit={handleSubmitUpload}
            >
              <label className="dataset-detail-file">
                <input
                  type="file"
                  accept=".csv,text/csv"
                  onChange={(event) =>
                    setArquivoSelecionado(event.target.files?.[0] || null)
                  }
                />
                <span>Escolher arquivo .csv</span>
                <strong>
                  {arquivoSelecionado
                    ? arquivoSelecionado.name
                    : "Nenhum arquivo selecionado"}
                </strong>
              </label>
              <div className="dataset-detail-modal-actions">
                <button
                  type="button"
                  className="dataset-detail-secondary"
                  onClick={handleFecharUpload}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  className="dataset-detail-primary dataset-detail-primary--save"
                  disabled={!arquivoSelecionado}
                >
                  Enviar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default DatasetDetalhe;
