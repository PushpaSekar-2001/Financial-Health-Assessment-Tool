import React from 'react';

function Navigation({ language, onLanguageChange, activeTab, onTabChange }) {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-primary sticky-top">
      <div className="container-fluid">
        <a className="navbar-brand fw-bold" href="#home">
          💰 Financial Health Assessment Tool
        </a>
        
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === 'dashboard' ? 'active' : ''}`}
                onClick={() => onTabChange('dashboard')}
              >
                📊 Dashboard
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === 'analysis' ? 'active' : ''}`}
                onClick={() => onTabChange('analysis')}
              >
                📈 Analysis
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === 'recommendations' ? 'active' : ''}`}
                onClick={() => onTabChange('recommendations')}
              >
                💡 Recommendations
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === 'upload' ? 'active' : ''}`}
                onClick={() => onTabChange('upload')}
              >
                📁 Upload
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${activeTab === 'reports' ? 'active' : ''}`}
                onClick={() => onTabChange('reports')}
              >
                📄 Reports
              </button>
            </li>
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                href="#language"
                id="languageDropdown"
                role="button"
                data-bs-toggle="dropdown"
              >
                🌐 {language === 'en' ? 'English' : 'हिन्दी'}
              </a>
              <ul className="dropdown-menu" aria-labelledby="languageDropdown">
                <li>
                  <button
                    className={`dropdown-item ${language === 'en' ? 'active' : ''}`}
                    onClick={() => onLanguageChange('en')}
                  >
                    English
                  </button>
                </li>
                <li>
                  <button
                    className={`dropdown-item ${language === 'hi' ? 'active' : ''}`}
                    onClick={() => onLanguageChange('hi')}
                  >
                    हिन्दी
                  </button>
                </li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navigation;
