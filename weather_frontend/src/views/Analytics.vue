<template>
  <div class="analytics">
    <div class="page-header">
      <h1>📊 Analytics</h1>
      <p class="subtitle">Tendances et indicateurs</p>
    </div>

    <CityFilter
      :showDates="true"
      :showPeriod="true"
      @filter-change="onFilterChange"
    />

    <!-- KPIs -->
    <section v-if="history.length" class="section">
      <h2>📈 KPIs sur la période</h2>
      <div class="kpi-grid">
        <KpiCard icon="🌡️" :value="kpi.avgTemp"     label="Temp. moyenne"  unit="°C"    color="#64ffda" />
        <KpiCard icon="🔥" :value="kpi.maxTemp"     label="Temp. max"      unit="°C"    color="#ff5252" />
        <KpiCard icon="🥶" :value="kpi.minTemp"     label="Temp. min"      unit="°C"    color="#2196f3" />
        <KpiCard icon="💧" :value="kpi.avgHumidity" label="Humidité moy."  unit="%"     color="#ffc107" />
        <KpiCard icon="💨" :value="kpi.maxWind"     label="Vent max"       unit=" km/h" color="#8892b0" />
        <KpiCard icon="📅" :value="kpi.dataPoints"  label="Enregistrements" unit=""     color="#bb86fc" />
      </div>
    </section>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <span class="spinner"></span> Chargement...
    </div>

    <!-- Charts -->
    <section v-else-if="history.length" class="section">
      <h2>📉 Graphiques</h2>
      <div class="charts-grid">
        <TemperatureChart
            title="🌡️ Température"
            :history="history"
            dataKey="avg_temperature_c"
            color="#64ffda"
            unit="°C"
            />
            <TemperatureChart
            title="💧 Humidité"
            :history="history"
            dataKey="avg_humidity_pct"
            color="#ffc107"
            unit="%"
            />
            <TemperatureChart
            title="💨 Vent"
            :history="history"
            dataKey="avg_wind_speed_kph"
            color="#ff5252"
            unit="km/h"
            />
      </div>
    </section>

    <p v-else class="empty">
      Sélectionnez une ville et une période pour afficher les analytics
    </p>
  </div>
</template>

<script>
import CityFilter       from '../components/CityFilter.vue'
import KpiCard          from '../components/KpiCard.vue'
import TemperatureChart from '../components/TemperatureChart.vue'
import { getWeatherHistory } from '../api/weather'

export default {
  name: 'Analytics',
  components: { CityFilter, KpiCard, TemperatureChart },
  data() {
    return {
      history: [],
      loading: false,
      filters: {}
    }
  },
  computed: {
    kpi() {
      if (!this.history.length) return {}
      const temps = this.history.map(h => h.avg_temperature_c).filter(v => v != null)
      console.log('Temps:', temps)
      const humid = this.history.map(h => h.avg_humidity_pct).filter(v => v != null)
      const winds = this.history.map(h => h.avg_wind_speed_kph).filter(v => v != null)
      return {
        avgTemp:     temps.length ? (temps.reduce((a, b) => a + b, 0) / temps.length)  : null,
        maxTemp:     temps.length ? Math.max(...temps) : null,
        minTemp:     temps.length ? Math.min(...temps) : null,
        avgHumidity: humid.length ? (humid.reduce((a, b) => a + b, 0) / humid.length)  : null,
        maxWind:     winds.length ? Math.max(...winds) : null,
        dataPoints:  this.history.length
      }
    }
  },
  methods: {
    async onFilterChange(filters) {
      this.filters = filters
      this.loading = true
      try {
        this.history = await getWeatherHistory(
          filters.city,
          filters.dateFrom,
          filters.dateTo
        )
      } catch (e) {
        console.error('Erreur Analytics:', e)
        this.history = []
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
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

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
}

.empty {
  color: #5a6a8a;
  text-align: center;
  padding: 3rem;
  font-size: 1.1rem;
}

.loading {
  text-align: center;
  color: #64ffda;
  padding: 3rem;
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