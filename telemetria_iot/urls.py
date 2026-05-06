from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def api_root(request):
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Telemetría Maicao API</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #0a0e27 0%, #0f1729 50%, #1e3a5f 100%);
    min-height: 100vh;
    color: #f1f5f9;
    padding: 2rem 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .container {
    max-width: 900px;
    width: 100%;
  }
  .card {
    background: rgba(15, 23, 41, 0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(34, 211, 238, 0.2);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    box-shadow: 0 25px 60px rgba(0,0,0,0.5), 0 0 80px rgba(6,182,212,0.1);
  }
  .header {
    text-align: center;
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid rgba(148,163,184,0.1);
  }
  .logo {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
  h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
  }
  .subtitle {
    color: #94a3b8;
    font-size: 1rem;
    margin-bottom: 1rem;
  }
  .badges {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-top: 1rem;
  }
  .badge {
    font-size: 0.75rem;
    padding: 0.3rem 0.8rem;
    background: rgba(6,182,212,0.1);
    border: 1px solid rgba(6,182,212,0.3);
    border-radius: 12px;
    color: #22d3ee;
    font-weight: 500;
  }
  .badge.success {
    background: rgba(34,197,94,0.1);
    border-color: rgba(34,197,94,0.3);
    color: #22c55e;
  }
  .section {
    margin-bottom: 2rem;
  }
  .section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #f1f5f9;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 0.75rem;
  }
.endpoint {
    background: rgba(15,23,41,0.5);
    border: 1px solid rgba(148,163,184,0.1);
    border-radius: 10px;
    padding: 0.85rem 1rem;
    transition: all 0.2s;
    text-decoration: none;
    display: block;
    cursor: pointer;
  }
  .endpoint:hover {
    background: rgba(15,23,41,0.8);
    border-color: rgba(34,211,238,0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(6,182,212,0.15);
  }
  .endpoint-name {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-bottom: 0.2rem;
  }
  .endpoint-url {
    font-size: 0.85rem;
    color: #22d3ee;
    font-family: 'Courier New', monospace;
    font-weight: 600;
  }
  .info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
  }
  .info-item {
    background: rgba(15,23,41,0.5);
    border: 1px solid rgba(148,163,184,0.1);
    border-radius: 10px;
    padding: 1rem;
  }
  .info-label {
    font-size: 0.75rem;
    color: #94a3b8;
    margin-bottom: 0.3rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .info-value {
    font-size: 0.95rem;
    color: #f1f5f9;
    font-weight: 500;
  }
  .footer {
    text-align: center;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(148,163,184,0.1);
    color: #64748b;
    font-size: 0.8rem;
  }
  .frontend-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #06b6d4, #3b82f6);
    color: white;
    padding: 0.85rem 1.5rem;
    border-radius: 12px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    margin-top: 1rem;
    transition: all 0.2s;
    box-shadow: 0 8px 24px rgba(6,182,212,0.3);
  }
  .frontend-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(6,182,212,0.4);
  }
  .status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #22c55e;
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(34,197,94,0.6);
    animation: pulse 2s ease-in-out infinite;
    margin-right: 6px;
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.6; transform: scale(0.85); }
  }
  @media (max-width: 600px) {
    .info-grid { grid-template-columns: 1fr; }
    h1 { font-size: 1.5rem; }
    .card { padding: 2rem 1.5rem; }
  }
