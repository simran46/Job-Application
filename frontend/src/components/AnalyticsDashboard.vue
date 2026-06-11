<template>
  <div class="analytics-overlay" @click.self="$emit('close')">
    <div class="analytics-modal">
      <!-- Header -->
      <div class="modal-header">
        <h2 class="modal-title">Analytics Dashboard</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <!-- Charts Grid -->
      <div class="charts-grid" v-if="jobs.length > 0">
        <!-- Status Chart Card -->
        <div class="chart-card">
          <h3 class="chart-title">Jobs by Status</h3>
          <div class="chart-content">
            <donut-chart :data="statusChartData" />
          </div>
        </div>

        <!-- City Chart Card -->
        <div class="chart-card">
          <h3 class="chart-title">Jobs by City</h3>
          <div class="chart-content">
            <donut-chart :data="cityChartData" />
          </div>
        </div>

        <!-- State Chart Card -->
        <div class="chart-card">
          <h3 class="chart-title">Jobs by State</h3>
          <div class="chart-content">
            <donut-chart :data="stateChartData" />
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-analytics">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="empty-icon">
          <line x1="18" y1="20" x2="18" y2="10"></line>
          <line x1="12" y1="20" x2="12" y2="4"></line>
          <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
        <p>No job postings available to analyze. Post some jobs to view the charts!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import DonutChart from './DonutChart.vue';

const props = defineProps({
  jobs: {
    type: Array,
    required: true
  }
});

defineEmits(['close']);

// Helper to count and format values
const computeDistribution = (key, isList = false) => {
  const counts = {};
  
  props.jobs.forEach(job => {
    const rawVal = job[key];
    if (isList) {
      const list = Array.isArray(rawVal) ? rawVal : [];
      if (list.length === 0) {
        counts['Unspecified'] = (counts['Unspecified'] || 0) + 1;
      } else {
        list.forEach(item => {
          counts[item] = (counts[item] || 0) + 1;
        });
      }
    } else {
      const val = rawVal ? rawVal.trim() : 'Unspecified';
      counts[val] = (counts[val] || 0) + 1;
    }
  });

  return Object.entries(counts).map(([name, count]) => ({
    name,
    count
  }));
};

const statusChartData = computed(() => computeDistribution('status', true));
const cityChartData = computed(() => computeDistribution('city'));
const stateChartData = computed(() => computeDistribution('state'));
</script>

<style scoped>
.analytics-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.analytics-modal {
  background: var(--bg-modal);
  border: 1px solid var(--border-color);
  border-radius: 24px;
  width: 100%;
  max-width: 1100px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  padding: 24px;
  animation: modal-zoom 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modal-zoom {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 16px;
  margin-bottom: 24px;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
  background: linear-gradient(135deg, #ffffff 0%, var(--primary-color) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 2rem;
  line-height: 1;
  cursor: pointer;
  transition: color 0.2s;
}

.close-btn:hover {
  color: var(--text-main);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 24px;
}

.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.chart-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-main);
  border-left: 4px solid var(--primary-color);
  padding-left: 10px;
}

.chart-content {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 250px;
}

.empty-analytics {
  padding: 60px 20px;
  text-align: center;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-icon {
  width: 48px;
  height: 48px;
  color: var(--text-muted);
}
</style>
