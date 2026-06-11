<template>
  <div class="donut-container">
    <!-- SVG Donut Chart -->
    <div class="donut-chart-wrapper">
      <svg viewBox="-120 -120 240 240" class="donut-svg">
        <!-- Background circle for 0 items -->
        <circle 
          v-if="chartSlices.length === 0" 
          cx="0" 
          cy="0" 
          r="80" 
          fill="none" 
          stroke="var(--border-color)" 
          stroke-width="32" 
        />
        
        <!-- Slices -->
        <template v-else>
          <!-- Single full 100% item case -->
          <circle 
            v-if="chartSlices.length === 1" 
            cx="0" 
            cy="0" 
            r="80" 
            fill="none" 
            :stroke="chartSlices[0].color" 
            stroke-width="32" 
            class="donut-segment"
            @mouseenter="hoveredIndex = 0"
            @mouseleave="hoveredIndex = null"
            :class="{ 'is-hovered': hoveredIndex === 0 }"
          />
          
          <!-- Multiple items paths -->
          <path 
            v-for="(slice, index) in chartSlices" 
            v-else
            :key="index"
            :d="slice.pathData"
            :fill="slice.color"
            class="donut-slice"
            :class="{ 'is-hovered': hoveredIndex === index }"
            @mouseenter="hoveredIndex = index"
            @mouseleave="hoveredIndex = null"
          />
        </template>
        
        <!-- Center Donut Hole (makes it a donut rather than a pie chart) -->
        <!-- We match the background of the donut hole to the card background -->
        <circle 
          cx="0" 
          cy="0" 
          r="64" 
          fill="var(--bg-card)" 
        />
        
        <!-- Text inside Center Donut Hole -->
        <g class="donut-center-text">
          <text 
            x="0" 
            y="-6" 
            text-anchor="middle" 
            class="center-value"
          >
            {{ centerValue }}
          </text>
          <text 
            x="0" 
            y="18" 
            text-anchor="middle" 
            class="center-label"
          >
            {{ centerLabel }}
          </text>
        </g>
      </svg>
    </div>

    <!-- Legends on the side -->
    <div class="donut-legend">
      <div 
        v-for="(item, index) in chartSlices" 
        :key="index" 
        class="legend-item"
        :class="{ 'is-active': hoveredIndex === index }"
        @mouseenter="hoveredIndex = index"
        @mouseleave="hoveredIndex = null"
      >
        <span class="legend-color-dot" :style="{ backgroundColor: item.color }"></span>
        <span class="legend-name" :title="item.name">{{ item.name }}</span>
        <span class="legend-value">{{ item.count }} ({{ Math.round(item.percent * 100) }}%)</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  }
});

const hoveredIndex = ref(null);

const colors = [
  '#6366f1', // indigo
  '#10b981', // emerald
  '#f59e0b', // amber
  '#3b82f6', // blue
  '#ec4899', // pink
  '#8b5cf6', // purple
  '#14b8a6', // teal
  '#f43f5e', // rose
  '#06b6d4', // cyan
  '#84cc16'  // lime
];

const totalCount = computed(() => {
  return props.data.reduce((sum, item) => sum + item.count, 0);
});