</style>
</head>
<body>
<div class="container">
  <div class="card">
    <div class="header">
      <div class="logo">💧</div>
      <h1>Telemetría Maicao API</h1>
      <p class="subtitle">Sistema de Telemetría IoT para Monitoreo Remoto de Niveles de Agua</p>
      <div class="badges">
        <span class="badge success"><span class="status-dot"></span>Online</span>
        <span class="badge">Django REST</span>
        <span class="badge">JWT Auth</span>
        <span class="badge">MySQL</span>
        <span class="badge">v1.0.0</span>
      </div>
      <a href="https://telemetria-maicao-frontend-production.up.railway.app" target="_blank" class="frontend-btn">
        🚀 Ir a la aplicación
      </a>
    </div>

    <div class="section">
      <div class="section-title">📡 Endpoints disponibles</div>
      <div class="grid">
        <a href="/admin/" target="_blank" class="endpoint">
          <div class="endpoint-name">Panel Admin</div>
          <div class="endpoint-url">/admin/ →</div>
        </a>
        <a href="/api/token/" target="_blank" class="endpoint">
          <div class="endpoint-name">Login JWT</div>
          <div class="endpoint-url">/api/token/ →</div>
        </a>
        <a href="/api/token/refresh/" target="_blank" class="endpoint">
          <div class="endpoint-name">Refresh Token</div>
          <div class="endpoint-url">/api/token/refresh/ →</div>
        </a>
        <a href="/api/users/" target="_blank" class="endpoint">
          <div class="endpoint-name">Usuarios y Roles</div>
          <div class="endpoint-url">/api/users/ →</div>
        </a>
        <a href="/api/tanks/" target="_blank" class="endpoint">
          <div class="endpoint-name">Tanques</div>
          <div class="endpoint-url">/api/tanks/ →</div>
        </a>
        <a href="/api/readings/" target="_blank" class="endpoint">
          <div class="endpoint-name">Lecturas ESP32</div>
          <div class="endpoint-url">/api/readings/ →</div>
        </a>
        <a href="/api/alerts/" target="_blank" class="endpoint">
          <div class="endpoint-name">Alertas</div>
          <div class="endpoint-url">/api/alerts/ →</div>
        </a>
        <a href="/api/system/logs/" target="_blank" class="endpoint">
          <div class="endpoint-name">Logs del Sistema</div>
          <div class="endpoint-url">/api/system/logs/ →</div>
        </a>
        <div class="endpoint">
          <div class="endpoint-name">Login JWT</div>
          <div class="endpoint-url">/api/token/</div>
        </div>
        <div class="endpoint">
          <div class="endpoint-name">Refresh Token</div>
          <div class="endpoint-url">/api/token/refresh/</div>
        </div>
        <div class="endpoint">
          <div class="endpoint-name">Usuarios y Roles</div>
          <div class="endpoint-url">/api/users/</div>
        </div>
        <div class="endpoint">
          <div class="endpoint-name">Tanques</div>
          <div class="endpoint-url">/api/tanks/</div>
        </div>
        <div class="endpoint">
          <div class="endpoint-name">Lecturas ESP32</div>
          <div class="endpoint-url">/api/readings/</div>
        </div>
        <div class="endpoint">
          <div class="endpoint-name">Alertas</div>
          <div class="endpoint-url">/api/alerts/</div>
        </div>
        <div class="endpoint">
          <div class="endpoint-name">Logs del Sistema</div>
          <div class="endpoint-url">/api/system/logs/</div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">📋 Información del proyecto</div>
      <div class="info-grid">
        <div class="info-item">
          <div class="info-label">Institución</div>
          <div class="info-value">Universidad de La Guajira</div>
        </div>
        <div class="info-item">
          <div class="info-label">Ubicación</div>
          <div class="info-value">Maicao, La Guajira</div>
        </div>
        <div class="info-item">
          <div class="info-label">Programa</div>
          <div class="info-value">Ingeniería de Sistemas</div>
        </div>
        <div class="info-item">
          <div class="info-label">Año</div>
          <div class="info-value">2026</div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-title">👥 Equipo de desarrollo</div>
      <div class="grid">
        <div class="endpoint">
          <div class="endpoint-name">Desarrollador</div>
          <div class="endpoint-url">Florez Pedro</div>
        </div>
        <div class="endpoint">
          <div class="endpoint-name">Desarrollador</div>
          <div class="endpoint-url">Maldonado Juan</div>
        </div>
        <div class="endpoint">
          <div class="endpoint-name">Desarrollador</div>
          <div class="endpoint-url">Ortiz Darien</div>
        </div>
      </div>
    </div>

    <div class="footer">
      <p>Sistema de Telemetría IoT · Diseño e Implementación con ESP32 · MQTT · Django · Angular</p>
    </div>
  </div>
</div>
</body>
</html>
"""
    return HttpResponse(html)


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/tanks/', include('tanks.urls')),
    path('api/readings/', include('readings.urls')),
    path('api/alerts/', include('alerts.urls')),
    path('api/system/', include('system_logs.urls')),
]