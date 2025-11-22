const http = require('http');
const fs = require('fs');
const path = require('path');

const port = 5000;

// MIME types for different file extensions
const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json'
};

// Create server
const server = http.createServer((req, res) => {
    console.log('Request: ' + req.url);
    
    // Set default file to index.html
    let filePath = req.url === '/' ? '/index.html' : req.url;
    filePath = path.join(__dirname, filePath);
    
    // Get file extension
    const extname = path.extname(filePath);
    const contentType = mimeTypes[extname] || 'text/plain';
    
    // Read and serve the file
    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                res.writeHead(404);
                res.end('File not found');
            } else {
                res.writeHead(500);
                res.end('Server error: ' + error.code);
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

// Start server
server.listen(port, () => {
    console.log('AI Chatbot server is running at: http://localhost:' + port);
    console.log('Serving files from: ' + __dirname);
    console.log('Press Ctrl+C to stop the server');
});