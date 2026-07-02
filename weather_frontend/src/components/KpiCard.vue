<template>
  <div class="kpi-card" :style="{ borderLeftColor: color }">
    <div class="kpi-icon">{{ icon }}</div>
    <div class="kpi-content">
      <span class="kpi-value">{{ displayValue }}</span>
      <span class="kpi-label">{{ label }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KpiCard',
  props: {
    icon:   { type: String, default: '📊' },
    value:  { type: [Number, String], default: '--' },
    label:  { type: String, default: '' },
    unit:   { type: String, default: '' },
    color:  { type: String, default: '#64ffda' }
  },
  computed: {
    displayValue() {
      if (this.value === null || this.value === undefined) return '--'
      const v = typeof this.value === 'number' ? this.value.toFixed(1) : this.value
      return `${v}${this.unit}`
    }
  }
}
</script>

<style scoped>
.kpi-card {
  background: #1a1a2e;
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid #64ffda;
  transition: transform 0.2s;
}

.kpi-card:hover {
  transform: scale(1.02);
}

.kpi-icon {
  font-size: 2rem;
  min-width: 48px;
  text-align: center;
}

.kpi-content {
  display: flex;
  flex-direction: column;
}

.kpi-value {
  font-size: 1.6rem;
  font-weight: 700;
  color: #e6e6e6;
}

.kpi-label {
  font-size: 0.8rem;
  color: #5a6a8a;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
</style>