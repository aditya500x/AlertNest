const http = require('http');
const express = require('express');
const cors = require('cors');
const { Server } = require('socket.io');
require('dotenv').config();

const incidentRoutes = require('./routes/incidents');
const chatRoutes = require('./routes/chat');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: '*',
  }
});

app.use(cors());
app.use(express.json());

// Pass io to routes via middleware
app.use((req, res, next) => {
  req.io = io;
  next();
});

// Setup socket.io
io.on('connection', (socket) => {
  console.log(`[Socket.IO] New client connected: ${socket.id}`);
  
  socket.on('disconnect', () => {
    console.log(`[Socket.IO] Client disconnected: ${socket.id}`);
  });
});

// Routes
app.use('/incident', incidentRoutes);
app.use('/incidents', incidentRoutes); // Support plural
app.use('/chat', chatRoutes); // Can also be embedded inside incident map

// Healthcheck
app.get('/', (req, res) => {
  res.json({ status: 'ok', service: 'AlertNest Backend MVP' });
});

const PORT = process.env.PORT || 3000;

server.listen(PORT, () => {
  console.log(`[Server] AlertNest backend running on port ${PORT}`);
});
