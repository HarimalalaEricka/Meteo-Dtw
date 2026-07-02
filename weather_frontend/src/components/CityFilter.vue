<template>
  <div class="filter-bar">
    <div class="filter-group">
      <label>🏙️ Ville</label>
      <select v-model="selectedCity" @change="emitFilters">
        <option value="">Toutes les villes</option>
        <option
            v-for="c in cities"
            :key="c.city_name"
            :value="c.city_name"
            >
            {{ c.city_name }}
        </option>
      </select>
    </div>

    <div class="filter-group" v-if="showDates">
      <label>📅 Du</label>
      <input type="date" v-model="dateFrom" @change="emitFilters" />
    </div>

    <div class="filter-group" v-if="showDates">
      <label>📅 Au</label>
      <input type="date" v-model="dateTo" @change="emitFilters" />
    </div>

    <div class="filter-group" v-if="showPeriod">
      <label>⏱️ Période</label>
      <div class="period-buttons">
        <button
          v-for="p in periods"
          :key="p.value"
          :class="['period-btn', { active: period === p.value }]"
          @click="setPeriod(p.value)"
        >
          {{ p.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { getCities } from '../api/weather'

export default {
  name: 'CityFilter',
  props: {
    showDates:  { type: Boolean, default: false },
    showPeriod: { type: Boolean, default: false }
  },
  emits: ['filter-change'],
  data() {
    return {
      cities: [],
      selectedCity: '',
      dateFrom: '',
      dateTo: '',
      period: 7,
      periods: [
        { label: '7j',  value: 7 },
        { label: '14j', value: 14 },
        { label: '30j', value: 30 }
      ]
    }
  },
  async mounted() {
    try {
      this.cities = await getCities()
      console.log(this.cities)
    } catch (e) {
      console.error('Erreur chargement villes:', e)
    }
  },
  methods: {
    emitFilters() {
      this.$emit('filter-change', {
        city:     this.selectedCity || null,
        dateFrom: this.dateFrom || null,
        dateTo:   this.dateTo || null,
        period:   this.period
      })
    },
    setPeriod(val) {
      this.period = val
      const now = new Date()
      this.dateTo   = now.toISOString().split('T')[0]
      const from    = new Date(now)
      from.setDate(from.getDate() - val)
      this.dateFrom = from.toISOString().split('T')[0]
      this.emitFilters()
    }
  }
}
</script>

<style scoped>
.filter-bar {
  display: flex;
  gap: 1.5rem;
  align-items: flex-end;
  padding: 1.25rem 1.5rem;
  background: #1a1a2e;
  border-radius: 12px;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.filter-group label {
  font-size: 0.8rem;
  color: #8892b0;
  font-weight: 600;
}

select, input[type="date"] {
  padding: 0.6rem 1rem;
  border-radius: 8px;
  border: 1px solid #2a2a4a;
  background: #0a0a1a;
  color: #e6e6e6;
  font-size: 0.9rem;
  min-width: 160px;
}

select:focus, input:focus {
  outline: none;
  border-color: #64ffda;
}

.period-buttons {
  display: flex;
  gap: 0.4rem;
}

.period-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #2a2a4a;
  background: #0a0a1a;
  color: #8892b0;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.period-btn:hover {
  border-color: #64ffda;
  color: #64ffda;
}

.period-btn.active {
  background: #64ffda;
  color: #0a0a1a;
  border-color: #64ffda;
}
</style>