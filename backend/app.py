from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from functools import wraps
import traceback

# Import modules
from data_loader import (
    load_business_data, load_data_from_file, validate_financial_data,
    normalize_financial_data, get_all_businesses, UPLOAD_FOLDER
)
from analysis import perform_analysis
from recommendation import generate_recommendation
from report_generator import generate_pdf_report, generate_json_report, export_to_excel
from translations import get_translation, translate_analysis

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['JSON_SORT_KEYS'] = False

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'status': 'error', 'message': 'Bad request', 'details': str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error', 'details': str(error)}), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Check API health status"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

# Main analysis endpoint
@app.route('/api/analysis/<business_id>', methods=['GET'])
def get_business_analysis(business_id):
    """Get complete financial analysis for a business"""
    try:
        language = request.args.get('language', 'en')
        
        # Load business data
        df = load_business_data(business_id)
        if df is None or df.empty:
            return jsonify({
                'status': 'error',
                'message': f'Business with ID {business_id} not found'
            }), 404
        
        # Perform analysis
        analysis = perform_analysis(df)
        if analysis is None:
            return jsonify({
                'status': 'error',
                'message': 'Failed to perform analysis'
            }), 500
        
        # Generate recommendations
        recommendations = generate_recommendation(df, analysis)
        
        # Translate if needed
        if language != 'en':
            analysis = translate_analysis(analysis, language)
        
        return jsonify({
            'status': 'success',
            'data': {
                'business_id': business_id,
                'analysis': analysis,
                'recommendations': recommendations
            }
        }), 200
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': 'Error performing analysis',
            'details': str(e)
        }), 500

# List all businesses endpoint
@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    """Get list of all businesses"""
    try:
        businesses = get_all_businesses()
        return jsonify({
            'status': 'success',
            'count': len(businesses),
            'data': businesses
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error fetching businesses',
            'details': str(e)
        }), 500

# File upload and analysis
@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload financial data file (CSV, XLSX) and perform analysis"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No file selected'
            }), 400
        
        # Save file
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Load and validate data
        df, error = load_data_from_file(file_path)
        if error:
            return jsonify({
                'status': 'error',
                'message': 'Failed to load file',
                'details': error
            }), 400
        
        # Normalize data
        df = normalize_financial_data(df)
        
        # Validate data
        is_valid, validation_msg = validate_financial_data(df)
        if not is_valid:
            return jsonify({
                'status': 'error',
                'message': 'Data validation failed',
                'details': validation_msg
            }), 400
        
        # Perform analysis on each business in the file
        results = []
        for idx, row in df.iterrows():
            row_df = df.iloc[[idx]]
            analysis = perform_analysis(row_df)
            recommendations = generate_recommendation(row_df, analysis)
            
            results.append({
                'business_id': analysis['business_id'],
                'analysis': analysis,
                'recommendations': recommendations
            })
        
        return jsonify({
            'status': 'success',
            'message': f'Processed {len(results)} records',
            'file_path': filename,
            'data': results
        }), 200
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': 'Error processing file',
            'details': str(e)
        }), 500

# Generate PDF report
@app.route('/api/report/pdf/<business_id>', methods=['GET'])
def get_pdf_report(business_id):
    """Generate and download PDF report"""
    try:
        # Load data and analysis
        df = load_business_data(business_id)
        if df is None or df.empty:
            return jsonify({
                'status': 'error',
                'message': 'Business not found'
            }), 404
        
        analysis = perform_analysis(df)
        recommendations = generate_recommendation(df, analysis)
        
        business_data = {
            'business_id': business_id,
            'industry_type': df['industry_type'].iloc[0] if 'industry_type' in df.columns else 'Unknown'
        }
        
        # Generate PDF
        pdf_buffer, error = generate_pdf_report(business_data, analysis, recommendations)
        if error:
            return jsonify({
                'status': 'error',
                'message': 'Failed to generate report',
                'details': error
            }), 500
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'{business_id}_financial_report_{datetime.now().strftime("%Y%m%d")}.pdf'
        )
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': 'Error generating report',
            'details': str(e)
        }), 500

# Generate Excel report
@app.route('/api/report/excel/<business_id>', methods=['GET'])
def get_excel_report(business_id):
    """Generate and download Excel report"""
    try:
        # Load data and analysis
        df = load_business_data(business_id)
        if df is None or df.empty:
            return jsonify({
                'status': 'error',
                'message': 'Business not found'
            }), 404
        
        analysis = perform_analysis(df)
        recommendations = generate_recommendation(df, analysis)
        
        business_data = {
            'business_id': business_id,
            'industry_type': df['industry_type'].iloc[0] if 'industry_type' in df.columns else 'Unknown'
        }
        
        # Generate Excel
        excel_buffer, error = export_to_excel(business_data, analysis, recommendations)
        if error:
            return jsonify({
                'status': 'error',
                'message': 'Failed to generate report',
                'details': error
            }), 500
        
        return send_file(
            excel_buffer,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f'{business_id}_financial_report_{datetime.now().strftime("%Y%m%d")}.xlsx'
        )
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': 'Error generating report',
            'details': str(e)
        }), 500

