import React, { createContext, useContext, useState, useEffect } from 'react';
import enTranslations from '../locales/en.json';
import teTranslations from '../locales/te.json';
import hiTranslations from '../locales/hi.json';

const translationsMap = {
  en: enTranslations,
  te: teTranslations,
  hi: hiTranslations
};

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [currentLang, setCurrentLang] = useState(() => {
    return localStorage.getItem('farmer_language') || 'en';
  });

  useEffect(() => {
    localStorage.setItem('farmer_language', currentLang);
  }, [currentLang]);

  const changeLanguage = (langCode) => {
    if (translationsMap[langCode]) {
      setCurrentLang(langCode);
    }
  };

  /**
   * Helper function to resolve nested keys like "nav.dashboard"
   */
  const t = (keyPath, fallback = '') => {
    const keys = keyPath.split('.');
    let current = translationsMap[currentLang];

    for (const key of keys) {
      if (current && current[key] !== undefined) {
        current = current[key];
      } else {
        // Fallback to English if translation is missing
        let enCurrent = translationsMap.en;
        for (const enKey of keys) {
          if (enCurrent && enCurrent[enKey] !== undefined) {
            enCurrent = enCurrent[enKey];
          } else {
            return fallback || keyPath;
          }
        }
        return enCurrent;
      }
    }
    return current;
  };

  return (
    <LanguageContext.Provider value={{ currentLang, changeLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};
