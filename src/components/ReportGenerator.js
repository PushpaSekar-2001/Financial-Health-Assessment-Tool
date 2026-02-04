import React, { useState } from 'react';

function ReportGenerator({ businessId, apiBase }) {
  const [generating, setGenerating] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const generateReport = async (format) => {
    setGenerating(format);
    setError('');
    setSuccess('');

    try {
      const url = `${apiBase}/report/${format}/${businessId}`;

      // For PDF and Excel, download the file
      if (format === 'pdf' || format === 'excel') {
        const response = await fetch(url);
        
        if (!response.ok) {
          const data = await response.json();
          setError(data.message || 'Failed to generate report');
          return;
        }

        const blob = await response.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `${businessId}_report.${format === 'pdf' ? 'pdf' : 'xlsx'}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);
        document.body.removeChild(a);

        setSuccess(`${format.toUpperCase()} report downloaded successfully!`);
      } else {
        // For JSON, display in a modal or new tab
        const response = await fetch(url);
        const data = await response.json();

        if (data.status === 'success') {
          // Open in new tab with formatted JSON
          const jsonString = JSON.stringify(data.data, null, 2);
          const newTab = window.open();
          newTab.document.write(`<pre>${jsonString}</pre>`);
          setSuccess('JSON report opened in new tab');
        } else {
          setError(data.message || 'Failed to generate report');
        }
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setGenerating('');
    }
  };

  return (
    <div className="reports-container p-4">
      <h1 className="mb-4">📄 Generate Reports</h1>

      {error && <div className="alert alert-danger">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      <div className="row">
        {/* PDF Report */}
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h5 className="card-title">📕 PDF Report</h5>
              <p className="card-text">
                Professional investor-ready report with detailed analysis, charts, and recommendations.
              </p>
              <button
                className="btn btn-primary"
                onClick={() => generateReport('pdf')}
                disabled={generating !== ''}
              >
                {generating === 'pdf' ? '⏳ Generating...' : '📥 Download PDF'}
              </button>
            </div>
          </div>
        </div>

        {/* Excel Report */}
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h5 className="card-title">📗 Excel Report</h5>
              <p className="card-text">
                Spreadsheet format with financial metrics, ratios, and data that can be further analyzed.
              </p>
              <button
                className="btn btn-success"
                onClick={() => generateReport('excel')}
                disabled={generating !== ''}
              >
                {generating === 'excel' ? '⏳ Generating...' : '📥 Download Excel'}
              </button>
            </div>
          </div>
        </div>

        {/* JSON Report */}
        <div className="col-md-4 mb-4">
          <div className="card h-100">
            <div className="card-body text-center">
              <h5 className="card-title">📘 JSON Report</h5>
              <p className="card-text">
                Machine-readable format ideal for integration with other systems and APIs.
              </p>
              <button
                className="btn btn-info"
                onClick={() => generateReport('json')}
                disabled={generating !== ''}
              >
                {generating === 'json' ? '⏳ Generating...' : '📥 View JSON'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Report Details */}
      <div className="row mt-4">
        <div className="col-md-12">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">📊 What's Included in Reports?</h5>
              <div className="row">
                <div className="col-md-6">
                  <h6>Financial Analysis</h6>
                  <ul>
                    <li>Annual revenue & expenses</li>
                    <li>Net profit & profitability</li>
                    <li>Assets & liabilities breakdown</li>
                    <li>Working capital metrics</li>
                  </ul>
                </div>
                <div className="col-md-6">
                  <h6>Financial Ratios</h6>
                  <ul>
                    <li>Liquidity ratios (Current, Quick)</li>
                    <li>Profitability ratios (ROA, ROE)</li>
                    <li>Leverage ratios (D/E, Debt Ratio)</li>
                    <li>Efficiency metrics</li>
                  </ul>
                </div>
              </div>
              <hr />
              <div className="row">
                <div className="col-md-6">
                  <h6>Assessment & Risk</h6>
                  <ul>
                    <li>Financial health score</li>
                    <li>Risk category assessment</li>
                    <li>Creditworthiness score</li>
                    <li>GST compliance status</li>
                  </ul>
                </div>
                <div className="col-md-6">
                  <h6>Recommendations</h6>
                  <ul>
                    <li>Cost optimization opportunities</li>
                    <li>Suitable financial products</li>
                    <li>Industry-specific insights</li>
                    <li>Strategic action plan</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Business Info */}
      <div className="alert alert-info mt-4">
        <h6>Business ID: <strong>{businessId}</strong></h6>
        <p className="mb-0">Reports are generated based on the comprehensive financial analysis for this business.</p>
      </div>
    </div>
  );
}

export default ReportGenerator;