# Get analysis as JSON
@app.route('/api/report/json/<business_id>', methods=['GET'])
def get_json_report(business_id):
    """Get analysis as JSON report"""
    try:
        df = load_business_data(business_id)
        if df is None or df.empty:
            return jsonify({
                'status': 'error',
                'message': 'Business not found'
            }), 404
        
        analysis = perform_analysis(df)
        recommendations = generate_recommendation(df, analysis)
        
        business_data = {
            'business_id': business_id,
            'industry_type': df['industry_type'].iloc[0] if 'industry_type' in df.columns else 'Unknown'
        }
        
        report = generate_json_report(business_data, analysis, recommendations)
        
        return jsonify({
            'status': 'success',
            'data': report
        }), 200
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': 'Error generating report',
            'details': str(e)
        }), 500

# Multilingual support
@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages"""
    from translations import get_supported_languages
    return jsonify({
        'status': 'success',
        'languages': get_supported_languages()
    }), 200

# Translation endpoint
@app.route('/api/translate/<key>', methods=['GET'])
def translate_key(key):
    """Translate a key to specified language"""
    language = request.args.get('language', 'en')
    translation = get_translation(key, language)
    
    return jsonify({
        'status': 'success',
        'key': key,
        'language': language,
        'translation': translation
    }), 200

# Batch analysis endpoint
@app.route('/api/batch-analysis', methods=['POST'])
def batch_analysis():
    """Perform analysis on multiple businesses"""
    try:
        data = request.get_json()
        
        if not data or 'business_ids' not in data:
            return jsonify({
                'status': 'error',
                'message': 'business_ids array required'
            }), 400
        
        business_ids = data['business_ids']
        language = data.get('language', 'en')
        
        results = []
        for business_id in business_ids:
            df = load_business_data(business_id)
            if df is not None and not df.empty:
                analysis = perform_analysis(df)
                recommendations = generate_recommendation(df, analysis)
                
                if language != 'en':
                    analysis = translate_analysis(analysis, language)
                
                results.append({
                    'business_id': business_id,
                    'status': 'success',
                    'analysis': analysis,
                    'recommendations': recommendations
                })
            else:
                results.append({
                    'business_id': business_id,
                    'status': 'not_found'
                })
        
        return jsonify({
            'status': 'success',
            'count': len(results),
            'data': results
        }), 200
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': 'Batch analysis failed',
            'details': str(e)
        }), 500

# Dashboard metrics endpoint
@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_metrics():
    """Get dashboard summary metrics"""
    try:
        businesses = get_all_businesses()
        
        total_revenue = sum([b.get('annual_revenue', 0) for b in businesses])
        avg_score = sum([b.get('financial_health_score', 0) for b in businesses]) / len(businesses) if businesses else 0
        
        risk_distribution = {
            'low_risk': len([b for b in businesses if 'Low' in b.get('financial_health_score', '')]),
            'medium_risk': len([b for b in businesses if 'Medium' in b.get('financial_health_score', '')]),
            'high_risk': len([b for b in businesses if 'High' in b.get('financial_health_score', '')])
        }
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_businesses': len(businesses),
                'total_revenue': total_revenue,
                'average_health_score': round(avg_score, 2),
                'risk_distribution': risk_distribution,
                'businesses': businesses[:10]  # Top 10
            }
        }), 200
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({
            'status': 'error',
            'message': 'Failed to fetch dashboard metrics',
            'details': str(e)
        }), 500

# API Documentation
@app.route('/api/docs', methods=['GET'])
def api_docs():
    """Get API documentation"""
    docs = {
        'title': 'Financial Health Assessment Tool API',
        'version': '1.0.0',
        'endpoints': {
            'GET /api/health': 'Health check',
            'GET /api/analysis/<business_id>': 'Get comprehensive financial analysis',
            'GET /api/businesses': 'List all businesses',
            'POST /api/upload': 'Upload and analyze financial data file',
            'GET /api/report/pdf/<business_id>': 'Download PDF report',
            'GET /api/report/excel/<business_id>': 'Download Excel report',
            'GET /api/report/json/<business_id>': 'Get JSON report',
            'POST /api/batch-analysis': 'Analyze multiple businesses',
            'GET /api/dashboard': 'Get dashboard metrics',
            'GET /api/languages': 'Get supported languages',
            'GET /api/docs': 'Get API documentation'
        }
    }
    return jsonify(docs), 200

# Error logging middleware
@app.before_request
def log_request():
    """Log incoming requests"""
    app.logger.info(f"{request.method} {request.path}")

if __name__ == "__main__":
    print("Starting Financial Health Assessment Tool API...")
    print("Server running at http://127.0.0.1:5000")
    print("API Documentation: http://127.0.0.1:5000/api/docs")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)