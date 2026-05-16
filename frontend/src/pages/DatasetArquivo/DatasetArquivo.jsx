import "./DatasetArquivo.css";
import { Link, useParams } from "react-router-dom";
import { useEffect, useMemo, useState } from "react";
import logo from "../../assets/logo.svg";

const formatSlug = (slug = "") =>
  slug
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");

const csvSamples = {
  "captura-2024-04-18.csv": "tempo,ssid,forca\n14:22,wifi-lab-01,-41\n14:23,wifi-lab-01,-42\n14:24,wifi-lab-01,-40\n14:25,wifi-lab-01,-44",
  "captura-2024-04-17.csv": "tempo,ssid,forca\n09:40,wifi-lab-01,-43\n09:41,wifi-lab-01,-45\n09:42,wifi-lab-01,-44",
  "mov-2024-04-15.csv": "tempo,area,evento\n16:05,corredor,passagem\n16:06,corredor,passagem\n16:08,corredor,parada",
  "presenca-2024-04-10.csv": "tempo,sala,presenca\n11:18,reuniao,1\n11:20,reuniao,1\n11:24,reuniao,0"
};

const parseCsv = (texto = "") => {
  const linhas = texto
    .split(/\r\n|\r|\n/)
    .map((linha) => linha.trim())
    .filter(Boolean);

  if (linhas.length === 0) {
    return { headers: [], rows: [] };
  }

  const headers = linhas[0].split(",");
  const rows = linhas.slice(1).map((linha) => linha.split(","));
  return { headers, rows };
};

const DatasetArquivo = () => {
  const { datasetId, arquivoId } = useParams();
  const datasetName = datasetId ? formatSlug(datasetId) : "Dataset";
  const arquivoNome = arquivoId ? decodeURIComponent(arquivoId) : "arquivo.csv";
  const [csvText, setCsvText] = useState("");

  useEffect(() => {
    const storageKey = datasetId
      ? `dataset:${datasetId}:file:${arquivoNome}`
      : null;
    if (storageKey) {
      const armazenado = sessionStorage.getItem(storageKey);
      if (armazenado) {
        setCsvText(armazenado);
        return;
      }
    }
    setCsvText(csvSamples[arquivoNome] || "");
  }, [arquivoNome, datasetId]);

  const { headers, rows } = useMemo(() => parseCsv(csvText), [csvText]);
  const rowsVisible = rows.slice(0, 100);
  const restante = rows.length - rowsVisible.length;

  return (
    <div className="dataset-file-page">
      <div className="dataset-file-shell">
        <header className="dataset-file-header">
          <div className="dataset-file-brand">
            <div className="dataset-file-badge">
              <img src={logo} alt="SensingFI" />
            </div>
            <div className="dataset-file-text">
              <span className="dataset-file-eyebrow">Visualizacao do CSV</span>
              <h1 className="dataset-file-title">{datasetName}</h1>
              <p className="dataset-file-subtitle">{arquivoNome}</p>
            </div>
          </div>
          <div className="dataset-file-actions">
            <Link className="dataset-file-secondary" to={`/datasets/${datasetId}`}>
              Voltar para o dataset
            </Link>
          </div>
        </header>

        <section className="dataset-file-card">
          <div className="dataset-file-card-header">
            <div>
              <h2>Conteudo do arquivo</h2>
              <p className="dataset-file-helper">
                Visualize os registros em formato tabular.
              </p>
            </div>
            <div className="dataset-file-meta">
              <span className="dataset-file-chip">{rows.length} linhas</span>
              <span className="dataset-file-chip">{headers.length} colunas</span>
            </div>
          </div>

          {headers.length === 0 ? (
            <div className="dataset-file-empty">
              Nenhum conteudo CSV disponivel para este arquivo.
            </div>
          ) : (
            <div className="dataset-file-table">
              <table className="dataset-file-table-grid">
                <thead>
                  <tr>
                    {headers.map((header) => (
                      <th key={header}>{header}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {rowsVisible.map((row, index) => (
                    <tr key={index}>
                      {headers.map((header, cellIndex) => (
                        <td key={header}>{row[cellIndex] || "-"}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {restante > 0 && (
            <p className="dataset-file-footnote">
              Mostrando as primeiras {rowsVisible.length} linhas. Existem mais {restante}
              registros.
            </p>
          )}
        </section>
      </div>
    </div>
  );
};

export default DatasetArquivo;
