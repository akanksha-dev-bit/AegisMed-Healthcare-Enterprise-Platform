import axios from 'axios';

export const API_BASE = 'http://localhost:8000';

const client = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const api = {
  getHealth: async () => {
    try {
      const res = await client.get('/health', { timeout: 3000 });
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.message };
    }
  },

  // Document Intelligence
  uploadDocument: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await client.post('/api/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      });
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.response?.data?.detail || err.message };
    }
  },

  extractText: async (text) => {
    try {
      const res = await client.post('/api/documents/extract-text', { text }, { timeout: 60000 });
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.response?.data?.detail || err.message };
    }
  },

  // Policy RAG
  getPolicyDocuments: async () => {
    try {
      const res = await client.get('/api/policies/documents');
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.message };
    }
  },

  searchPolicies: async (query, topK = 5, sourceFilter = null) => {
    try {
      const res = await client.post('/api/policies/search', {
        query,
        top_k: topK,
        source_filter: sourceFilter,
      });
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.response?.data?.detail || err.message };
    }
  },

  // Appointments
  chatAppointment: async (message) => {
    try {
      const res = await client.post('/api/appointments/chat', { message });
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.response?.data?.detail || err.message };
    }
  },

  getDoctors: async () => {
    try {
      const res = await client.get('/api/appointments/doctors');
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.message };
    }
  },

  getBookings: async () => {
    try {
      const res = await client.get('/api/appointments/bookings');
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.message };
    }
  },

  getSlots: async (params) => {
    try {
      const res = await client.get('/api/appointments/slots', { params });
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.message };
    }
  },

  // Evaluation
  runDemoEval: async () => {
    try {
      const res = await client.get('/api/evaluation/demo', { timeout: 90000 });
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.response?.data?.detail || err.message };
    }
  },

  runSingleEval: async (payload) => {
    try {
      const res = await client.post('/api/evaluation/single', payload, { timeout: 60000 });
      return { data: res.data, error: null };
    } catch (err) {
      return { data: null, error: err.response?.data?.detail || err.message };
    }
  },
};
