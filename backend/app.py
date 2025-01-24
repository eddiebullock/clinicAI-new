from flask import Flask
from routes.upload import upload_bp

app = Flask(__name__)

# Register the upload blueprint
app.register_blueprint(upload_bp)

if __name__ == "__main__":
    app.run(debug=True)
