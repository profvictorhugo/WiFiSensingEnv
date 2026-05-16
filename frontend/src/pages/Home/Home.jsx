import "./Home.css";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faRightFromBracket } from "@fortawesome/free-solid-svg-icons";
import logo from "../../assets/logo.svg";

const modules = [
  {
    title: "Usuários",
    description: "Gerencie perfis, permissões e acessos.",
    tone: "tone-users",
    path: "/usuarios",
  },
  {
    title: "Modelos",
    description: "Organize modelos de ML e versões treinadas.",
    tone: "tone-models",
    path: "/modelos",
  },
  {
    title: "Datasets",
    description: "Acompanhe coleções de dados e status de captura.",
    tone: "tone-datasets",
    path: "/datasets",
  },
  {
    title: "Configurações",
    description: "Ajustes da conta, segurança e preferências gerais.",
    tone: "tone-account",
    path: "/configuracoes",
  },
];

const recentHistory = [
  {
    title: "Dataset: Sinal-ambiente-abril",
    meta: "Enviado há 2 dias · 48 arquivos",
    detail: "Origem: wifi-lab-01",
    type: "dataset",
    slug: "sinal-ambiente-abril",
  },
  {
    title: "Dataset: movimentos-corredor",
    meta: "Enviado há 4 dias · 32 arquivos",
    detail: "Origem: wifi-lab-02",
    type: "dataset",
    slug: "movimentos-corredor",
  },
  {
    title: "Modelo V3 - treino incremental",
    meta: "Atualizado ha 6 dias",
    detail: "Baseado em 3 datasets",
    type: "modelo",
    slug: "v3-treino-incremental",
  },
  {
    title: "Dataset: presenca-sala-reuniao",
    meta: "Enviado há 8 dias · 20 arquivos",
    detail: "Origem: wifi-lab-01",
    type: "dataset",
    slug: "presenca-sala-reuniao",
  },
];

const getHistoryPath = (item) => {
  if (item.type === "dataset") {
    return `/datasets/${item.slug}`;
  }
  return `/modelos/${item.slug}`;
};

const Home = () => {
  return (
    <div className="home-page">
      <div className="home-shell">
        <header className="home-header">
          <div className="home-brand">
            <div className="home-badge">
              <img src={logo} alt="SensingFI" />
            </div>
            <div className="home-brand-text">
              <span className="home-eyebrow">Resumo geral</span>
              <h1 className="home-title">Página Inicial</h1>
              <p className="home-subtitle">
                Selecione um modulo para visualizar dados, configurar modelos e gerenciar acessos.
              </p>
            </div>
          </div>
          <div className="home-accent" aria-hidden="true" />
        </header>

        <section className="home-body">
          <div className="home-left-column">
            <div className="home-modules">
              <ul className="home-modules-list">
                {modules.map((module) => (
                  <li key={module.title} className="home-module-item">
                    <span className={`home-module-dot ${module.tone}`} aria-hidden="true" />
                    <div className="home-module-text">
                      <strong>{module.title}</strong>
                      <span>{module.description}</span>
                    </div>
                    <Link className="home-module-button" to={module.path}>
                      Abrir
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <div className="home-logout-container">
              <Link to="/" className="home-logout-button" title="Sair da conta">
                <FontAwesomeIcon icon={faRightFromBracket} className="home-logout-icon" />
                <span>Sair da conta</span>
              </Link>
            </div>
          </div>
          <aside className="home-summary">
            <h3 className="home-summary-title">Resumo rápido</h3>
            <p className="home-summary-text">
              Histórico de atividades recentes.
            </p>
            <ul className="home-summary-history">
              {recentHistory.map((item) => (
                <li key={item.title} className="home-summary-history-item">
                  <Link
                    className="home-summary-history-link"
                    to={getHistoryPath(item)}
                    aria-label={`Abrir ${item.title}`}
                  >
                    <div className="home-summary-history-content">
                      <strong>{item.title}</strong>
                      <span>{item.meta}</span>
                      <small>{item.detail}</small>
                    </div>
                  </Link>
                </li>
              ))}
            </ul>
          </aside>
        </section>
      </div>
    </div>
  );
};

export default Home;
