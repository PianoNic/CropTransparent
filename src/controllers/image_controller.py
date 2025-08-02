from flask import Flask, request, send_file, render_template, jsonify
from src.services.image_service import auto_crop_image
import base64
import io
import os

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about')
    def about():
        return render_template('about.html')
    
    @app.route('/api/app-info')
    def app_info():
        environment = os.environ.get('FLASK_ENV', 'unknown environment')
        version = os.environ.get('APP_VERSION', 'unknown version')
        
        return jsonify({
            "environment": environment,
            "version": version
        })

    @app.route('/process', methods=['POST'])
    def process_image():
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        try:
            image_data = file.read()
            output_buffer, original_size, cropped_size, crop_method, background_info, output_format = auto_crop_image(image_data)
            
            encoded = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
            output_buffer.seek(0)
            
            filename = file.filename or 'image.png'
            original_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'png'
            
            # Use the output format from the service, but map it to lowercase for consistency
            if output_format:
                extension = output_format.lower()
                if extension == 'jpeg':
                    extension = 'jpg'
            else:
                # Fallback logic
                if original_extension not in ['png', 'gif', 'webp', 'jpg', 'jpeg']:
                    extension = 'png'
                else:
                    extension = original_extension
                    if extension == 'jpeg':
                        extension = 'jpg'
            
            # Set proper MIME type
            mime_type = 'png'
            if extension == 'jpg':
                mime_type = 'jpeg'
            elif extension in ['gif', 'webp']:
                mime_type = extension
            
            # Create output filename
            base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
            output_filename = f"cropped_{base_name}.{extension}"
            
            response_data = {
                "success": True, 
                "image": f"data:image/{mime_type};base64,{encoded}",
                "filename": output_filename,
                "original_size": f"{original_size[0]}x{original_size[1]}",
                "cropped_size": f"{cropped_size[0]}x{cropped_size[1]}",
                "crop_method": crop_method,
                "output_format": extension
            }
            
            if background_info:
                response_data["background_color"] = background_info
            
            return jsonify(response_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/download', methods=['POST'])
    def download_image():
        try:
            data = request.get_json()
            if not data or 'image' not in data or 'filename' not in data:
                return jsonify({"error": "Missing data"}), 400
            
            image_data = data['image'].split(',')[1]
            image_binary = base64.b64decode(image_data)
            
            output = io.BytesIO(image_binary)
            output.seek(0)
            
            # Determine MIME type from filename extension
            filename = data['filename']
            extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'png'
            
            mime_type_map = {
                'png': 'image/png',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'gif': 'image/gif',
                'webp': 'image/webp'
            }
            
            mime_type = mime_type_map.get(extension, 'image/png')
            
            return send_file(
                output,
                download_name=filename,
                as_attachment=True,
                mimetype=mime_type
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500