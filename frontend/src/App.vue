<template>
  <div class="app-container">
    <!-- Header Section -->
    <header class="dashboard-header">
      <div class="header-left">
        <h1 class="app-title">CareerPulse</h1>
        <p class="app-subtitle">Premium Job Listing & Talent Analytics Portal</p>
      </div>
      
      <!-- Quick Stats -->
      <div class="header-stats" v-if="jobs.length > 0">
        <div class="stat-box">
          <span class="stat-number">{{ jobs.length }}</span>
          <span class="stat-label">Total Jobs</span>
        </div>
        <div class="stat-box">
          <span class="stat-number">{{ postedCount }}</span>
          <span class="stat-label">Posted</span>
        </div>
        <div class="stat-box">
          <span class="stat-number">{{ filledCount }}</span>
          <span class="stat-label">Filled</span>
        </div>
      </div>

      <div class="header-actions">
        <button class="btn btn-secondary" @click="openAnalytics">
          <!-- Analytics Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"></line>
            <line x1="12" y1="20" x2="12" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="14"></line>
          </svg>
          Analytics
        </button>
        <button class="btn btn-primary" @click="openCreateForm">
          <!-- Plus Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          Post a Job
        </button>
      </div>
    </header>

    <!-- Error Alerts -->
    <div v-if="errorMessage" class="error-alert">
      <span>{{ errorMessage }}</span>
      <button class="alert-close" @click="errorMessage = ''">&times;</button>
    </div>

    <!-- Main Grid Content -->
    <main class="dashboard-main">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading job postings...</p>
      </div>

      <div v-else-if="jobs.length === 0" class="empty-state">
        <div class="empty-illustration">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
          </svg>
        </div>
        <h2>No Jobs Posted Yet</h2>
        <p>Get started by creating your first job listing. It will display here as a premium card and feed into your real-time analytics.</p>
        <button class="btn btn-primary" @click="openCreateForm">
          Post Your First Job
        </button>
      </div>

      <!-- Job Cards Grid (Animated layout) -->
      <transition-group 
        v-else 
        name="card-list" 
        tag="div" 
        class="jobs-grid"
      >
        <job-card
          v-for="job in jobs"
          :key="job.id"
          :job="job"
          :backend-url="backendBaseUrl"
          @edit="openEditForm"
          @delete="handleDelete"
          @duplicate="handleDuplicate"
        />
      </transition-group>
    </main>

    <!-- Dialog Box: Job Form (Create / Edit) -->
    <transition name="modal-fade">
      <div v-if="isFormOpen" class="modal-overlay" @click.self="closeForm">
        <div class="modal-container">
          <div class="modal-header">
            <h2 class="modal-title">{{ isEditMode ? 'Edit Job Posting' : 'Post a New Job' }}</h2>
            <button class="close-btn" @click="closeForm">&times;</button>
          </div>

          <form @submit.prevent="submitForm" class="job-form">
            <!-- 2-Column Grid -->
            <div class="form-grid">
              <!-- Job Title -->
              <div class="form-group col-span-2">
                <label class="form-label" for="job-title">Job Title *</label>
                <input 
                  type="text" 
                  id="job-title" 
                  class="form-input" 
                  v-model="form.title" 
                  placeholder="e.g. Senior Frontend Engineer"
                  :class="{ 'has-error': errors.title }"
                />
                <span v-if="errors.title" class="error-text">{{ errors.title }}</span>
              </div>

              <!-- Status Multiselect -->
              <div class="form-group">
                <multi-select
                  v-model="form.status"
                  :options="statusOptions"
                  placeholder="Select statuses..."
                  label="Status (Multiselect) *"
                  :has-error="!!errors.status"
                />
                <span v-if="errors.status" class="error-text">{{ errors.status }}</span>
              </div>

              <!-- Job Category Multiselect -->
              <div class="form-group">
                <multi-select
                  v-model="form.category"
                  :options="categoryOptions"
                  placeholder="Select categories..."
                  label="Job Category (Multiselect) *"
                  :has-error="!!errors.category"
                />
                <span v-if="errors.category" class="error-text">{{ errors.category }}</span>
              </div>

              <!-- Address -->
              <div class="form-group col-span-2">
                <label class="form-label" for="job-address">Address</label>
                <input 
                  type="text" 
                  id="job-address" 
                  class="form-input" 
                  v-model="form.address" 
                  placeholder="e.g. 100 Innovation Way"
                />
              </div>

              <!-- City -->
              <div class="form-group">
                <label class="form-label" for="job-city">City</label>
                <input 
                  type="text" 
                  id="job-city" 
                  class="form-input" 
                  v-model="form.city" 
                  placeholder="e.g. San Francisco"
                />
              </div>

              <!-- State -->
              <div class="form-group">
                <label class="form-label" for="job-state">State</label>
                <input 
                  type="text" 
                  id="job-state" 
                  class="form-input" 
                  v-model="form.state" 
                  placeholder="e.g. California"
                />
              </div>

              <!-- Start Date -->
              <div class="form-group">
                <label class="form-label" for="job-start-date">Start Date</label>
                <input 
                  type="date" 
                  id="job-start-date" 
                  class="form-input" 
                  v-model="form.start_date"
                />
              </div>

              <!-- End Date -->
              <div class="form-group">
                <label class="form-label" for="job-end-date">End Date</label>
                <input 
                  type="date" 
                  id="job-end-date" 
                  class="form-input" 
                  v-model="form.end_date"
                  :class="{ 'has-error': errors.date }"
                />
                <span v-if="errors.date" class="error-text">{{ errors.date }}</span>
              </div>

              <!-- Description -->
              <div class="form-group col-span-2">
                <label class="form-label" for="job-desc">Description</label>
                <textarea 
                  id="job-desc" 
                  class="form-textarea" 
                  v-model="form.description" 
                  placeholder="Describe roles, responsibilities, requirements..."
                  rows="4"
                ></textarea>
              </div>

              <!-- Job Profile Picture Upload (Drag and Drop / Browse) -->
              <div class="form-group col-span-2">
                <label class="form-label">Job Profile Picture</label>
                
                <div 
                  class="upload-dropzone"
                  :class="{ 'is-dragging': isDragging, 'has-file': form.profile_picture }"
                  @dragover.prevent="onDragOver"
                  @dragleave="onDragLeave"
                  @drop.prevent="onDrop"
                  @click="triggerFileSelect"
                >
                  <input 
                    type="file" 
                    ref="fileInput" 
                    style="display: none" 
                    accept="image/*"
                    @change="onFileSelected"
                  />
                  
                  <div class="dropzone-content" v-if="!form.profile_picture">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="upload-icon">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                      <polyline points="17 8 12 3 7 8"></polyline>
                      <line x1="12" y1="3" x2="12" y2="15"></line>
                    </svg>
                    <p class="dropzone-text">Drag and drop profile picture here, or <span>browse</span></p>
                    <span class="dropzone-subtext">Supports PNG, JPG, GIF up to 5MB</span>
                  </div>

                  <!-- Image Preview Panel -->
                  <div class="preview-panel" v-else @click.stop>
                    <img :src="imagePreviewUrl" alt="Profile Picture Preview" class="upload-preview" />
                    <div class="preview-info">
                      <span class="preview-name">{{ getFileName(form.profile_picture) }}</span>
                      <button type="button" class="btn btn-danger btn-sm" @click="clearProfilePicture">Remove Image</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer Buttons -->
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeForm">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="submitting">
                <span v-if="submitting" class="spinner btn-spinner"></span>
                {{ isEditMode ? 'Save Changes' : 'Post Job' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>

    <!-- Dialog Box: Analytics Dashboard -->
    <analytics-dashboard
      v-if="isAnalyticsOpen"
      :jobs="jobs"
      @close="isAnalyticsOpen = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import axios from 'axios';
import JobCard from './components/JobCard.vue';
import MultiSelect from './components/MultiSelect.vue';
import AnalyticsDashboard from './components/AnalyticsDashboard.vue';

// Constants
const backendBaseUrl = 'http://localhost:8000';
const apiEndpoint = `${backendBaseUrl}/api/jobs/`;

const statusOptions = ['Draft', 'Requested', 'Posted', 'Filled'];
const categoryOptions = ['Full-time', 'Part-time', 'Intern', 'Contract', 'Remote'];

// Reactive state
const jobs = ref([]);
const loading = ref(true);
const submitting = ref(false);
const isFormOpen = ref(false);
const isAnalyticsOpen = ref(false);
const isEditMode = ref(false);
const currentJobId = ref(null);
const errorMessage = ref('');

const isDragging = ref(false);
const fileInput = ref(null);
const localPreviewUrl = ref(null);

const form = reactive({
  title: '',
  status: [],
  category: [],
  address: '',
  city: '',
  state: '',
  start_date: '',
  end_date: '',
  description: '',
  profile_picture: null
});

const errors = reactive({
  title: '',
  status: '',
  category: '',
  date: ''
});

// Computed properties for dashboard stats
const postedCount = computed(() => {
  return jobs.value.filter(job => 
    Array.isArray(job.status) && job.status.some(s => s.toLowerCase().includes('post'))
  ).length;
});

const filledCount = computed(() => {
  return jobs.value.filter(job => 
    Array.isArray(job.status) && job.status.some(s => s.toLowerCase().includes('fill'))
  ).length;
});

// Computed preview URL for uploaded profile picture
const imagePreviewUrl = computed(() => {
  if (localPreviewUrl.value) return localPreviewUrl.value;
  if (typeof form.profile_picture === 'string') {
    if (form.profile_picture.startsWith('http')) return form.profile_picture;
    return `${backendBaseUrl}${form.profile_picture.startsWith('/') ? '' : '/'}${form.profile_picture}`;
  }
  return '';
});

// Fetch all jobs
const fetchJobs = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    const response = await axios.get(apiEndpoint);
    // Ensure lists are sorted by backend logic (order ascending, then id ascending)
    jobs.value = response.data;
  } catch (error) {
    console.error('Error fetching jobs:', error);
    errorMessage.value = 'Failed to load jobs from backend server. Please make sure the Django server is running.';
  } finally {
    loading.value = false;
  }
};

