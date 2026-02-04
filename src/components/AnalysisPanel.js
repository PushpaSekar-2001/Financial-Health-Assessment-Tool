import React from 'react';
import { Bar, Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadarController,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  RadarController,
  Tooltip,
  Legend,
  Filler
);

function AnalysisPanel({ analysis, language }) {
  if (!analysis) return <div className="alert alert-info">No analysis data available</div>;

  const metrics = analysis.financial_metrics;
  const ratios = {
    ...analysis.liquidity_ratios,
    ...analysis.profitability_ratios,
    ...analysis.leverage_ratios
  };

  const getRiskColor = (risk) => {
    switch(risk.toLowerCase()) {
      case 'low risk': return 'success';
      case 'medium risk': return 'warning';
      case 'high risk': return 'danger';
      case 'critical risk': return 'danger';
      default: return 'secondary';
    }
  };

  // Financial Metrics Chart
  const metricsChartData = {
    labels: ['Revenue', 'Expenses', 'Profit'],
    datasets: [{
      label: 'Amount (₹)',
      data: [metrics.annual_revenue, metrics.total_expenses, metrics.net_profit],
      backgroundColor: ['#4ECDC4', '#FF6B6B', '#45B7D1'],
      borderColor: ['#4ECDC4', '#FF6B6B', '#45B7D1'],
      borderWidth: 2
    }]
  };

  // Ratio Comparison Chart
  const ratioChartData = {
    labels: ['Current Ratio', 'Quick Ratio', 'ROE (%)', 'Asset Turnover'],
    datasets: [{
      label: 'Ratio Values',
      data: [
        ratios.current_ratio || 0,
        ratios.quick_ratio || 0,
        (ratios.roe || 0) / 10,
        ratios.asset_turnover || 0
      ],
      borderColor: '#FF6B6B',
      backgroundColor: 'rgba(255, 107, 107, 0.1)',
      fill: true,
      tension: 0.4,
      borderWidth: 2,
      pointBackgroundColor: '#FF6B6B',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 5
    }]
  };

  return (
    <div className="analysis-container p-4">
      <h1 className="mb-4">📈 Financial Analysis</h1>

      {/* Summary Cards */}
      <div className="row mb-4">
        <div className="col-md-3">
          <div className="card">
            <div className="card-body text-center">
              <h5 className="card-title">Business ID</h5>
              <p className="card-text">{analysis.business_id}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card">
            <div className="card-body text-center">
              <h5 className="card-title">Industry</h5>
              <p className="card-text">{analysis.industry_type}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card">
            <div className="card-body text-center">
              <h5 className="card-title">Health Score</h5>
              <p className="card-text display-6">{analysis.financial_health.health_score}</p>
            </div>
          </div>
        </div>
        <div className="col-md-3">
          <div className="card">
            <div className="card-body text-center">
              <h5 className="card-title">Risk Level</h5>
              <p>
                <span className={`badge bg-${getRiskColor(analysis.financial_health.risk_category)} p-2`}>
                  {analysis.financial_health.risk_category}
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Financial Metrics Section */}
      <div className="row mb-4">
        <div className="col-md-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Financial Metrics Overview</h5>
              <div className="row">
                <div className="col-md-6">
                  <div style={{ maxHeight: '300px' }}>
                    <Bar
                      data={metricsChartData}
                      options={{
                        maintainAspectRatio: false,
                        responsive: true,
                        plugins: {
                          legend: { display: true, position: 'top' }
                        }
                      }}
                      height={300}
                    />
                  </div>
                </div>
                <div className="col-md-6">
                  <table className="table table-sm">
                    <tbody>
                      <tr>
                        <td><strong>Annual Revenue</strong></td>
                        <td className="text-end">₹{metrics.annual_revenue.toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td><strong>Total Expenses</strong></td>
                        <td className="text-end">₹{metrics.total_expenses.toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td><strong>Net Profit</strong></td>
                        <td className="text-end text-success"><strong>₹{metrics.net_profit.toLocaleString()}</strong></td>
                      </tr>
                      <tr>
                        <td><strong>Total Assets</strong></td>
                        <td className="text-end">₹{metrics.total_assets.toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td><strong>Total Liabilities</strong></td>
                        <td className="text-end">₹{metrics.total_liabilities.toLocaleString()}</td>
                      </tr>
                      <tr>
                        <td><strong>Equity</strong></td>
                        <td className="text-end">₹{metrics.equity.toLocaleString()}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Ratios Analysis */}
      <div className="row mb-4">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Liquidity Ratios</h5>
              <table className="table table-sm">
                <tbody>
                  <tr>
                    <td><strong>Current Ratio</strong></td>
                    <td className="text-end">{ratios.current_ratio?.toFixed(2)}</td>
                    <td><span className={`badge bg-${ratios.current_ratio >= 1.5 ? 'success' : 'warning'}`}>
                      {ratios.current_ratio >= 1.5 ? 'Good' : 'Fair'}
                    </span></td>
                  </tr>
                  <tr>
                    <td><strong>Quick Ratio</strong></td>
                    <td className="text-end">{ratios.quick_ratio?.toFixed(2)}</td>
                    <td><span className={`badge bg-${ratios.quick_ratio >= 1.0 ? 'success' : 'warning'}`}>
                      {ratios.quick_ratio >= 1.0 ? 'Good' : 'Fair'}
                    </span></td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Profitability Ratios</h5>
              <table className="table table-sm">
                <tbody>
                  <tr>
                    <td><strong>Profit Margin (%)</strong></td>
                    <td className="text-end">{ratios.profit_margin?.toFixed(2)}%</td>
                  </tr>
                  <tr>
                    <td><strong>ROA (%)</strong></td>
                    <td className="text-end">{ratios.roa?.toFixed(2)}%</td>
                  </tr>
                  <tr>
                    <td><strong>ROE (%)</strong></td>
                    <td className="text-end">{ratios.roe?.toFixed(2)}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* Leverage and Efficiency */}
      <div className="row">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Leverage Ratios</h5>
              <table className="table table-sm">
                <tbody>
                  <tr>
                    <td><strong>Debt-to-Equity</strong></td>
                    <td className="text-end">{ratios.debt_equity_ratio?.toFixed(2)}</td>
                  </tr>
                  <tr>
                    <td><strong>Debt Ratio</strong></td>
                    <td className="text-end">{ratios.debt_ratio?.toFixed(2)}</td>
                  </tr>
                  <tr>
                    <td><strong>DSCR</strong></td>
                    <td className="text-end">{ratios.dscr?.toFixed(2)}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Efficiency Ratios</h5>
              <table className="table table-sm">
                <tbody>
                  <tr>
                    <td><strong>Asset Turnover</strong></td>
                    <td className="text-end">{analysis.efficiency_ratios?.asset_turnover?.toFixed(2)}</td>
                  </tr>
                  <tr>
                    <td><strong>Days Inventory</strong></td>
                    <td className="text-end">{analysis.efficiency_ratios?.days_inventory}</td>
                  </tr>
                  <tr>
                    <td><strong>Days Receivables</strong></td>
                    <td className="text-end">{analysis.efficiency_ratios?.days_receivables}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {/* GST Compliance */}
      <div className="row mt-4">
        <div className="col-md-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Tax Compliance Status</h5>
              <p>
                <strong>GST Compliance:</strong> {' '}
                <span className={`badge bg-${analysis.gst_compliance === 'Compliant' ? 'success' : 'warning'}`}>
                  {analysis.gst_compliance}
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AnalysisPanel;
