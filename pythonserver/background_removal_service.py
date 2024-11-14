from flask import Flask, request, jsonify
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/remove-background', methods=['POST'])
def remove_background():
    try:
        # Add CORS headers
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type'
            }
            return ('', 204, headers)

        # Add CORS headers to the response
        headers = {'Access-Control-Allow-Origin': '*'}
        
        file = request.files['image']
        image_data = file.read()
        input_image = Image.open(io.BytesIO(image_data))
        output_image_data = remove(input_image)

        output_image_bytes = io.BytesIO()
        output_image_data.save(output_image_bytes, format='PNG')
        return output_image_bytes.getvalue(), 200, {'Content-Type': 'image/png', **headers}
    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)