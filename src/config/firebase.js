const admin = require('firebase-admin');

// Mock structure for when Firebase credentials are not provided (Hackathon MVP fallback)
class MockDb {
  data = { incidents: {}, chat: {} };
  
  collection(name) {
    return {
      doc: (id) => ({
        set: async (val) => { 
          if (!this.data[name]) this.data[name] = {};
          this.data[name][id] = val; 
        },
        update: async (val) => {
          this.data[name][id] = { ...this.data[name][id], ...val };
        },
        get: async () => ({
          exists: !!this.data[name]?.[id],
          data: () => this.data[name]?.[id]
        }),
        collection: (subName) => ({
          add: async (val) => {
            const subId = Date.now().toString();
            if (!this.data[name][id].sub) this.data[name][id].sub = {};
            this.data[name][id].sub[subId] = val;
            return { id: subId };
          },
          get: async () => {
            const subData = this.data[name]?.[id]?.sub || {};
            return { docs: Object.entries(subData).map(([subId, subVal]) => ({ id: subId, data: () => subVal })) };
          }
        })
      }),
      add: async (val) => {
        if (!this.data[name]) this.data[name] = {};
        const id = Date.now().toString();
        this.data[name][id] = val;
        return { id };
      },
      get: async () => {
        const docs = Object.entries(this.data[name] || {}).map(([id, val]) => ({
          id,
          data: () => val
        }));
        return { docs };
      }
    };
  }
}

// Check for credentials
const serviceAccountRaw = process.env.FIREBASE_SERVICE_ACCOUNT_KEY;

let db;
let auth;
let messaging;
let isMock = false;

if (serviceAccountRaw) {
  try {
    const serviceAccount = JSON.parse(serviceAccountRaw);
    admin.initializeApp({
      credential: admin.credential.cert(serviceAccount)
    });
    db = admin.firestore();
    auth = admin.auth();
    messaging = admin.messaging();
    console.log('[Firebase] Initialized real Firebase services.');
  } catch (error) {
    console.error('[Firebase] Failed to parse Service Account Key, falling back to Mock:', error.message);
    isMock = true;
  }
} else {
  console.log('[Firebase] No Service Account provided, using Mock DB for MVP demo.');
  isMock = true;
}

if (isMock) {
  db = new MockDb();
  auth = {
    verifyIdToken: async (token) => {
      // Very basic mock verification
      if (token === 'mock-admin-token') return { uid: 'admin-1', role: 'admin' };
      if (token === 'mock-staff-token') return { uid: 'staff-1', role: 'staff' };
      return { uid: 'guest-1', role: 'guest' };
    }
  };
  messaging = {
    send: async (msg) => {
      console.log('[FCM-Mock] Push Notification Sent:', msg);
      return 'mock-message-id';
    }
  };
}

module.exports = { db, auth, messaging, isMock };
