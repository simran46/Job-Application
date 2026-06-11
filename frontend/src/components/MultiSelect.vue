<template>
  <div class="multiselect-container" ref="containerRef">
    <label v-if="label" class="multiselect-label">{{ label }}</label>
    
    <div 
      class="multiselect-select-box" 
      :class="{ 'is-open': isOpen, 'has-error': hasError }"
      @click="toggleDropdown"
    >
      <!-- Selected tags list -->
      <div class="multiselect-tags-container">
        <span v-if="modelValue.length === 0" class="multiselect-placeholder">
          {{ placeholder }}
        </span>
        <div 
          v-for="item in modelValue" 
          :key="item" 
          class="multiselect-tag"
          @click.stop
        >
          <span>{{ item }}</span>
          <button 
            type="button" 
            class="multiselect-remove-btn" 
            @click.stop="removeItem(item)"
          >
            &times;
          </button>
        </div>
      </div>
      
      <!-- Dropdown arrow -->
      <div class="multiselect-arrow">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </div>
    </div>
    
    <!-- Dropdown List -->
    <transition name="fade-slide">
      <div v-if="isOpen" class="multiselect-dropdown">
        <!-- Search bar inside dropdown -->
        <div class="multiselect-search-container" @click.stop>
          <input 
            type="text" 
            class="multiselect-search-input" 
            placeholder="Search options..."
            v-model="searchQuery"
            ref="searchInputRef"
          />
        </div>
        
        <!-- Options List -->
        <ul class="multiselect-options-list">
          <li 
            v-for="option in filteredOptions" 
            :key="option"
            class="multiselect-option"
            :class="{ 'is-selected': isSelected(option) }"
            @click.stop="toggleItem(option)"
          >
            <div class="multiselect-checkbox" :class="{ 'checked': isSelected(option) }">
              <svg v-if="isSelected(option)" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
            </div>
            <span class="multiselect-option-text">{{ option }}</span>
          </li>
          <li v-if="filteredOptions.length === 0" class="multiselect-no-options">
            No options found
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  options: {
    type: Array,
    required: true
  },
  placeholder: {
    type: String,
    default: 'Select options'
  },
  label: {
    type: String,
    default: ''
  },
  hasError: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);
const searchQuery = ref('');
const containerRef = ref(null);
const searchInputRef = ref(null);

const filteredOptions = computed(() => {
  if (!searchQuery.value) return props.options;
  return props.options.filter(option => 
    option.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const isSelected = (option) => {
  return props.modelValue.includes(option);
};

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    // Focus search input after modal renders
    setTimeout(() => {
      searchInputRef.value?.focus();
    }, 50);
  }
};

const toggleItem = (option) => {
  const newValue = [...props.modelValue];
  const index = newValue.indexOf(option);
  if (index === -1) {
    newValue.push(option);
  } else {
    newValue.splice(index, 1);
  }
  emit('update:modelValue', newValue);
};

const removeItem = (option) => {
  const newValue = props.modelValue.filter(item => item !== option);
  emit('update:modelValue', newValue);
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.multiselect-container {
  position: relative;
  width: 100%;
  text-align: left;
  font-family: inherit;
}

.multiselect-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.multiselect-select-box {
  min-height: 48px;
  padding: 6px 12px;
  background: var(--bg-card-element);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.multiselect-select-box:hover {
  border-color: var(--primary-color-hover);
}

.multiselect-select-box.is-open {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(var(--primary-color-rgb), 0.15);
}

.multiselect-select-box.has-error {
  border-color: var(--error-color);
}

.multiselect-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  flex-grow: 1;
}

.multiselect-placeholder {
  color: var(--text-muted);
  font-size: 0.95rem;
  user-select: none;
}

.multiselect-tag {
  background: var(--primary-light);
  color: var(--primary-color);
  border: 1px solid rgba(var(--primary-color-rgb), 0.2);
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: background 0.2s, color 0.2s;
}

.multiselect-tag:hover {
  background: rgba(var(--primary-color-rgb), 0.15);
}

.multiselect-remove-btn {
  background: none;
  border: none;
  color: var(--primary-color);
  font-size: 1.1rem;
  line-height: 1;
  padding: 0;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.multiselect-remove-btn:hover {
  opacity: 1;
}

.multiselect-arrow {
  color: var(--text-secondary);
  transition: transform 0.25s;
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

.multiselect-select-box.is-open .multiselect-arrow {
  transform: rotate(180deg);
}

.multiselect-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  width: 100%;
  background: var(--bg-dropdown);
  backdrop-filter: blur(16px);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
  z-index: 100;
  overflow: hidden;
  max-height: 300px;
  display: flex;
  flex-direction: column;
}

.multiselect-search-container {
  padding: 10px;
  border-bottom: 1px solid var(--border-color);
  background: rgba(255, 255, 255, 0.02);
}

.multiselect-search-input {
  width: 100%;
  height: 36px;
  padding: 8px 12px;
  background: var(--bg-card-element);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-main);
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s;
}

.multiselect-search-input:focus {
  border-color: var(--primary-color);
}

.multiselect-options-list {
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-y: auto;
  max-height: 200px;
}

.multiselect-option {
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
}

.multiselect-option:hover {
  background: rgba(255, 255, 255, 0.05);
}

.multiselect-option.is-selected {
  background: rgba(var(--primary-color-rgb), 0.08);
}

.multiselect-checkbox {
  width: 18px;
  height: 18px;
  border: 2px solid var(--border-color-checkbox);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, border-color 0.2s;
  flex-shrink: 0;
}

.multiselect-checkbox.checked {
  background: var(--primary-color);
  border-color: var(--primary-color);
  color: #ffffff;
}

.multiselect-checkbox.checked svg {
  width: 12px;
  height: 12px;
}

.multiselect-option-text {
  font-size: 0.9rem;
  color: var(--text-main);
}

.multiselect-no-options {
  padding: 16px;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.875rem;
}

/* Transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
