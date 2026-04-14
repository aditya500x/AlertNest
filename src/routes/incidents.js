const express = require('express');
const router = express.Router();
const { db } = require('../config/firebase');
const { parseIncident } = require('../services/nlpService');
const { routeNotification } = require('../services/notificationService');

// POST /incident
router.post('/', async (req, res) => {
  try {
    const { text, reporterId } = req.body;
    
    if (!text) {
      return res.status(400).json({ error: { code: 'BAD_REQUEST', message: 'Missing text parameter' } });
    }

    // Triage using NLP mock
    const { type, severity, location } = parseIncident(text);

    const incidentData = {
      text,
      type,
      severity,
      location,
      status: 'ACTIVE',
      reporterId: reporterId || 'anonymous',
      timestamp: Date.now()
    };

    // Store in DB
    const docRef = await db.collection('incidents').add(incidentData);
    const incident = { id: docRef.id, ...incidentData };

    // Broadcast Real-time
    req.io.emit('new_incident', incident);

    // Push Notifications
    await routeNotification(incident);

    res.status(201).json(incident);
  } catch (error) {
    console.error('[Incidents] Error creating:', error);
    res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Failed to create incident' } });
  }
});

// GET /incidents
router.get('/', async (req, res) => {
  try {
    const snapshot = await db.collection('incidents').get();
    let incidents = [];
    
    snapshot.docs.forEach(doc => {
      incidents.push({ id: doc.id, ...doc.data() });
    });

    // Filter to ACTIVE
    incidents = incidents.filter(i => i.status === 'ACTIVE');

    // Triage Sorting: HIGH > MEDIUM > LOW
    const severityMap = { 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
    incidents.sort((a, b) => severityMap[b.severity] - severityMap[a.severity]);

    res.json(incidents);
  } catch (error) {
    console.error('[Incidents] Error fetching:', error);
    res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch incidents' } });
  }
});

// POST /incident/:id/resolve
router.post('/:id/resolve', async (req, res) => {
  try {
    const { id } = req.params;
    
    const docRef = db.collection('incidents').doc(id);
    const doc = await docRef.get();
    
    if (!doc.exists) {
      return res.status(404).json({ error: { code: 'NOT_FOUND', message: 'Incident not found' } });
    }

    await docRef.update({
      status: 'RESOLVED',
      resolvedAt: Date.now()
    });

    req.io.emit('incident_resolved', { id });

    res.json({ success: true, id, status: 'RESOLVED' });
  } catch (error) {
    console.error('[Incidents] Error resolving:', error);
    res.status(500).json({ error: { code: 'INTERNAL_ERROR', message: 'Failed to resolve incident' } });
  }
});

module.exports = router;
