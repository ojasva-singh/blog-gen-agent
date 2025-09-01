"""
Simple Health Check Server for LinkedIn Post Generator App
Provides /health endpoint that returns 200 OK for deployment monitoring
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import datetime
import os
import sys

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Handler for health check requests"""
    
    def do_GET(self):
        """Handle GET requests"""
        
        if self.path == '/health':
            self.send_health_response()
        elif self.path == '/' or self.path == '/status':
            self.send_status_response()
        else:
            self.send_404_response()
    
    def do_HEAD(self):
        """Handle HEAD requests (for some monitoring systems)"""
        if self.path in ['/health', '/', '/status']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_health_response(self):
        """Send health check response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "healthy",
            "message": "AI LinkedIn Post Generator is running",
            "timestamp": datetime.datetime.now().isoformat(),
            "service": "linkedin-post-generator"
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def send_status_response(self):
        """Send detailed status response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Check if required environment variables exist
        env_status = {
            "GEMINI_API_KEY": "configured" if os.getenv("GEMINI_API_KEY") else "missing"
        }
        
        response = {
            "status": "running",
            "service": "AI LinkedIn Post Generator",
            "version": "1.0.0",
            "description": "Personalized LinkedIn post generation using AI",
            "timestamp": datetime.datetime.now().isoformat(),
            "python_version": sys.version,
            "environment": env_status,
            "features": [
                "Profile analysis",
                "Topic recommendations", 
                "Custom post generation",
                "Character limit control",
                "Hashtag management",
                "Media suggestions",
                "Engagement analysis"
            ],
            "endpoints": {
                "/health": "Simple health check",
                "/status": "Detailed service information",
                "/": "Service status"
            }
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def send_404_response(self):
        """Send 404 response for unknown endpoints"""
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            "error": "Not Found",
            "message": f"Endpoint {self.path} not found",
            "available_endpoints": ["/health", "/status", "/"]
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def run_health_server(port=8080):
    """Run the health check server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    
    print(f"🏥 Health Check Server starting on port {port}")
    print(f"📊 Health endpoint: http://localhost:{port}/health")
    print(f"📋 Status endpoint: http://localhost:{port}/status")
    print(f"🏠 Homepage: http://localhost:{port}/")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Health Check Server stopped")
        httpd.server_close()


if __name__ == '__main__':
    # Default port is 8080, but can be overridden via command line or environment
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('HEALTH_PORT', 8080))
    run_health_server(port)