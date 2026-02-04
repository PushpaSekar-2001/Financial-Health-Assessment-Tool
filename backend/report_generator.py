from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import os
from pathlib import Path
import json

def generate_pdf_report(business_data, analysis, recommendations):
    """Generate professional PDF report for financial analysis"""
    
    if not business_data or not analysis:
        return None, "Insufficient data for report generation"
    
    try:
        # Create PDF in memory
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter, topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        # Container for PDF elements
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#003366'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#003366'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        normal_style = styles['Normal']
        
        # Title
        elements.append(Paragraph('SME FINANCIAL HEALTH ASSESSMENT REPORT', title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        meta_data = [
            ['Business ID:', business_data['business_id']],
            ['Industry:', business_data['industry_type']],
            ['Report Date:', analysis['analysis_date']],
            ['Assessment Score:', f"{analysis['financial_health']['health_score']}/100"]
        ]
        
        meta_table = Table(meta_data, colWidths=[2*inch, 4*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E8F0F5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        elements.append(Paragraph('EXECUTIVE SUMMARY', heading_style))
        risk_color = get_risk_color(analysis['financial_health']['risk_category'])
        summary_text = f"""
        <b>Financial Health Status:</b> {analysis['financial_health']['risk_category']}<br/>
        <b>Assessment Score:</b> {analysis['financial_health']['health_score']}/100<br/>
        <b>Creditworthiness Score:</b> {analysis['creditworthiness']['score']}/100<br/>
        <b>GST Compliance:</b> {analysis['gst_compliance']}<br/>
        """
        elements.append(Paragraph(summary_text, normal_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Financial Metrics Section
        elements.append(Paragraph('FINANCIAL METRICS', heading_style))
        
        metrics = analysis['financial_metrics']
        financial_data = [
            ['Metric', 'Amount (₹)'],
            ['Annual Revenue', f"₹{metrics['annual_revenue']:,.0f}"],
            ['Total Expenses', f"₹{metrics['total_expenses']:,.0f}"],
            ['Net Profit', f"₹{metrics['net_profit']:,.0f}"],
            ['Total Assets', f"₹{metrics['total_assets']:,.0f}"],
            ['Total Liabilities', f"₹{metrics['total_liabilities']:,.0f}"],
            ['Equity', f"₹{metrics['equity']:,.0f}"],
            ['Current Assets', f"₹{metrics['current_assets']:,.0f}"],
            ['Current Liabilities', f"₹{metrics['current_liabilities']:,.0f}"]
        ]
        
        financial_table = Table(financial_data, colWidths=[3*inch, 3*inch])
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')])
        ]))
        elements.append(financial_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Financial Ratios Section
        elements.append(Paragraph('FINANCIAL RATIOS ANALYSIS', heading_style))
        
        ratios_data = [
            ['Ratio Category', 'Ratio', 'Value', 'Assessment'],
            ['Liquidity', 'Current Ratio', str(analysis['liquidity_ratios']['current_ratio']), 'Good' if analysis['liquidity_ratios']['current_ratio'] > 1.5 else 'Needs Review'],
            ['Liquidity', 'Quick Ratio', str(analysis['liquidity_ratios']['quick_ratio']), 'Good' if analysis['liquidity_ratios']['quick_ratio'] > 1.0 else 'Needs Review'],
            ['Profitability', 'Profit Margin (%)', f"{analysis['profitability_ratios']['profit_margin']:.2f}%", 'Good' if analysis['profitability_ratios']['profit_margin'] > 10 else 'Needs Review'],
            ['Profitability', 'ROA (%)', f"{analysis['profitability_ratios']['roa']:.2f}%", 'Good' if analysis['profitability_ratios']['roa'] > 5 else 'Needs Review'],
            ['Profitability', 'ROE (%)', f"{analysis['profitability_ratios']['roe']:.2f}%", 'Good' if analysis['profitability_ratios']['roe'] > 15 else 'Needs Review'],
            ['Leverage', 'Debt-to-Equity', str(analysis['leverage_ratios']['debt_equity_ratio']), 'Good' if analysis['leverage_ratios']['debt_equity_ratio'] < 1.5 else 'Needs Review'],
            ['Leverage', 'DSCR', str(analysis['leverage_ratios']['dscr']), 'Good' if analysis['leverage_ratios']['dscr'] > 1.2 else 'Needs Review'],
            ['Efficiency', 'Asset Turnover', str(analysis['efficiency_ratios']['asset_turnover']), 'Monitor']
        ]
        
        ratios_table = Table(ratios_data, colWidths=[1.5*inch, 1.8*inch, 1.2*inch, 1.5*inch])
        ratios_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')])
        ]))
        elements.append(ratios_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Recommendations Section
        if recommendations:
            elements.append(PageBreak())
            elements.append(Paragraph('RECOMMENDATIONS', heading_style))
            
            # Cost optimization
            if recommendations.get('cost_optimization'):
                elements.append(Paragraph('<b>Cost Optimization Opportunities:</b>', normal_style))
                for item in recommendations['cost_optimization'][:2]:
                    elements.append(Paragraph(f"• {item['title']}: {item['detail']}", normal_style))
                elements.append(Spacer(1, 0.1*inch))
            
            # Financial products
            if recommendations.get('financial_products'):
                elements.append(Paragraph('<b>Suitable Financial Products:</b>', normal_style))
                for product in recommendations['financial_products'][:3]:
                    elements.append(Paragraph(
                        f"• <b>{product['product']}</b> - {product['estimated_loan_amount']} at {product['interest_rate_range']}",
                        normal_style
                    ))
                elements.append(Spacer(1, 0.1*inch))
            
            # Action plan
            if recommendations.get('action_plan'):
                elements.append(Paragraph('<b>Action Plan:</b>', normal_style))
                if recommendations['action_plan'].get('immediate'):
                    elements.append(Paragraph('<i>Immediate Actions:</i>', normal_style))
                    for action in recommendations['action_plan']['immediate'][:2]:
                        elements.append(Paragraph(f"• {action}", normal_style))
                elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        footer_text = f"Report Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Financial Health Assessment Tool v1.0"
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=normal_style, fontSize=8, textColor=colors.grey)))
        
        # Build PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        return pdf_buffer, None
        
    except Exception as e:
        return None, f"Error generating PDF: {str(e)}"