// Form dialog control
const openCreateForm = () => {
  isEditMode.value = false;
  currentJobId.value = null;
  resetForm();
  isFormOpen.value = true;
};

const openEditForm = (job) => {
  isEditMode.value = true;
  currentJobId.value = job.id;
  resetForm();
  
  // Fill form fields
  form.title = job.title;
  form.status = Array.isArray(job.status) ? [...job.status] : [];
  form.category = Array.isArray(job.category) ? [...job.category] : [];
  form.address = job.address || '';
  form.city = job.city || '';
  form.state = job.state || '';
  form.start_date = job.start_date || '';
  form.end_date = job.end_date || '';
  form.description = job.description || '';
  form.profile_picture = job.profile_picture || null;
  
  isFormOpen.value = true;
};

const closeForm = () => {
  isFormOpen.value = false;
  resetForm();
};

const openAnalytics = () => {
  isAnalyticsOpen.value = true;
};

const resetForm = () => {
  form.title = '';
  form.status = [];
  form.category = [];
  form.address = '';
  form.city = '';
  form.state = '';
  form.start_date = '';
  form.end_date = '';
  form.description = '';
  form.profile_picture = null;
  
  localPreviewUrl.value = null;
  
  errors.title = '';
  errors.status = '';
  errors.category = '';
  errors.date = '';
};

