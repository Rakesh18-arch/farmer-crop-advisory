import React, { useState, useEffect, useRef } from 'react';
import { chatbotService } from '../services/chatbotService';
import { useLanguage } from '../context/LanguageContext';

const AIChatbot = () => {
  const { currentLang, t } = useLanguage();

  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: 'Namaste Farmer! 🌾 I am your AI Agricultural Expert powered by multi-model Agronomic LLMs.\n\nAsk me anything regarding:\n• Crop selection & soil NPK synergy\n• Plant disease identification & organic/chemical cures\n• Fertilizer dosages (Urea, DAP, MOP per acre)\n• Real-time APMC Mandi price intelligence & forecasts\n• Government welfare schemes (PM-KISAN, PMFBY)',
      provider: 'AgriLLM-Neural-v2.6'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [sending, setSending] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState('agri-neural');
  const [availableProviders, setAvailableProviders] = useState([
    { id: 'agri-neural', name: 'AgriLLM-Neural (Built-in Knowledge Engine)' },
    { id: 'gemini', name: 'Google Gemini 1.5 Flash' },
    { id: 'groq', name: 'Groq LLaMA 3.3 70B' },
    { id: 'openai', name: 'OpenAI GPT-4o Mini' }
  ]);
  const chatBottomRef = useRef(null);

  useEffect(() => {
    // Fetch live available providers from backend
    chatbotService.getModels().then(data => {
      if (data.success && data.providers && data.providers.length > 0) {
        setAvailableProviders(data.providers);
      }
    }).catch(() => {});
  }, []);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const handleSend = async (messageText) => {
    const textToSend = messageText || inputText;
    if (!textToSend.trim() || sending) return;

    // Add user message
    const userMsg = { sender: 'user', text: textToSend };
    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setSending(true);

    try {
      const data = await chatbotService.sendMessage(textToSend, currentLang, selectedProvider);
      if (data.success && data.reply) {
        setMessages(prev => [...prev, {
          sender: 'bot',
          text: data.reply,
          provider: data.model || selectedProvider
        }]);
      } else {
        setMessages(prev => [...prev, {
          sender: 'bot',
          text: 'I encountered an issue processing that query. Please ask again.',
          provider: 'AgriAI System'
        }]);
      }
    } catch {
      setMessages(prev => [...prev, {
        sender: 'bot',
        text: 'Sorry, could not reach the agricultural AI server right now.',
        provider: 'AgriAI Offline'
      }]);
    } finally {
      setSending(false);
    }
  };

  const quickPrompts = [
    'Recommend best crop for black soil with low nitrogen',
    'How to cure tomato leaf curl disease organically?',
    'What is the standard Urea & DAP dosage for Paddy per acre?',
    'Current market price trend for Cotton in APMC Mandis',
    'How to apply for PM-KISAN subsidy scheme?'
  ];

  return (
    <div className="page-body d-flex flex-column" style={{ minHeight: 'calc(100vh - 120px)' }}>
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-sm-center gap-2 mb-3">
        <div>
          <h2 className="brand-font mb-1">
            <i className="bi bi-robot text-success me-2"></i>
            AgriAI LLM Expert Advisory
          </h2>
          <p className="text-muted small mb-0">24/7 Intelligent Agricultural Decision Support & Conversational Assistant</p>
        </div>

        {/* Model Selector */}
        <div className="d-flex align-items-center gap-2">
          <small className="text-muted fw-bold d-none d-md-inline">AI Engine:</small>
          <select
            className="form-select form-select-sm shadow-sm"
            style={{ minWidth: '220px' }}
            value={selectedProvider}
            onChange={(e) => setSelectedProvider(e.target.value)}
          >
            {availableProviders.map(p => (
              <option key={p.id} value={p.id}>
                {p.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Chat Box Container */}
      <div className="agri-card flex-grow-1 d-flex flex-column p-0 overflow-hidden shadow-sm" style={{ minHeight: '520px' }}>
        {/* Header Bar */}
        <div className="p-3 bg-light border-bottom d-flex justify-content-between align-items-center flex-wrap gap-2">
          <div className="d-flex align-items-center gap-2">
            <div className="bg-success text-white rounded-circle d-flex align-items-center justify-content-center fs-5" style={{ width: '38px', height: '38px' }}>
              🌱
            </div>
            <div>
              <span className="fw-bold small d-block">AgriExpert Decision Intelligence</span>
              <small className="text-success" style={{ fontSize: '0.75rem' }}>
                <span className="badge bg-success-subtle text-success border border-success-subtle me-1">Active</span>
                Multi-Model LLM • English / Telugu / Hindi
              </small>
            </div>
          </div>
          <div className="d-flex gap-2">
            <span className="badge badge-pill-soft badge-soft-emerald small align-self-center">
              ICAR + APMC Data Synchronized
            </span>
          </div>
        </div>

        {/* Message Stream */}
        <div className="p-3 flex-grow-1 overflow-auto" style={{ maxHeight: '58vh' }}>
          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`d-flex flex-column mb-3 ${m.sender === 'user' ? 'align-items-end' : 'align-items-start'}`}
            >
              {m.sender === 'bot' && (
                <div className="d-flex align-items-center gap-1 mb-1 ms-1">
                  <span className="badge bg-light text-muted border small" style={{ fontSize: '0.7rem' }}>
                    🤖 {m.provider || 'AgriLLM'}
                  </span>
                </div>
              )}
              <div
                className={`p-3 rounded shadow-sm ${
                  m.sender === 'user'
                    ? 'bg-success text-white'
                    : 'bg-white text-dark border'
                }`}
                style={{
                  maxWidth: '82%',
                  borderRadius: m.sender === 'user' ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                  whiteSpace: 'pre-wrap',
                  fontSize: '0.925rem',
                  lineHeight: '1.55'
                }}
              >
                {m.text}
              </div>
            </div>
          ))}

          {sending && (
            <div className="d-flex justify-content-start mb-3">
              <div className="p-3 bg-light border rounded text-muted small d-flex align-items-center gap-2">
                <span className="spinner-grow spinner-grow-sm text-success"></span>
                <span>Generating agronomic guidance using <strong>{selectedProvider}</strong>...</span>
              </div>
            </div>
          )}
          <div ref={chatBottomRef} />
        </div>

        {/* Quick Suggestion Pills */}
        <div className="p-2 bg-light border-top d-flex gap-2 overflow-auto" style={{ whiteSpace: 'nowrap' }}>
          <small className="text-muted fw-bold align-self-center px-2">Quick Inquiries:</small>
          {quickPrompts.map((q, idx) => (
            <button
              key={idx}
              type="button"
              className="btn btn-outline-secondary btn-sm rounded-pill text-nowrap"
              style={{ fontSize: '0.78rem' }}
              onClick={() => handleSend(q)}
            >
              {q}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="p-3 bg-white border-top">
          <div className="input-group">
            <input
              type="text"
              className="form-control"
              placeholder="Ask anything about crops, soil nutrients, pests, fertilizers, mandi prices..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={sending}
            />
            <button type="submit" className="btn btn-agri px-4" disabled={sending || !inputText.trim()}>
              <i className="bi bi-send-fill me-1"></i> Send Query
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AIChatbot;
