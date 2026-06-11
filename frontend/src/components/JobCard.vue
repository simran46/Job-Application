<template>
  <div class="job-card" :class="{ 'is-deleting': isDeleting }">
    <!-- Header with profile picture & quick actions -->
    <div class="card-header">
      <div class="profile-pic-container">
        <img 
          v-if="job.profile_picture" 
          :src="getImageUrl(job.profile_picture)" 
          alt="Job Profile" 
          class="profile-pic"
          @error="handleImageError"
        />
        <div v-else class="profile-pic-fallback">
          {{ getInitials(job.title) }}
        </div>
      </div>
      
      <!-- Action Buttons -->
      <div class="action-buttons">
        <button 
          class="action-btn edit-btn" 
          title="Edit Job" 
          @click="$emit('edit', job)"
        >
          <!-- Edit Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-svg">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 1 1 3 3L12 15l-4 1 1-4z"></path>
          </svg>
        </button>
        <button 
          class="action-btn duplicate-btn" 
          title="Duplicate Job" 
          @click="$emit('duplicate', job.id)"
        >
          <!-- Copy/Duplicate Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-svg">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
        </button>
        <button 
          class="action-btn delete-btn" 
          title="Delete Job" 
          @click="triggerDelete"
        >
          <!-- Trash Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon-svg">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Title & Badges -->
    <div class="card-body">
      <h3 class="job-title">{{ job.title }}</h3>
      
      <!-- Category Tags -->
      <div class="category-tags">
        <span 
          v-for="cat in job.category" 
          :key="cat" 
          class="category-tag"
        >
          {{ cat }}
        </span>
      </div>
      
      <!-- Status Badges -->
      <div class="status-tags">
        <span 
          v-for="status in job.status" 
          :key="status" 
          class="status-tag"
          :class="getStatusClass(status)"
        >
          <span class="status-dot"></span>
          {{ status }}
        </span>
      </div>
      
      <!-- Job Description -->
      <p v-if="job.description" class="job-description">
        {{ job.description }}
      </p>
      
      <!-- Details Meta (Dates, Location) -->
      <div class="card-meta">
        <!-- Location Info -->
        <div class="meta-item location-info" v-if="job.address || job.city || job.state">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="meta-icon">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
            <circle cx="12" cy="10" r="3"></circle>
          </svg>
          <span class="meta-text">
            {{ formatLocation(job) }}
          </span>
        </div>
        
        <!-- Date Info -->
        <div class="meta-item date-info" v-if="job.start_date || job.end_date">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="meta-icon">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="16" y1="2" x2="16" y2="6"></line>
            <line x1="8" y1="2" x2="8" y2="6"></line>
            <line x1="3" y1="10" x2="21" y2="10"></line>
          </svg>
          <span class="meta-text">
            {{ formatDateRange(job.start_date, job.end_date) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  job: {
    type: Object,
    required: true
  },
  backendUrl: {
    type: String,
    default: 'http://localhost:8000'
  }
});

const emit = defineEmits(['edit', 'delete', 'duplicate']);

const isDeleting = ref(false);

const getImageUrl = (path) => {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  return `${props.backendUrl}${path.startsWith('/') ? '' : '/'}${path}`;
};

const getInitials = (title) => {
  if (!title) return 'JP';
  return title
    .split(' ')
    .slice(0, 2)
    .map(word => word[0])
    .join('')
    .toUpperCase();
};

const formatLocation = (job) => {
  const parts = [];
  if (job.address) parts.push(job.address);
  if (job.city) parts.push(job.city);
  if (job.state) parts.push(job.state);
  return parts.join(', ');
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

const formatDateRange = (start, end) => {
  if (start && end) {
    return `${formatDate(start)} - ${formatDate(end)}`;
  } else if (start) {
    return `Starts ${formatDate(start)}`;
  } else if (end) {
    return `Ends ${formatDate(end)}`;
  }
  return '';
};

const getStatusClass = (statusVal) => {
  if (!statusVal) return 'status-draft';
  const val = statusVal.toLowerCase();
  if (val.includes('draft')) return 'status-draft';
  if (val.includes('request')) return 'status-requested';
  if (val.includes('post')) return 'status-posted';
  if (val.includes('fill')) return 'status-filled';
  return 'status-other';
};

const triggerDelete = () => {
  // Toggle CSS class to initiate transition animation
  isDeleting.value = true;
  // Wait for animation to finish before emitting the delete action
  setTimeout(() => {
    emit('delete', props.job.id);
  }, 400);
};

const handleImageError = (e) => {
  e.target.style.display = 'none';
};
</script>

<style scoped>
.job-card {
  background: var(--bg-card);
  backdrop-filter: blur(12px);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), 
              box-shadow 0.3s ease, 
              opacity 0.4s ease, 
              max-height 0.4s ease;
  overflow: hidden;
  position: relative;
}

.job-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px -4px rgba(var(--primary-color-rgb), 0.15), 0 4px 12px -2px var(--border-color-glow);
  border-color: rgba(var(--primary-color-rgb), 0.3);
}

.job-card.is-deleting {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}

/* Card Header styles */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.profile-pic-container {
  width: 60px;
  height: 60px;
  border-radius: 14px;
  overflow: hidden;
  background: var(--bg-card-element);
  border: 1px solid var(--border-color);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.profile-pic {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-pic-fallback {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
  background: var(--primary-light);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-buttons {
  display: flex;
  gap: 6px;
}

.action-btn {
  background: var(--bg-card-element);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  color: var(--text-secondary);
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  color: var(--text-main);
  background: var(--border-color);
  transform: translateY(-2px);
}

.edit-btn:hover {
  border-color: rgba(var(--primary-color-rgb), 0.5);
  color: var(--primary-color);
  background: var(--primary-light);
}

.duplicate-btn:hover {
  border-color: rgba(99, 102, 241, 0.5);
  color: rgb(99, 102, 241);
  background: rgba(99, 102, 241, 0.1);
}

.delete-btn:hover {
  border-color: rgba(239, 68, 68, 0.5);
  color: rgb(239, 68, 68);
  background: rgba(239, 68, 68, 0.1);
}

.icon-svg {
  width: 16px;
  height: 16px;
}

/* Card Body styles */
.card-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.job-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-main);
  line-height: 1.3;
}

.category-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.category-tag {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 9999px;
  font-weight: 500;
}

.status-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.status-tag {
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 6px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-transform: capitalize;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  display: inline-block;
}

/* Color schemes for statuses */
.status-draft {
  background: rgba(156, 163, 175, 0.1);
  color: #9ca3af;
  border: 1px solid rgba(156, 163, 175, 0.2);
}
.status-draft .status-dot { background: #9ca3af; }

.status-requested {
  background: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.2);
}
.status-requested .status-dot { background: #f59e0b; }

.status-posted {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}
.status-posted .status-dot { background: #10b981; }

.status-filled {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border: 1px solid rgba(59, 130, 246, 0.2);
}
.status-filled .status-dot { background: #3b82f6; }

.status-other {
  background: rgba(139, 92, 246, 0.1);
  color: #8b5cf6;
  border: 1px solid rgba(139, 92, 246, 0.2);
}
.status-other .status-dot { background: #8b5cf6; }

.job-description {
  margin: 0;
  font-size: 0.875rem;
  color: var(--text-secondary);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-meta {
  border-top: 1px solid var(--border-color);
  padding-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 4px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
  font-size: 0.8rem;
}

.meta-icon {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.meta-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