// Image Upload Actions
const triggerFileSelect = () => {
  fileInput.value?.click();
};

const processFile = (file) => {
  if (!file) return;
  if (!file.type.startsWith('image/')) {
    alert('Please upload an image file.');
    return;
  }
  form.profile_picture = file;
  localPreviewUrl.value = URL.createObjectURL(file);
};

const onFileSelected = (event) => {
  const file = event.target.files?.[0];
  processFile(file);
};

const onDragOver = () => {
  isDragging.value = true;
};

const onDragLeave = () => {
  isDragging.value = false;
};

const onDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files?.[0];
  processFile(file);
};

const clearProfilePicture = () => {
  form.profile_picture = '';
  localPreviewUrl.value = null;
  if (fileInput.value) fileInput.value.value = '';
};

const getFileName = (val) => {
  if (val instanceof File) return val.name;
  if (typeof val === 'string') {
    return val.substring(val.lastIndexOf('/') + 1);
  }
  return 'Profile Picture';
};

// Form validation
const validate = () => {
  let isValid = true;
  errors.title = '';
  errors.status = '';
  errors.category = '';
  errors.date = '';

  if (!form.title.trim()) {
    errors.title = 'Job title is required.';
    isValid = false;
  }
  if (form.status.length === 0) {
    errors.status = 'Select at least one status.';
    isValid = false;
  }
  if (form.category.length === 0) {
    errors.category = 'Select at least one job category.';
    isValid = false;
  }
  if (form.start_date && form.end_date) {
    if (new Date(form.start_date) > new Date(form.end_date)) {
      errors.date = 'End date cannot be earlier than start date.';
      isValid = false;
    }
  }
  return isValid;
};

