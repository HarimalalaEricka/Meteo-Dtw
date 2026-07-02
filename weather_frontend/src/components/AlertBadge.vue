<template>
  <div :class="['alert-badge', severityClass]">
    <div class="alert-header">
      <span class="alert-icon">{{ alertIcon }}</span>
      <span class="alert-type">{{ alert.alert_type || alert.type }}</span>
      <span class="alert-severity">{{ alert.severity }}</span>
    </div>
    <div class="alert-body">
      <p class="alert-city">📍 {{ alert.city || alert.city_name }}</p>
      <p class="alert-message">{{ alert.message || alert.description }}</p>
    </div>
    <div class="alert-footer">
      <small>{{ formatDate(alert.triggered_at || alert.created_at) }}</small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AlertBadge',
  props: {
    alert: { type: Object, required: true }
  },
  computed: {
    severityClass() {
      const s = (this.alert.severity || '').toLowerCase()
      if (s === 'critical' || s === 'danger')  return 'severity-critical'
      if (s === 'warning'  || s === 'moyen')   return 'severity-warning'
      return 'severity-info'
    },
    alertIcon() {
      const type = (this.alert.alert_type || this.alert.type || '').toLowerCase()
      if (type.includes('heat') || type.includes('canicule'))  return '🔥'
      if (type.includes('cold') || type.includes('froid'))     return '🥶'
      if (type.includes('rain') || type.includes('pluie'))     return '🌧️'
      if (type.includes('wind') || type.includes('vent'))      return '💨'
      if (type.includes('storm') || type.includes('orage'))    return '⛈️'
      return '⚠️'
    }
  },
  methods: {
    formatDate(dt) {
      if (!dt) return ''
      return new Date(dt).toLocaleString('fr-FR', {
        day: '2-digit', month: 'short',
        hour: '2-digit', minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.alert-badge {
  border-radius: 12px;
  padding: 1.25rem;
  border-left: 4px solid;
  transition: transform 0.2s;
}

.alert-badge:hover {
  transform: translateX(4px);
}

.severity-critical {
  background: rgba(255, 82, 82, 0.1);
  border-left-color: #ff5252;
}

.severity-warning {
  background: rgba(255, 193, 7, 0.1);
  border-left-color: #ffc107;
}

.severity-info {
  background: rgba(33, 150, 243, 0.1);
  border-left-color: #2196f3;
}

.alert-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.alert-icon {
  font-size: 1.5rem;
}

.alert-type {
  color: #e6e6e6;
  font-weight: 700;
  text-transform: uppercase;
  font-size: 0.9rem;
}

.alert-severity {
  margin-left: auto;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
}

.severity-critical .alert-severity {
  background: #ff5252;
  color: #fff;
}

.severity-warning .alert-severity {
  background: #ffc107;
  color: #1a1a2e;
}

.severity-info .alert-severity {
  background: #2196f3;
  color: #fff;
}

.alert-city {
  color: #8892b0;
  font-size: 0.85rem;
  margin: 0 0 0.3rem;
}

.alert-message {
  color: #ccd6f6;
  font-size: 0.9rem;
  margin: 0;
}

.alert-footer {
  margin-top: 0.75rem;
}

.alert-footer small {
  color: #5a6a8a;
}
</style>