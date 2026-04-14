const express = require('express');
const router = express.Router();
const { db } = require('../config/firebase');

// Format: /chat/:incidentId

// GET /chat/:incidentId
router.get('/:incidentId', async (req, res) => {
  try {
    const { incidentId } = req.params;

    // Verify incident exists
    const incidentDoc = await db.collection('incidents').doc(incidentId).get();
    if (!incidentDoc.exists) {
      return res.status(404).json({ error: { code: 'NOT_FOUND', message: 'Incident not found' } });
    }

    const snapshot = await db.collection('incidents').doc(incidentId).collection('messages').get();
    
    // Some mock impls don't correctly support complex subcollections immediately, falling back to a global chat table if needed.
    // For MVP, if docs map exists we use it.
    let messages = [];
    if (snapshot && snapshot.docs) {
      messages = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    }

    // Sort chronologically
    messages.sort((a, b) => a.timestamp - b.timestamp);

    res.json(messages);
  } catch (error) {
    console.error('[Chat] Error fetching:', error);
    res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch messages' } });
  }
});

// POST /chat/:incidentId
router.post('/:incidentId', async (req, res) => {
  try {
    const { incidentId } = req.params;
    const { sender, text } = req.body;

    if (!text || !sender) {
      return res.status(400).json({ error: { code: 'BAD_REQUEST', message: 'Missing sender or text parameter' } });
    }

    // Verify incident exists
    const incidentRef = db.collection('incidents').doc(incidentId);
    const incidentDoc = await incidentRef.get();
    if (!incidentDoc.exists) {
      return res.status(404).json({ error: { code: 'NOT_FOUND', message: 'Incident not found' } });
    }

    const messageData = {
      sender,
      text,
      timestamp: Date.now()
    };

    const docRef = await incidentRef.collection('messages').add(messageData);
    const message = { id: docRef.id, ...messageData };

    // Broadcast Chat to room/incidentId channel
    // For MVP keeping it simple and broadcasting to all, but client can filter
    req.io.emit(`chat_update_${incidentId}`, message);

    res.status(201).json(message);
  } catch (error) {
    console.error('[Chat] Error sending:', error);
    res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Failed to send message' } });
  }
});

module.exports = router;