// Submit form (create or edit)
const submitForm = async () => {
  if (!validate()) return;
  
  submitting.value = true;
  errorMessage.value = '';
  
  try {
    const formData = new FormData();
    formData.append('title', form.title.trim());
    formData.append('address', form.address.trim());
    formData.append('city', form.city.trim());
    formData.append('state', form.state.trim());
    formData.append('start_date', form.start_date);
    formData.append('end_date', form.end_date);
    formData.append('description', form.description.trim());
    
    // Send list data as JSON array strings. Handled robustly by our backend custom parser.
    formData.append('status', JSON.stringify(form.status));
    formData.append('category', JSON.stringify(form.category));
    
    // Only upload file if it's a new File object
    if (form.profile_picture instanceof File) {
      formData.append('profile_picture', form.profile_picture);
    } else if (form.profile_picture === '') {
      // If user cleared the picture
      formData.append('profile_picture', '');
    }

    if (isEditMode.value) {
      const response = await axios.patch(`${apiEndpoint}${currentJobId.value}/`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      // Find and replace updated item
      const idx = jobs.value.findIndex(j => j.id === currentJobId.value);
      if (idx !== -1) {
        jobs.value[idx] = response.data;
      }
    } else {
      const response = await axios.post(apiEndpoint, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      // Append new job to listing
      jobs.value.push(response.data);
    }
    
    closeForm();
  } catch (error) {
    console.error('Error submitting form:', error);
    errorMessage.value = 'Failed to save job posting. Please try again.';
  } finally {
    submitting.value = false;
  }
};

// Delete job handler
const handleDelete = async (id) => {
  try {
    await axios.delete(`${apiEndpoint}${id}/`);
    // Filter out deleted item from UI list
    jobs.value = jobs.value.filter(job => job.id !== id);
  } catch (error) {
    console.error('Error deleting job:', error);
    errorMessage.value = 'Failed to delete the job posting.';
  }
};

// Duplicate job handler
const handleDuplicate = async (id) => {
  try {
    const response = await axios.post(`${apiEndpoint}${id}/duplicate/`);
    const duplicatedJob = response.data;
    
    // Find index of duplicated parent card to place the clone exactly below
    const parentIndex = jobs.value.findIndex(j => j.id === id);
    if (parentIndex !== -1) {
      // Insert duplicate just below parent card
      jobs.value.splice(parentIndex + 1, 0, duplicatedJob);
    } else {
      jobs.value.push(duplicatedJob);
    }
    
    // Fetch all jobs to ensure correct ordering list state
    await fetchJobs();
  } catch (error) {
    console.error('Error duplicating job:', error);
    errorMessage.value = 'Failed to duplicate the job posting.';
  }
};

// Fetch jobs on mounted
onMounted(fetchJobs);
</script>

<style scoped>
/* Dashboard Header Styles */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  background: var(--bg-card);
  backdrop-filter: blur(16px);
  border: 1px solid var(--border-color);
  padding: 24px;
  border-radius: 20px;
  margin-bottom: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.header-left {
  flex-grow: 1;
  text-align: left;
}

.app-title {
  font-size: 2.2rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  background: linear-gradient(135deg, #ffffff 0%, var(--primary-color) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.app-subtitle {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin-top: 4px;
}

.header-stats {
  display: flex;
  gap: 24px;
  padding: 0 24px;
  border-right: 1px solid var(--border-color);
  border-left: 1px solid var(--border-color);
}

.stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 2px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.header-actions {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

/* Alert styles */
.error-alert {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #f87171;
  padding: 14px 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.9rem;
  text-align: left;
  animation: slide-in 0.25s ease-out;
}

.alert-close {
  background: none;
  border: none;
  color: #f87171;
  font-size: 1.4rem;
  cursor: pointer;
  line-height: 1;
}

@keyframes slide-in {
  from { transform: translateY(-10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Main Layout Grid */
.dashboard-main {
  min-height: 400px;
  display: flex;
  flex-direction: column;
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  width: 100%;
}

/* Loading state */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
  gap: 16px;
  color: var(--text-secondary);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border-width: 2px;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Empty State */
.empty-state {
  background: var(--bg-card);
  border: 1px dashed var(--border-color);
  border-radius: 24px;
  padding: 60px 40px;
  max-width: 600px;
  margin: 40px auto;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.empty-illustration {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: var(--primary-light);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.empty-illustration svg {
  width: 40px;
  height: 40px;
}

.empty-state h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
}

.empty-state p {
  font-size: 0.95rem;
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 460px;
}

/* Modal Form Styles */
.modal-overlay {
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

.modal-container {
  background: var(--bg-modal);
  border: 1px solid var(--border-color);
  border-radius: 24px;
  width: 100%;
  max-width: 650px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  padding: 24px;
  animation: modal-enter 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modal-enter {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 16px;
  margin-bottom: 20px;
}

.modal-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
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

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  text-align: left;
}

.col-span-2 {
  grid-column: span 2;
}

/* Custom Upload Dropzone */
.upload-dropzone {
  border: 2px dashed var(--border-color);
  border-radius: 16px;
  background: var(--bg-card-element);
  min-height: 120px;
  cursor: pointer;
  transition: border-color 0.25s, background-color 0.25s;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-dropzone:hover {
  border-color: var(--primary-color);
  background: rgba(var(--primary-color-rgb), 0.02);
}

.upload-dropzone.is-dragging {
  border-color: var(--primary-color);
  background: rgba(var(--primary-color-rgb), 0.08);
}

.upload-dropzone.has-file {
  border-style: solid;
  background: rgba(255, 255, 255, 0.01);
}

.dropzone-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  text-align: center;
  gap: 6px;
}

.upload-icon {
  color: var(--text-muted);
}

.dropzone-text {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.dropzone-text span {
  color: var(--primary-color);
  text-decoration: underline;
}

.dropzone-subtext {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.preview-panel {
  display: flex;
  align-items: center;
  padding: 16px;
  width: 100%;
  gap: 16px;
}

.upload-preview {
  width: 70px;
  height: 70px;
  border-radius: 12px;
  object-fit: cover;
  border: 1px solid var(--border-color);
  background: var(--bg-app);
}

.preview-info {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  flex-grow: 1;
}

.preview-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 300px;
}

.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
  border-radius: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1px solid var(--border-color);
  padding-top: 18px;
  margin-top: 24px;
}

.has-error {
  border-color: var(--error-color) !important;
}

/* Form inputs */
input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1) brightness(0.9);
  cursor: pointer;
}

/* Modal and transition animations */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.25s;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}

/* Transition-Group Card Move Animations */
.card-list-move {
  transition: transform 0.4s ease;
}

.card-list-enter-active {
  transition: opacity 0.4s ease, transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.card-list-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
  position: absolute; /* needed for move transition of remaining cards to kick in immediately */
  width: calc(100% / 3 - 16px); /* adjust based on parent grids */
}

/* Responsive fixes for leave-active grid sizing */
@media (max-width: 1100px) {
  .card-list-leave-active {
    width: calc(50% - 12px);
  }
}
@media (max-width: 750px) {
  .card-list-leave-active {
    width: 100%;
  }
}

.card-list-enter-from {
  opacity: 0;
  transform: scale(0.9) translateY(30px);
}

.card-list-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}

/* Responsive adjustments */
@media (max-width: 900px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
  }
  .header-stats {
    padding: 16px 0;
    border-left: none;
    border-right: none;
    border-top: 1px solid var(--border-color);
    border-bottom: 1px solid var(--border-color);
    width: 100%;
    justify-content: space-around;
  }
  .header-actions {
    width: 100%;
    justify-content: flex-end;
  }
}

@media (max-width: 600px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
  .col-span-2 {
    grid-column: span 1;
  }
}
</style>
