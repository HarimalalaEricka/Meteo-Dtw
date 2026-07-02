<template>
  <div class="weather-card">
    <div class="card-header">
      <h3>{{ data.city }}</h3>
      <span class="weather-icon">{{ weatherIcon }}</span>
    </div>
    <div class="card-body">
      <div class="temp-main">
        <span class="temp-value">{{ formatTemp(data.temperature_c) }}</span>
        <span class="temp-unit">°C</span>
      </div>
      <p class="description">{{ data.description || 'N/A' }}</p>
      <div class="card-details">
        <div class="detail">
          <span class="detail-icon">💧</span>
          <span class="detail-label">Humidité</span>
          <span class="detail-value">{{ formatTemp(data.humidity_pct) }}%</span>
        </div>
        <div class="detail">
          <span class="detail-icon">💨</span>
          <span class="detail-label">Vent</span>
          <span class="detail-value">{{ formatTemp(data.wind_speed_kph) }} km/h</span>
        </div>
      </div>
    </div>
    <div class="card-footer">
      <small>{{ formatDate(data.recorded_at) }}</small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WeatherCard',
  props: {
    data: { type: Object, required: true }
  },
  computed: {
    weatherIcon() {
      const desc = (this.data.description || '').toLowerCase()
      if (desc.includes('rain') || desc.includes('pluie'))    return '🌧️'
      if (desc.includes('cloud') || desc.includes('nuage'))   return '☁️'
      if (desc.includes('clear') || desc.includes('clair'))   return '☀️'
      if (desc.includes('storm') || desc.includes('orage'))   return '⛈️'
      if (desc.includes('snow') || desc.includes('neige'))    return '❄️'
      if (desc.includes('mist') || desc.includes('brouillard')) return '🌫️'
      return '🌤️'
    }
  },
  methods: {
    formatDate(dt) {
      if (!dt) return ''
      return new Date(dt).toLocaleString('fr-FR', {
        day: '2-digit', month: 'short',
        hour: '2-digit', minute: '2-digit'
      })
    },
    formatTemp(value) {
        return value != null ? Number(value).toFixed(2) : '--';
    }
  }
}
</script>

<style scoped>
.weather-card {
  background: linear-gradient(145deg, #1a1a2e, #16213e);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #2a2a4a;
  transition: transform 0.3s, box-shadow 0.3s;
  min-width: 240px;
}

.weather-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(100, 255, 218, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card-header h3 {
  color: #e6e6e6;
  font-size: 1.1rem;
  margin: 0;
}

.weather-icon {
  font-size: 2rem;
}

.temp-main {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.25rem;
}

.temp-value {
  font-size: 3rem;
  font-weight: 700;
  color: #64ffda;
  line-height: 1;
}

.temp-unit {
  font-size: 1.2rem;
  color: #8892b0;
  margin-top: 0.3rem;
}

.description {
  color: #8892b0;
  font-size: 0.9rem;
  margin: 0.5rem 0 1rem;
  text-transform: capitalize;
}

.card-details {
  display: flex;
  gap: 1.5rem;
}

.detail {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.detail-icon {
  font-size: 1rem;
}

.detail-label {
  font-size: 0.7rem;
  color: #5a6a8a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 0.95rem;
  color: #e6e6e6;
  font-weight: 600;
}

.card-footer {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid #2a2a4a;
}

.card-footer small {
  color: #5a6a8a;
  font-size: 0.75rem;
}
</style>