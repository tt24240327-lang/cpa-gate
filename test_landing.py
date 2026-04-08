from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Serve the copied prototype HTML file
    file_path = os.path.join(os.path.dirname(__file__), 'comparison_test.html')
    return send_file(file_path)

if __name__ == '__main__':
    print("\n=========================================================")
    print("[Local Test Server Running]")
    print("Open your browser and visit: ")
    print("http://127.0.0.1:8080")
    print("=========================================================\n")
    # Run on port 8080 to avoid clashing with the main app if it's running
    app.run(host='0.0.0.0', port=8080, debug=False)
