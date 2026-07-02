<template>
  <div class="chart-container">
    <h3 class="chart-title">{{ title }}</h3>
    <Line v-if="chartData" :data="chartData" :options="chartOptions" />
    <p v-else class="no-data">Aucune donnée disponible</p>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale, LinearScale, PointElement,
  LineElement, Title, Tooltip, Legend, Filler
)

export default {
  name: 'TemperatureChart',
  components: { Line },
  props: {
    title:    { type: String, default: 'Température' },
    history:  { type: Array, default: () => [] },
    dataKey:  { type: String, default: 'temperature' },
    color:    { type: String, default: '#64ffda' },
    unit:     { type: String, default: '°C' }
  },
  computed: {
    chartData() {
        if (!this.history.length) return null

        const sorted = [...this.history].sort((a, b) => {
            const dateA = a.recorded_at || a.date_key
            const dateB = b.recorded_at || b.date_key
            return new Date(dateA) - new Date(dateB)
        })

        return {
            labels: sorted.map(d => {
            const dateStr = d.recorded_at || d.date_key
            if (!dateStr) return 'N/A'
            
            const [year, month, day] = dateStr.split('-')
            const date = new Date(year, month - 1, day)
            
            return date.toLocaleDateString('fr-FR', {
                day: '2-digit',
                month: 'short'
            })
            }),
            datasets: [
            {
                label: `${this.title} (${this.unit})`,
                data: sorted.map(d => d[this.dataKey]),
                borderColor: this.color,
                backgroundColor: this.color + '20',
                borderWidth: 2,
                pointRadius: 3,
                pointBackgroundColor: this.color,
                tension: 0.4,
                fill: true
            }
            ]
        }
        },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: '#8892b0', font: { size: 12 } }
          },
          tooltip: {
            backgroundColor: '#1a1a2e',
            titleColor: '#64ffda',
            bodyColor: '#e6e6e6',
            borderColor: '#2a2a4a',
            borderWidth: 1
          }
        },
        scales: {
          x: {
            ticks: { color: '#5a6a8a', maxTicksLimit: 10 },
            grid:  { color: '#1a1a2e' }
          },
          y: {
            ticks: { color: '#5a6a8a' },
            grid:  { color: '#1a1a2e' }
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  background: #1a1a2e;
  border-radius: 12px;
  padding: 1.5rem;
  height: 350px;
}

.chart-title {
  color: #e6e6e6;
  font-size: 1rem;
  margin: 0 0 1rem;
}

.no-data {
  color: #5a6a8a;
  text-align: center;
  padding: 3rem 0;
}
</style>