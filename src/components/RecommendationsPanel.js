import React, { useState } from 'react';

function RecommendationsPanel({ recommendations, language }) {
  const [expandedSection, setExpandedSection] = useState(null);

  if (!recommendations) {
    return <div className="alert alert-info">No recommendations available</div>;
  }

  const toggleSection = (section) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  const renderSection = (title, content, icon) => (
    <div className="card mb-3">
      <div className="card-header bg-light cursor-pointer" onClick={() => toggleSection(title)}>
        <h5 className="mb-0">
          {icon} {title}
          <span className="float-end">
            {expandedSection === title ? '▼' : '▶'}
          </span>
        </h5>
      </div>
      {expandedSection === title && <div className="card-body">{content}</div>}
    </div>
  );

  return (
    <div className="recommendations-container p-4">
      <h1 className="mb-4">💡 AI-Powered Recommendations</h1>

      {/* Executive Summary */}
      <div className="alert alert-info mb-4" role="alert">
        <h5>Executive Summary</h5>
        <p className="mb-0">{recommendations.executive_summary}</p>
      </div>

      {/* Cash Flow Analysis */}
      {renderSection(
        'Cash Flow Analysis',
        <div>
          {recommendations.cash_flow_analysis?.issues.length > 0 && (
            <div className="mb-3">
              <h6 className="text-danger">⚠️ Issues Found:</h6>
              {recommendations.cash_flow_analysis.issues.map((issue, idx) => (
                <div key={idx} className="alert alert-warning mb-2">
                  <strong>{issue.severity} - {issue.issue}</strong>
                  <p className="mb-1">{issue.detail}</p>
                  <small><em>{issue.action}</em></small>
                </div>
              ))}
            </div>
          )}
          {recommendations.cash_flow_analysis?.opportunities.length > 0 && (
            <div>
              <h6 className="text-success">✅ Opportunities:</h6>
              {recommendations.cash_flow_analysis.opportunities.map((opp, idx) => (
                <p key={idx} className="mb-2">✓ {opp}</p>
              ))}
            </div>
          )}
        </div>,
        '💰'
      )}

      {/* Debt Analysis */}
      {renderSection(
        'Debt Analysis',
        <div>
          {recommendations.debt_analysis?.map((rec, idx) => (
            <div key={idx} className={`alert alert-${
              rec.priority === 'Critical' ? 'danger' :
              rec.priority === 'High' ? 'warning' : 'info'
            } mb-2`}>
              <strong>{rec.recommendation}</strong>
              <p className="mb-1">{rec.detail}</p>
              <small><em>Action: {rec.action}</em></small>
            </div>
          ))}
        </div>,
        '💳'
      )}

      {/* Cost Optimization */}
      {recommendations.cost_optimization?.length > 0 && renderSection(
        'Cost Optimization Opportunities',
        <div>
          {recommendations.cost_optimization.map((item, idx) => (
            <div key={idx} className="mb-3 p-3 border rounded">
              <h6 className="text-primary">{item.category}: {item.title}</h6>
              <p>{item.detail}</p>
              {item.target_saving && (
                <p className="text-success"><strong>{item.target_saving}</strong></p>
              )}
              {item.opportunity && (
                <p className="text-info"><strong>{item.opportunity}</strong></p>
              )}
              {item.action_items && (
                <div>
                  <strong>Action Items:</strong>
                  <ul className="mb-0">
                    {item.action_items.map((action, aidx) => (
                      <li key={aidx}>{action}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>,
        '💸'
      )}

      {/* Financial Products */}
      {recommendations.financial_products?.length > 0 && renderSection(
        'Suitable Financial Products',
        <div className="row">
          {recommendations.financial_products.map((product, idx) => (
            <div key={idx} className="col-md-6 mb-3">
              <div className="card h-100">
                <div className="card-body">
                  <h6 className="card-title text-primary">{product.product}</h6>
                  <p className="mb-1">
                    <strong>Eligibility:</strong> {' '}
                    <span className="badge bg-success">{product.eligibility}</span>
                  </p>
                  <p className="mb-1">
                    <strong>Amount:</strong> {product.estimated_loan_amount}
                  </p>
                  <p className="mb-1">
                    <strong>Interest Rate:</strong> {product.interest_rate_range}
                  </p>
                  <p className="mb-1">
                    <strong>Tenure:</strong> {product.tenure}
                  </p>
                  <p className="mb-0">{product.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>,
        '🏦'
      )}

      {/* Industry Risks */}
      {renderSection(
        'Industry-Specific Risks',
        <div>
          <p><strong>Industry:</strong> {recommendations.industry_risks?.industry}</p>
          <h6>Identified Risks:</h6>
          <ul>
            {recommendations.industry_risks?.identified_risks.map((risk, idx) => (
              <li key={idx}>{risk}</li>
            ))}
          </ul>
        </div>,
        '⚠️'
      )}

      {/* Tax Compliance */}
      {renderSection(
        'Tax Compliance',
        <div>
          {recommendations.tax_compliance?.map((comp, idx) => (
            <div key={idx} className={`alert alert-${
              comp.priority === 'Critical' ? 'danger' :
              comp.priority === 'High' ? 'warning' : 'info'
            } mb-2`}>
              <strong>{comp.compliance_area}</strong>
              <p className="mb-1">
                Status: <span className={`badge bg-${
                  comp.status === 'Compliant' ? 'success' : 'warning'
                }`}>{comp.status}</span>
              </p>
              <p className="mb-1"><em>{comp.action}</em></p>
              <small>Benefit: {comp.benefit}</small>
            </div>
          ))}
        </div>,
        '📋'
      )}

      {/* Action Plan */}
      {recommendations.action_plan && renderSection(
        'Strategic Action Plan',
        <div>
          {recommendations.action_plan.immediate?.length > 0 && (
            <div className="mb-3">
              <h6 className="text-danger">🚨 Immediate Actions (0-30 days)</h6>
              <ul>
                {recommendations.action_plan.immediate.map((action, idx) => (
                  <li key={idx} className="mb-1">{action}</li>
                ))}
              </ul>
            </div>
          )}

          {recommendations.action_plan.short_term?.length > 0 && (
            <div className="mb-3">
              <h6 className="text-warning">⏳ Short-term (1-3 months)</h6>
              <ul>
                {recommendations.action_plan.short_term.map((action, idx) => (
                  <li key={idx} className="mb-1">{action}</li>
                ))}
              </ul>
            </div>
          )}

          {recommendations.action_plan.medium_term?.length > 0 && (
            <div className="mb-3">
              <h6 className="text-info">📅 Medium-term (3-6 months)</h6>
              <ul>
                {recommendations.action_plan.medium_term.map((action, idx) => (
                  <li key={idx} className="mb-1">{action}</li>
                ))}
              </ul>
            </div>
          )}

          {recommendations.action_plan.long_term?.length > 0 && (
            <div>
              <h6 className="text-success">🎯 Long-term (6+ months)</h6>
              <ul>
                {recommendations.action_plan.long_term.map((action, idx) => (
                  <li key={idx} className="mb-1">{action}</li>
                ))}
              </ul>
            </div>
          )}
        </div>,
        '📊'
      )}
    </div>
  );
}

export default RecommendationsPanel;
