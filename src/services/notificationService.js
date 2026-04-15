const { messaging } = require('../config/firebase');

/**
 * Handles routing the notification based on the incident type.
 */
async function routeNotification(incident) {
  const { type, location, severity, id } = incident;

  const payload = {
    notification: {
      title: `${severity} ${type} Alert!`,
      body: `Location: ${location}. Please respond immediately.`
    },
    data: {
      incidentId: id,
      type
    }
  };

  // Smart Routing Logic Mock
  let targetTopic = 'all';

  if (type === 'FIRE') {
    console.log(`[SmartRouting] FIRE -> Routing to ALL STAFF and ADMINS`);
    targetTopic = 'all_staff';
  } else if (type === 'MEDICAL') {
    console.log(`[SmartRouting] MEDICAL -> Routing to NEAREST MEDICAL STAFF`);
    targetTopic = 'medical_staff';
  } else if (type === 'SECURITY') {
    console.log(`[SmartRouting] SECURITY -> Routing to SECURITY and ADMINS`);
    targetTopic = 'security_staff';
  }

  // Normally we would subscribe users to these topics or query their FCM tokens
  payload.topic = targetTopic;

  try {
    // Send via Firebase Cloud Messaging
    await messaging.send(payload);
    console.log(`[FCM] Successfully sent notification to topic: ${targetTopic}`);
  } catch (error) {
    if (error.code === 'messaging/topic-management-error' || error.message.includes('not connected') || error.message.includes('Mock')) {
      console.log(`[FCM-Fallback] Pseudo-sent via console (No real FCM config):`, JSON.stringify(payload));
    } else {
      console.error('[FCM] Error sending message:', error);
    }
  }
}

module.exports = { routeNotification };
