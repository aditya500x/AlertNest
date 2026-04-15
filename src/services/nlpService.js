/**
 * A basic Mock NLP service to extract type, severity, and location.
 * Replaces expensive LLM calls for MVP.
 */
function parseIncident(text) {
  const lowerText = text.toLowerCase();
  
  let type = 'SECURITY';
  if (lowerText.includes('fire') || lowerText.includes('smoke') || lowerText.includes('burn')) {
    type = 'FIRE';
  } else if (lowerText.includes('medical') || lowerText.includes('heart') || lowerText.includes('breath') || lowerText.includes('bleed') || lowerText.includes('faint')) {
    type = 'MEDICAL';
  }

  let severity = 'LOW';
  if (lowerText.includes('huge') || lowerText.includes('severe') || lowerText.includes('emergency') || lowerText.includes('gun') || lowerText.includes('died') || lowerText.includes('unconscious')) {
    severity = 'HIGH';
  } else if (lowerText.includes('smoke') || lowerText.includes('blood') || lowerText.includes('thief')) {
    severity = 'MEDIUM';
  }

  // Very rudimentary location extraction (e.g. "room 304", "floor 2")
  let location = 'Unknown';
  const roomMatch = lowerText.match(/(room|floor|section|area)\s+([a-z0-9]+)/i);
  if (roomMatch) {
    location = `${roomMatch[1]} ${roomMatch[2]}`;
  } else if (lowerText.includes('lobby')) {
    location = 'lobby';
  } else if (lowerText.includes('cafeteria')) {
    location = 'cafeteria';
  }

  return { type, severity, location };
}

module.exports = { parseIncident };