def get_risk_color(risk_category):
    """Get color code for risk category"""
    colors_map = {
        'Low Risk': '#28A745',
        'Medium Risk': '#FFC107',
        'High Risk': '#FD7E14',
        'Critical Risk': '#DC3545'
    }
    return colors_map.get(risk_category, '#6C757D')

def generate_json_report(business_data, analysis, recommendations):
    """Generate JSON format report for API responses"""
    report = {
        'metadata': {
            'business_id': business_data['business_id'],
            'industry': business_data['industry_type'],
            'report_date': analysis['analysis_date'],
            'report_version': '1.0'
        },
        'financial_analysis': analysis,
        'recommendations': recommendations,
        'generated_at': datetime.now().isoformat()
    }
    return report

def export_to_excel(business_data, analysis, recommendations):
    """Export report to Excel format"""
    try:
        import pandas as pd
        
        # Create Excel writer
        excel_buffer = io.BytesIO()
        writer = pd.ExcelWriter(excel_buffer, engine='openpyxl')
        
        # Sheet 1: Summary
        summary_df = pd.DataFrame({
            'Metric': ['Business ID', 'Industry', 'Financial Health Score', 'Risk Category', 'GST Compliance'],
            'Value': [
                business_data['business_id'],
                business_data['industry_type'],
                f"{analysis['financial_health']['health_score']}/100",
                analysis['financial_health']['risk_category'],
                analysis['gst_compliance']
            ]
        })
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Sheet 2: Financial Metrics
        metrics = analysis['financial_metrics']
        metrics_df = pd.DataFrame({
            'Metric': list(metrics.keys()),
            'Value': list(metrics.values())
        })
        metrics_df.to_excel(writer, sheet_name='Financial Metrics', index=False)
        
        # Sheet 3: Ratios
        ratios_data = []
        for category, values in analysis.items():
            if isinstance(values, dict) and 'ratio' in category.lower():
                for key, value in values.items():
                    ratios_data.append({'Category': category, 'Ratio': key, 'Value': value})
        
        if ratios_data:
            ratios_df = pd.DataFrame(ratios_data)
            ratios_df.to_excel(writer, sheet_name='Financial Ratios', index=False)
        
        writer.close()
        excel_buffer.seek(0)
        return excel_buffer, None
        
    except Exception as e:
        return None, f"Error generating Excel report: {str(e)}"