const chartSlices = computed(() => {
  if (totalCount.value === 0) return [];
  
  let cumulativePercent = 0;
  
  // Sort data descending by count to make the chart look structured
  const sortedData = [...props.data].sort((a, b) => b.count - a.count);
  
  return sortedData.map((item, index) => {
    const percent = item.count / totalCount.value;
    const color = colors[index % colors.length];
    
    // Trigonometry coordinates for SVG Path (we use donut thickness with inner radius 64 and outer radius 96)
    // Radius values
    const rOuter = 80;
    const rInner = 48; // To draw donut wedges, we need outer arc and inner arc
    
    // We compute angles in radians (shifted by -Math.PI / 2 to start at top)
    const startAngle = (startPercent) => (2 * Math.PI * startPercent) - (Math.PI / 2);
    
    const startPercent = cumulativePercent;
    cumulativePercent += percent;
    const endPercent = cumulativePercent;
    
    const angle1 = startAngle(startPercent);
    const angle2 = startAngle(endPercent);
    
    const x1_out = Math.cos(angle1) * rOuter;
    const y1_out = Math.sin(angle1) * rOuter;
    const x2_out = Math.cos(angle2) * rOuter;
    const y2_out = Math.sin(angle2) * rOuter;
    
    const x1_in = Math.cos(angle1) * rInner;
    const y1_in = Math.sin(angle1) * rInner;
    const x2_in = Math.cos(angle2) * rInner;
    const y2_in = Math.sin(angle2) * rInner;
    
    const largeArcFlag = percent > 0.5 ? 1 : 0;
    
    // SVG Path for Donut Wedge:
    // Move to outer start point
    // Arc to outer end point
    // Line to inner end point
    // Arc back to inner start point (sweep-flag is 0 to go counter-clockwise)
    // Close path
    const pathData = [
      `M ${x1_out} ${y1_out}`,
      `A ${rOuter} ${rOuter} 0 ${largeArcFlag} 1 ${x2_out} ${y2_out}`,
      `L ${x2_in} ${y2_in}`,
      `A ${rInner} ${rInner} 0 ${largeArcFlag} 0 ${x1_in} ${y1_in}`,
      `Z`
    ].join(' ');
    
    return {
      name: item.name,
      count: item.count,
      percent,
      color,
      pathData
    };
  });
});

// Dynamic values inside center hole based on segments hovered
const centerValue = computed(() => {
  if (hoveredIndex.value !== null && chartSlices.value[hoveredIndex.value]) {
    return chartSlices.value[hoveredIndex.value].count;
  }
  return totalCount.value;
});

const centerLabel = computed(() => {
  if (hoveredIndex.value !== null && chartSlices.value[hoveredIndex.value]) {
    const item = chartSlices.value[hoveredIndex.value];
    const pctStr = `${Math.round(item.percent * 100)}%`;
    // If the label is too long, truncate it
    const name = item.name;
    const truncatedName = name.length > 9 ? name.substring(0, 8) + '..' : name;
    return `${truncatedName} (${pctStr})`;
  }
  return 'Total Jobs';
});
</script>

<style scoped>
.donut-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  width: 100%;
}

.donut-chart-wrapper {
  position: relative;
  width: 180px;
  height: 180px;
}

.donut-svg {
  width: 100%;
  height: 100%;
}

.donut-slice {
  cursor: pointer;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.2s;
  transform-origin: 0px 0px;
}

.donut-slice:hover,
.donut-slice.is-hovered {
  transform: scale(1.06);
  filter: brightness(1.1);
  opacity: 0.95;
}

.donut-segment {
  cursor: pointer;
  transition: stroke-width 0.2s, opacity 0.2s;
}

.donut-segment.is-hovered {
  stroke-width: 38;
}

.donut-center-text {
  pointer-events: none;
  font-family: inherit;
}

.center-value {
  font-size: 1.65rem;
  font-weight: 700;
  fill: var(--text-main);
  dominant-baseline: middle;
}

.center-label {
  font-size: 0.75rem;
  font-weight: 500;
  fill: var(--text-muted);
  dominant-baseline: middle;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.donut-legend {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 140px;
  overflow-y: auto;
  padding-right: 4px;
}

/* Custom scrollbar for legend */
.donut-legend::-webkit-scrollbar {
  width: 4px;
}
.donut-legend::-webkit-scrollbar-track {
  background: transparent;
}
.donut-legend::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 2px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
  color: var(--text-secondary);
  padding: 4px 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.legend-item:hover,
.legend-item.is-active {
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main);
}

.legend-color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.legend-name {
  flex-grow: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 500;
}

.legend-value {
  font-weight: 600;
  flex-shrink: 0;
}
</style>
