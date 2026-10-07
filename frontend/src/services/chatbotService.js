import api from './api';

export const chatbotService = {
  // Send query to multilingual agricultural AI chatbot
  sendMessage: async (message, language = 'en', provider = null) => {
    const res = await api.post('/chatbot/message', { message, language, provider });
    return res.data;
  },

  // Get available LLM models
  getModels: async () => {
    const res = await api.get('/chatbot/models');
    return res.data;
  },

  // Ask direct query to LLM engine
  askLLM: async (prompt, provider = null, context = {}) => {
    const res = await api.post('/chatbot/ask-llm', { prompt, provider, context });
    return res.data;
  },

  // Get conversation history
  getHistory: async (sessionId = null) => {
    const params = sessionId ? { session_id: sessionId } : {};
    const res = await api.get('/chatbot/history', { params });
    return res.data;
  }
};
