<template>
  <div class="alerts-page">
    <div class="page-header">
      <h1>🚨 Alertes Météo</h1>
      <p class="subtitle">Suivi des conditions extrêmes</p>
    </div>

    <CityFilter @filter-change="onFilterChange" />

    <!-- Résumé -->
    <section v-if="summary" class="section">
      <h2>📊 Résumé</h2>
      <div class="kpi-grid">
        <KpiCard icon="🚨" :value="totalAlerts"    label="Total alertes"    color="#ff5252" />
        <KpiCard icon="🔴" :value="criticalCount"  label="Critiques"        color="#ff5252" />
        <KpiCard icon="🟡" :value="warningCount"   label="Avertissements"   color="#ffc107" />
        <KpiCard icon="🔵" :value="infoCount"      label="Informations"     color="#2196f3" />
      </div>
    </section>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <span class="spinner"></span> Chargement...
    </div>

    <!-- Liste alertes -->
    <section v-else class="section">
      <h2>📋 Liste des alertes</h2>
      <div v-if="alerts.length" class="alerts-list">
        <AlertBadge
          v-for="(alert, i) in alerts"
          :key="i"
          :alert="alert"
        />
      </div>
      <div v-else class="empty-state">
        <span class="empty-icon">✅</span>
        <p>Aucune alerte active</p>
        <small>Toutes les conditions sont normales</small>
      </div>
    </section>
  </div>
</template>

<script>
import CityFilter from '../components/CityFilter.vue'
import KpiCard    from '../components/KpiCard.vue'
import AlertBadge from '../components/AlertBadge.vue'
import { getAlerts, getAlertsSummary } from '../api/weather'

export default {
  name: 'Alerts',
  components: { CityFilter, KpiCard, AlertBadge },
  data() {
    return {
      alerts:  [],
      summary: null,
      loading: true,
      filters: {}
    }
  },
  computed: {
    totalAlerts()  { return this.alerts.length },
    criticalCount() {
      return this.alerts.filter(a =>
        ['critical', 'danger'].includes((a.severity || '').toLowerCase())
      ).length
    },
    warningCount() {
      return this.alerts.filter(a =>
        ['warning', 'moyen'].includes((a.severity || '').toLowerCase())
      ).length
    },
    infoCount() {
      return this.alerts.filter(a =>
        ['info', 'low'].includes((a.severity || '').toLowerCase())
      ).length
    }
  },
  async mounted() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const [alerts, summary] = await Promise.allSettled([
          getAlerts(this.filters.city),
        //   getAlertsSummary()
        ])
        this.alerts  = alerts.status  === 'fulfilled' ? alerts.value  : []
        this.summary = summary.status === 'fulfilled' ? summary.value : null
      } catch (e) {
        console.error('Erreur Alerts:', e)
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
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: #5a6a8a;
}

.empty-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1.2rem;
  color: #64ffda;
  margin: 0;
}

.empty-state small {
  color: #5a6a8a;
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