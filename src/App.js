import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import AnalysisPanel from './components/AnalysisPanel';
import RecommendationsPanel from './components/RecommendationsPanel';
import FileUpload from './components/FileUpload';
import ReportGenerator from './components/ReportGenerator';
import Navigation from './components/Navigation';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [businessId, setBusinessId] = useState('SME_1');
  const [analysisData, setAnalysisData] = useState(null);
  const [recommendationsData, setRecommendationsData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [language, setLanguage] = useState('en');
  const [allBusinesses, setAllBusinesses] = useState([]);

  const API_BASE = 'http://127.0.0.1:5000/api';

  // Fetch all businesses on mount
  useEffect(() => {
    fetchAllBusinesses();
    // Auto-fetch analysis for default business
    fetchAnalysis('SME_1');
  }, []);

  const fetchAllBusinesses = async () => {
    try {
      const res = await fetch(`${API_BASE}/businesses`);
      const data = await res.json();
      if (data.status === 'success') {
        setAllBusinesses(data.data);
      }
    } catch (err) {
      console.error('Error fetching businesses:', err);
    }
  };

  const fetchAnalysis = async (bid = businessId) => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API_BASE}/analysis/${bid}?language=${language}`);
      const data = await res.json();
      
      console.log('Analysis response:', data); // Debug log
      
      if (data.status === 'success') {
        setAnalysisData(data.data.analysis);
        setRecommendationsData(data.data.recommendations);
        setActiveTab('analysis');
      } else {
        setError(data.message || 'Failed to fetch analysis');
      }
    } catch (err) {
      console.error('Fetch error:', err); // Debug log
      setError(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleBusinessSelect = (bid) => {
    setBusinessId(bid);
    fetchAnalysis(bid);
  };

  const handleFileUpload = (uploadedData) => {
    if (uploadedData && uploadedData.length > 0) {
      // Analyze first business in uploaded data
      setAnalysisData(uploadedData[0].analysis);
      setRecommendationsData(uploadedData[0].recommendations);
      setBusinessId(uploadedData[0].business_id);
      setActiveTab('analysis');
    }
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    if (analysisData) {
      fetchAnalysis();
    }
  };

  return (
    <div className="App">
      <Navigation 
        language={language}
        onLanguageChange={handleLanguageChange}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
      
      <div className="container-fluid main-content">
        {error && (
          <div className="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Error:</strong> {error}
            <button type="button" className="btn-close" onClick={() => setError('')}></button>
          </div>
        )}

        {loading && (
          <div className="loading-spinner">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p>Analyzing financial data...</p>
          </div>
        )}

        {!loading && (
          <>
            {activeTab === 'dashboard' && (
              <Dashboard 
                businesses={allBusinesses}
                onBusinessSelect={handleBusinessSelect}
                selectedBusinessId={businessId}
              />
            )}

            {activeTab === 'analysis' && analysisData && (
              <AnalysisPanel analysis={analysisData} language={language} />
            )}

            {activeTab === 'recommendations' && recommendationsData && (
              <RecommendationsPanel recommendations={recommendationsData} language={language} />
            )}

            {activeTab === 'upload' && (
              <FileUpload onUploadSuccess={handleFileUpload} apiBase={API_BASE} />
            )}

            {activeTab === 'reports' && analysisData && (
              <ReportGenerator businessId={businessId} apiBase={API_BASE} />
            )}
          </>
        )}
      </div>

      <footer className="footer">
        <p>&copy; 2024 Financial Health Assessment Tool. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;
