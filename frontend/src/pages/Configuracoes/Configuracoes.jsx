import "./Configuracoes.css";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPenToSquare, faPowerOff } from "@fortawesome/free-solid-svg-icons";
import logo from "../../assets/logo.svg";

const Configuracoes = () => {
  const [formData, setFormData] = useState({
    twoFactor: true,
    emailNotifications: true,
    criticalAlerts: true,
    locale: "pt-BR",
    timezone: "America/Sao_Paulo",
    backupSchedule: "daily",
    maintenanceWindow: "02:00",
  });
  const [saveMessage, setSaveMessage] = useState("");
  const [showDevicesModal, setShowDevicesModal] = useState(false);
  const [devices, setDevices] = useState([
    {
      id: "device-1",
      name: "Notebook - Laboratorio",
      location: "Sao Paulo, BR",
      lastSeen: "Ativo agora",
    },
    {
      id: "device-2",
      name: "Desktop - Centro de dados",
      location: "Campinas, BR",
      lastSeen: "Ha 2 horas",
    },
    {
      id: "device-3",
      name: "Tablet - Monitoramento",
      location: "Rio de Janeiro, BR",
      lastSeen: "Ha 1 dia",
    },
    {
      id: "device-4",
      name: "Smartphone - Administrador",
      location: "Remoto",
      lastSeen: "Ha 3 dias",
    },
  ]);
  const [editingDeviceId, setEditingDeviceId] = useState(null);
  const [editingName, setEditingName] = useState("");

  const handleChange = (event) => {
    const { name, type, value, checked } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
    setSaveMessage("");
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setSaveMessage("Alterações salvas localmente.");
  };

  const handleStartEditDevice = (deviceId) => {
    const device = devices.find((item) => item.id === deviceId);
    if (!device) {
      return;
    }
    setEditingDeviceId(deviceId);
    setEditingName(device.name);
  };

  const handleSaveDeviceName = (deviceId) => {
    const nextName = editingName.trim();
    if (!nextName) {
      return;
    }
    setDevices((prev) =>
      prev.map((item) => (item.id === deviceId ? { ...item, name: nextName } : item))
    );
    setEditingDeviceId(null);
    setEditingName("");
  };

  const handleCancelEditDevice = () => {
    setEditingDeviceId(null);
    setEditingName("");
  };

  const handleDeviceInputKeyDown = (event, deviceId) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSaveDeviceName(deviceId);
    }
    if (event.key === "Escape") {
      event.preventDefault();
      handleCancelEditDevice();
    }
  };

  useEffect(() => {
    if (!showDevicesModal) {
      return undefined;
    }
    const handleKeyDown = (event) => {
      if (event.key !== "Escape") {
        return;
      }
      event.preventDefault();
      if (editingDeviceId) {
        handleCancelEditDevice();
        return;
      }
      setShowDevicesModal(false);
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [showDevicesModal, editingDeviceId]);

  const handleDisconnectDevice = (deviceId) => {
    const device = devices.find((item) => item.id === deviceId);
    if (!device) {
      return;
    }
    const confirmClose = window.confirm(
      `Encerrar acesso de "${device.name}" agora?`
    );
    if (!confirmClose) {
      return;
    }
    setDevices((prev) => prev.filter((item) => item.id !== deviceId));
  };

  return (
    <div className="config-page">
      <form className="config-shell" onSubmit={handleSubmit}>
        <header className="config-header">
          <div className="config-brand">
            <div className="config-badge">
              <img src={logo} alt="SensingFI" />
            </div>
            <div className="config-brand-text">
              <span className="config-eyebrow">Configurações</span>
              <h1 className="config-title">Preferências do sistema</h1>
              <p className="config-subtitle">
                Ajuste a conta, segurança e preferências gerais do ambiente.
              </p>
            </div>
          </div>
          <div className="config-actions">
            <Link to="/home" className="config-secondary-button">
              Voltar para a página principal
            </Link>
            <button type="submit" className="config-primary-button">
              Salvar alterações
            </button>
            {saveMessage && <span className="config-save-status">{saveMessage}</span>}
          </div>
        </header>

        <section className="config-grid">
          <article className="config-panel">
            <div className="config-panel-header">
              <div>
                <p className="config-panel-kicker">Segurança</p>
                <h3 className="config-panel-title">Controle de acessos</h3>
              </div>
            </div>
            <div className="config-panel-form">
              <label className="config-field config-toggle">
                <div className="config-field-main">
                  <span>Autenticação em duas etapas</span>
                  <small>Reforce o acesso com verificação adicional.</small>
                </div>
                <div className="config-toggle-control">
                  <input
                    type="checkbox"
                    name="twoFactor"
                    checked={formData.twoFactor}
                    onChange={handleChange}
                  />
                  <span className="config-toggle-slider" aria-hidden="true" />
                </div>
              </label>
              <div className="config-item">
                <div className="config-item-text">
                  <strong>Dispositivos conectados</strong>
                  <span>4 dispositivos ativos no momento.</span>
                </div>
                <div className="config-item-actions">
                  <button
                    type="button"
                    className="config-item-button"
                    onClick={() => setShowDevicesModal(true)}
                  >
                    Revisar
                  </button>
                </div>
              </div>
            </div>
          </article>

          <article className="config-panel">
            <div className="config-panel-header">
              <div>
                <p className="config-panel-kicker">Preferências gerais</p>
                <h3 className="config-panel-title">Rotinas e alertas</h3>
              </div>
            </div>
            <div className="config-panel-form">
              <label className="config-field config-toggle">
                <div className="config-field-main">
                  <span>Notificações por email</span>
                  <small>Avisos sobre treinos, dados e alertas operacionais.</small>
                </div>
                <div className="config-toggle-control">
                  <input
                    type="checkbox"
                    name="emailNotifications"
                    checked={formData.emailNotifications}
                    onChange={handleChange}
                  />
                  <span className="config-toggle-slider" aria-hidden="true" />
                </div>
              </label>

              <label className="config-field config-toggle">
                <div className="config-field-main">
                  <span>Alertas críticos</span>
                  <small>Incidentes de segurança e falhas de processamento.</small>
                </div>
                <div className="config-toggle-control">
                  <input
                    type="checkbox"
                    name="criticalAlerts"
                    checked={formData.criticalAlerts}
                    onChange={handleChange}
                  />
                  <span className="config-toggle-slider" aria-hidden="true" />
                </div>
              </label>

              <label className="config-field">
                <span>Idioma</span>
                <select name="locale" value={formData.locale} onChange={handleChange}>
                  <option value="pt-BR">Português (Brasil)</option>
                  <option value="en-US">English (US)</option>
                  <option value="es-ES">Español</option>
                </select>
                <small>Define o idioma principal do painel.</small>
              </label>

              <label className="config-field">
                <span>Fuso horário</span>
                <select name="timezone" value={formData.timezone} onChange={handleChange}>
                  <option value="America/Sao_Paulo">America/Sao_Paulo</option>
                  <option value="America/Fortaleza">America/Fortaleza</option>
                  <option value="America/Manaus">America/Manaus</option>
                </select>
                <small>Usado para relatórios e agendamentos.</small>
              </label>

              <label className="config-field">
                <span>Backups automáticos</span>
                <select
                  name="backupSchedule"
                  value={formData.backupSchedule}
                  onChange={handleChange}
                >
                  <option value="daily">Diário</option>
                  <option value="weekly">Semanal</option>
                  <option value="manual">Manual</option>
                </select>
                <small>Cópia do banco de dados e modelos.</small>
              </label>

              <label className="config-field">
                <span>Janela de manutenção</span>
                <select
                  name="maintenanceWindow"
                  value={formData.maintenanceWindow}
                  onChange={handleChange}
                >
                  <option value="00:00">00:00 - 02:00</option>
                  <option value="02:00">02:00 - 04:00</option>
                  <option value="04:00">04:00 - 06:00</option>
                </select>
                <small>Horário preferencial para tarefas automáticas.</small>
              </label>
            </div>
          </article>
        </section>
      </form>
      {showDevicesModal && (
        <div className="config-modal-backdrop" role="dialog" aria-modal="true">
          <div className="config-modal">
            <header className="config-modal-header">
              <div>
                <p className="config-modal-kicker">Segurança</p>
                <h2 className="config-modal-title">Dispositivos conectados</h2>
                <p className="config-modal-subtitle">
                  Lista de dispositivos com acesso recente ao ambiente.
                </p>
              </div>
              <button
                type="button"
                className="config-modal-close"
                onClick={() => setShowDevicesModal(false)}
              >
                Fechar
              </button>
            </header>
            <ul className="config-modal-list">
              {devices.map((device) => (
                <li key={device.id} className="config-device-item">
                  <div className="config-device-info">
                    {editingDeviceId === device.id ? (
                      <input
                        className="config-device-input"
                        type="text"
                        value={editingName}
                        onChange={(event) => setEditingName(event.target.value)}
                        onKeyDown={(event) => handleDeviceInputKeyDown(event, device.id)}
                        aria-label="Nome do dispositivo"
                      />
                    ) : (
                      <strong>{device.name}</strong>
                    )}
                    <span>{device.location}</span>
                  </div>
                  <div className="config-device-actions">
                    <span className="config-device-meta">{device.lastSeen}</span>
                    <div className="config-device-buttons">
                      {editingDeviceId === device.id ? (
                        <>
                          <button
                            type="button"
                            className="config-item-button"
                            onClick={() => handleSaveDeviceName(device.id)}
                          >
                            Salvar
                          </button>
                          <button
                            type="button"
                            className="config-cancel-button"
                            onClick={handleCancelEditDevice}
                          >
                            Cancelar
                          </button>
                        </>
                      ) : (
                        <button
                          type="button"
                          className="config-icon-button edit-button"
                          onClick={() => handleStartEditDevice(device.id)}
                          aria-label="Editar dispositivo"
                          title="Editar"
                        >
                          <FontAwesomeIcon icon={faPenToSquare} className="config-action-icon" />
                        </button>
                      )}
                      <button
                        type="button"
                        className="config-icon-button delete-button"
                        onClick={() => handleDisconnectDevice(device.id)}
                        aria-label="Desconectar dispositivo"
                        title="Desconectar"
                        disabled={editingDeviceId === device.id}
                      >
                        <FontAwesomeIcon icon={faPowerOff} className="config-action-icon" />
                      </button>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Configuracoes;
