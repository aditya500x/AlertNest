const http = require('http');

async function sendRequest(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'localhost',
      port: 3000,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json',
      }
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, data });
        }
      });
    });

    req.on('error', (e) => reject(e));

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

async function runDemo() {
  console.log('--- AlertNest Backend MVP Demo ---');
  await new Promise(r => setTimeout(r, 1000));

  try {
    console.log('\n1. Creating a FIRE emergency...');
    const fireIncident = await sendRequest('POST', '/incident', { text: "Huge fire burning in room 304, people are trying to escape!" });
    console.log('Response:', fireIncident.data);

    await new Promise(r => setTimeout(r, 500));

    console.log('\n2. Creating a MEDICAL emergency...');
    const medIncident = await sendRequest('POST', '/incident', { text: "Someone fainted in the lobby." });
    console.log('Response:', medIncident.data);

    await new Promise(r => setTimeout(r, 500));

    console.log('\n3. Fetching Triage / All Incidents (Should sort HIGH > LOW severity)...');
    const allIncidents = await sendRequest('GET', '/incidents');
    console.log('Active Incidents:', allIncidents);
    if (Array.isArray(allIncidents.data)) {
      allIncidents.data.forEach((inc, idx) => {
        console.log(`  ${idx + 1}. [${inc.severity}] ${inc.type} in ${inc.location || 'Unknown'}`);
      });
    }

    const targetId = fireIncident.data.id;

    console.log('\n4. Sending messages to the Chat system...');
    await sendRequest('POST', `/chat/${targetId}`, { sender: 'System', text: 'Auto-dispatching responders.' });
    await sendRequest('POST', `/chat/${targetId}`, { sender: 'Security Team 1', text: 'We are on our way.' });

    const chatHistory = await sendRequest('GET', `/chat/${targetId}`);
    console.log('Chat History for Incident:');
    chatHistory.data.forEach(msg => {
      console.log(`  [${msg.sender}]: ${msg.text}`);
    });

    console.log('\n5. Resolving the FIRE emergency...');
    const resolveResult = await sendRequest('POST', `/incident/${targetId}/resolve`);
    console.log('Response:', resolveResult.data);

    console.log('\n--- Demo Complete ---');
  } catch (err) {
    console.error('Demo Error (Is the server running?):', err.message);
  }
}

runDemo();
