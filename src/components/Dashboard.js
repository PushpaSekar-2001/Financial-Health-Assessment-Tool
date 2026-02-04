import React, { useState } from 'react';
import { Bar, Pie, Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Tooltip,
  Legend
);

function Dashboard({ businesses, onBusinessSelect, selectedBusinessId }) {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredBusinesses = businesses.filter(b =>
    b.business_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
    b.industry_type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Calculate statistics
  const stats = {
    total: businesses.length,
    lowRisk: businesses.filter(b => b.financial_health_score >= 80).length,
    mediumRisk: businesses.filter(b => b.financial_health_score >= 60 && b.financial_health_score < 80).length,
    highRisk: businesses.filter(b => b.financial_health_score < 60).length,
    avgScore: (businesses.reduce((sum, b) => sum + (b.financial_health_score || 0), 0) / businesses.length).toFixed(2),
    totalRevenue: businesses.reduce((sum, b) => sum + (b.annual_revenue || 0), 0)
  };

  const industryData = {};
  businesses.forEach(b => {
    industryData[b.industry_type] = (industryData[b.industry_type] || 0) + 1;
  });

  const riskChartData = {
    labels: ['Low Risk', 'Medium Risk', 'High Risk'],
    datasets: [{
      label: 'Number of Businesses',
      data: [stats.lowRisk, stats.mediumRisk, stats.highRisk],
      backgroundColor: ['#28A745', '#FFC107', '#DC3545'],
      borderColor: ['#28A745', '#FFC107', '#DC3545'],
      borderWidth: 1
    }]
  };

  const industryChartData = {
    labels: Object.keys(industryData),
    datasets: [{
      label: 'Businesses by Industry',
      data: Object.values(industryData),
      backgroundColor: [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A',
        '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E2'
      ]
    }]
  };

  return (
    <div className="dashboard-container p-4">
      <h1 className="mb-4">📊 Financial Health Dashboard</h1>

      {/* Statistics Cards */}
      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card stat-card bg-primary text-white">
            <div className="card-body">
              <h5 className="card-title">Total Businesses</h5>
              <p className="card-text display-4">{stats.total}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card stat-card bg-success text-white">
            <div className="card-body">
              <h5 className="card-title">Low Risk</h5>
              <p className="card-text display-4">{stats.lowRisk}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card stat-card bg-warning text-white">
            <div className="card-body">
              <h5 className="card-title">Medium Risk</h5>
              <p className="card-text display-4">{stats.mediumRisk}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card stat-card bg-danger text-white">
            <div className="card-body">
              <h5 className="card-title">High Risk</h5>
              <p className="card-text display-4">{stats.highRisk}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="row mb-4">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Risk Distribution</h5>
              <Pie data={riskChartData} />
            </div>
          </div>
        </div>
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Industries Represented</h5>
              <Bar data={industryChartData} />
            </div>
          </div>
        </div>
      </div>

      {/* Search and Business List */}
      <div className="row">
        <div className="col-md-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Businesses</h5>
              <input
                type="text"
                className="form-control mb-3"
                placeholder="Search by Business ID or Industry..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />

              <div className="table-responsive">
                <table className="table table-hover">
                  <thead className="table-light">
                    <tr>
                      <th>Business ID</th>
                      <th>Industry</th>
                      <th>Health Score</th>
                      <th>Risk Category</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredBusinesses.map((business, idx) => (
                      <tr key={idx} className={selectedBusinessId === business.business_id ? 'table-active' : ''}>
                        <td><strong>{business.business_id}</strong></td>
                        <td>{business.industry_type}</td>
                        <td>
                          <span className="badge bg-info">{business.financial_health_score}</span>
                        </td>
                        <td>
                          <span className={`badge bg-${
                            business.financial_health_score >= 80 ? 'success' :
                            business.financial_health_score >= 60 ? 'warning' : 'danger'
                          }`}>
                            {business.financial_health_score >= 80 ? 'Low Risk' :
                             business.financial_health_score >= 60 ? 'Medium Risk' : 'High Risk'}
                          </span>
                        </td>
                        <td>
                          <button
                            className="btn btn-sm btn-primary"
                            onClick={() => onBusinessSelect(business.business_id)}
                          >
                            Analyze
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
