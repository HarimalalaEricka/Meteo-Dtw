<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>🏠 Dashboard Météo</h1>
      <p class="subtitle">Vue d'ensemble — Madagascar</p>
    </div>

    <CityFilter @filter-change="onFilterChange" />

    <!-- Alertes actives -->
    <section v-if="alerts.length" class="section alerts-banner">
      <h2>🚨 Alertes actives ({{ alerts.length }})</h2>
      <div class="alerts-scroll">
        <AlertBadge
          v-for="(alert, i) in alerts.slice(0, 3)"
          :key="i"
          :alert="alert"
        />
      </div>
    </section>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <span class="spinner"></span> Chargement...
    </div>

    <!-- Météo actuelle -->
    <section v-else class="section">
      <h2>☀️ Météo actuelle</h2>
      <div v-if="todayWeather.length" class="weather-grid">
        <WeatherCard
          v-for="(w, i) in todayWeather"
          :key="i"
          :data="w"
        />
      </div>
      <p v-else class="empty">Aucune donnée météo disponible</p>
    </section>

    <!-- KPI rapides -->
    <section v-if="todayWeather.length" class="section">
      <h2>📊 Résumé</h2>
      <div class="kpi-grid">
        <KpiCard icon="🌡️" :value="avgTemp"     label="Temp. moyenne"  unit="°C" color="#64ffda" />
        <KpiCard icon="🔥" :value="maxTemp"     label="Temp. max"      unit="°C" color="#ff5252" />
        <KpiCard icon="🥶" :value="minTemp"     label="Temp. min"      unit="°C" color="#2196f3" />
        <KpiCard icon="💧" :value="avgHumidity" label="Humidité moy."  unit="%"  color="#ffc107" />
        <KpiCard icon="💨" :value="avgWind"     label="Vent moyen"     unit=" km/h" color="#8892b0" />
        <KpiCard icon="🏙️" :value="cityCount"  label="Villes"         unit=""   color="#bb86fc" />
      </div>
    </section>
  </div>
</template>

<script>
import CityFilter  from '../components/CityFilter.vue'
import WeatherCard from '../components/WeatherCard.vue'
import KpiCard     from '../components/KpiCard.vue'
import AlertBadge  from '../components/AlertBadge.vue'
import { getWeatherToday, getAlerts } from '../api/weather'

export default {
  name: 'Dashboard',
  components: { CityFilter, WeatherCard, KpiCard, AlertBadge },
  data() {
    return {
      todayWeather: [],
      alerts: [],
      loading: true,
      filters: { city: null }
    }
  },
  computed: {
    temps()       { return this.todayWeather.map(w => w.temperature_c).filter(t => t != null) },
    avgTemp()     { return this.temps.length ? (this.temps.reduce((a, b) => a + b, 0) / this.temps.length) : null },
    maxTemp()     { return this.temps.length ? Math.max(...this.temps) : null },
    minTemp()     { return this.temps.length ? Math.min(...this.temps) : null },
    avgHumidity() {
      const h = this.todayWeather.map(w => w.humidity_pct).filter(v => v != null)
      return h.length ? (h.reduce((a, b) => a + b, 0) / h.length) : null
    },
    avgWind() {
      const w = this.todayWeather.map(x => x.wind_speed_kph).filter(v => v != null)
      return w.length ? (w.reduce((a, b) => a + b, 0) / w.length) : null
    },
    cityCount() {
      return new Set(this.todayWeather.map(w => w.city)).size
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const [weather, alerts] = await Promise.allSettled([
          getWeatherToday(this.filters.city),
          getAlerts(this.filters.city)
        ])
        this.todayWeather = weather.status === 'fulfilled' ? weather.value : []
        this.alerts       = alerts.status  === 'fulfilled' ? alerts.value  : []
      } catch (e) {
        console.error('Erreur Dashboard:', e)
      } finally {
        this.loading = false
      }
    },
    async onFilterChange(filters) {
      this.filters = filters
      await this.loadData()
    }
  }
}
</script>

<style scoped>
.page-header {
  margin-bottom: 1.5rem;
}

.page-header h1 {
  color: #e6e6e6;
  font-size: 1.8rem;
  margin: 0;
}

.subtitle {
  color: #5a6a8a;
  margin: 0.25rem 0 0;
}

.section {
  margin-bottom: 2rem;
}

.section h2 {
  color: #ccd6f6;
  font-size: 1.15rem;
  margin: 0 0 1rem;
}

.weather-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1.25rem;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.alerts-banner {
  background: rgba(255, 82, 82, 0.05);
  border-radius: 12px;
  padding: 1.25rem;
  border: 1px solid rgba(255, 82, 82, 0.2);
}

.alerts-scroll {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
}

.empty {
  color: #5a6a8a;
  text-align: center;
  padding: 2rem;
}

.loading {
  text-align: center;
  color: #64ffda;
  padding: 3rem;
  font-size: 1.1rem;
}

.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid #64ffda;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 0.5rem;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>