import React, { useState } from 'react';

function FileUpload({ onUploadSuccess, apiBase }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [uploadedData, setUploadedData] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      const validTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
      if (validTypes.includes(selectedFile.type)) {
        setFile(selectedFile);
        setError('');
      } else {
        setError('Please select a valid CSV or Excel file');
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch(`${apiBase}/upload`, {
        method: 'POST',
        body: formData
      });

      const data = await res.json();

      if (data.status === 'success') {
        setSuccess(`Successfully processed ${data.data.length} records`);
        setUploadedData(data.data);
        onUploadSuccess(data.data);
        setFile(null);
      } else {
        setError(data.message || 'Upload failed');
      }
    } catch (err) {
      setError(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container p-4">
      <h1 className="mb-4">📁 Upload Financial Data</h1>

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Upload CSV or Excel File</h5>
          <p className="text-muted">Supported formats: CSV (.csv), Excel (.xlsx, .xls)</p>

          {error && <div className="alert alert-danger">{error}</div>}
          {success && <div className="alert alert-success">{success}</div>}

          <div className="mb-3">
            <label htmlFor="fileInput" className="form-label">Select File</label>
            <input
              id="fileInput"
              type="file"
              className="form-control"
              onChange={handleFileChange}
              accept=".csv, .xlsx, .xls"
              disabled={loading}
            />
          </div>

          {file && (
            <div className="alert alert-info">
              Selected file: <strong>{file.name}</strong>
            </div>
          )}

          <button
            className="btn btn-primary"
            onClick={handleUpload}
            disabled={!file || loading}
          >
            {loading ? '⏳ Processing...' : '📤 Upload & Analyze'}
          </button>
        </div>
      </div>

      {/* File Format Guide */}
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">📋 Required File Format</h5>
          <p>Your file should contain the following columns:</p>
          <ul>
            <li><strong>business_id</strong> - Unique identifier</li>
            <li><strong>industry_type</strong> - Business industry</li>
            <li><strong>annual_revenue</strong> - Annual revenue in ₹</li>
            <li><strong>total_expenses</strong> - Total expenses in ₹</li>
            <li><strong>current_assets</strong> - Current assets</li>
            <li><strong>current_liabilities</strong> - Current liabilities</li>
            <li><strong>total_assets</strong> - Total assets</li>
            <li><strong>total_liabilities</strong> - Total liabilities</li>
            <li><strong>gst_compliance_status</strong> - Compliant/Non-Compliant</li>
          </ul>
        </div>
      </div>

      {/* Results Table */}
      {uploadedData && (
        <div className="card">
          <div className="card-body">
            <h5 className="card-title">Uploaded Records</h5>
            <div className="table-responsive">
              <table className="table table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Business ID</th>
                    <th>Health Score</th>
                    <th>Risk Category</th>
                    <th>Profit Margin</th>
                  </tr>
                </thead>
                <tbody>
                  {uploadedData.map((record, idx) => (
                    <tr key={idx}>
                      <td>{record.business_id}</td>
                      <td>
                        <span className="badge bg-info">
                          {record.analysis.financial_health.health_score}
                        </span>
                      </td>
                      <td>
                        <span className={`badge bg-${
                          record.analysis.financial_health.risk_category === 'Low Risk' ? 'success' :
                          record.analysis.financial_health.risk_category === 'Medium Risk' ? 'warning' : 'danger'
                        }`}>
                          {record.analysis.financial_health.risk_category}
                        </span>
                      </td>
                      <td>{record.analysis.profitability_ratios.profit_margin.toFixed(2)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
