import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

void main() {
  runApp(const AlertNestApp());
}

class AlertNestApp extends StatelessWidget {
  const AlertNestApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AlertNest | Tactical Command',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF080F18),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00E5FF),
          secondary: Color(0xFF0052D4),
          surface: Color(0xFF121A25),
          error: Color(0xFFFF716C),
        ),
        textTheme: GoogleFonts.interTextTheme(ThemeData.dark().textTheme),
      ),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(64),
        child: Container(
          decoration: BoxDecoration(
            color: const Color(0xFF080F18).withOpacity(0.9),
            border: const Border(
              bottom: BorderSide(color: Color(0x3300E5FF), width: 1),
            ),
            boxShadow: [
              BoxShadow(
                color: const Color(0xFF00E5FF).withOpacity(0.15),
                blurRadius: 10,
                offset: const Offset(0, 1),
              ),
            ],
          ),
          child: SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.grid_view, color: Color(0xFF00E5FF)),
                      const SizedBox(width: 12),
                      Text(
                        'TACTICAL_COMMAND',
                        style: GoogleFonts.spaceGrotesk(
                          fontSize: 20,
                          fontWeight: FontWeight.w900,
                          letterSpacing: -1,
                          foreground: Paint()
                            ..shader = const LinearGradient(
                              colors: [Color(0xFF00E5FF), Color(0xFF0052D4)],
                            ).createShader(const Rect.fromLTWH(0, 0, 200, 70)),
                        ),
                      ),
                    ],
                  ),
                  Row(
                    children: [
                      Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.end,
                        children: [
                          Text(
                            'SYSTEM_READY',
                            style: GoogleFonts.spaceGrotesk(
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 2,
                              color: const Color(0xFF00E5FF),
                            ),
                          ),
                          Text(
                            'LATENCY: 12MS',
                            style: GoogleFonts.spaceGrotesk(
                              fontSize: 10,
                              color: Colors.blueGrey.shade400,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(width: 16),
                      Container(
                        width: 40,
                        height: 40,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(color: const Color(0x4D00E5FF)),
                          image: const DecorationImage(
                            image: NetworkImage(
                              'https://lh3.googleusercontent.com/aida-public/AB6AXuCJLF0yQ44U1Sz3TytExY0elqZhSpzBsa6RNkVO5-ikdP1IHr39qyTSdZsbI42_ux0O0rzEwfkZWzgnJeB1Dy_Li0p5qyQ_oegSDovEzRmDKYLfz59nGH_POGMeMQAurAxh73x63IBN5XqXq2-PgXVeeLI6W36pZBqWLKg51EmZmcCZQVzsnjq71_qjTu41KtidDiHmxxpqHu7KlEkF69AvQbIZ4Gb0JHuwGKI_9IMPjp1qDDdEiYTKZxwnh7H1d_F6SIJZFxZ0me6B',
                            ),
                            fit: BoxFit.cover,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Status Header
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: const Color(0xFF0C141E),
                  borderRadius: BorderRadius.circular(8),
                  border: const Border(
                    top: BorderSide(color: Color(0x3300E5FF), width: 1),
                  ),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'REPORT INCIDENT',
                            style: GoogleFonts.spaceGrotesk(
                              fontSize: 28,
                              fontWeight: FontWeight.bold,
                              letterSpacing: -0.5,
                              color: Colors.white,
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'AI-powered NLP analysis active. Describe the threat below.',
                            style: GoogleFonts.inter(
                              fontSize: 13,
                              color: Colors.blueGrey.shade300,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        Text(
                          'CURRENT_LOCATION',
                          style: GoogleFonts.spaceGrotesk(
                            fontSize: 10,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 2,
                            color: Colors.blueGrey.shade400,
                          ),
                        ),
                        Text(
                          'ROOM 412',
                          style: GoogleFonts.spaceGrotesk(
                            fontSize: 32,
                            fontWeight: FontWeight.w900,
                            color: Colors.white,
                            shadows: [
                              const Shadow(
                                color: Color(0x4DFFFFFF),
                                blurRadius: 8,
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Input Hub
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 1,
                    child: Container(
                      height: 200,
                      padding: const EdgeInsets.all(24),
                      decoration: BoxDecoration(
                        color: const Color(0x99121A25),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.white.withOpacity(0.05)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'SITUATION_DESCRIPTION',
                            style: GoogleFonts.spaceGrotesk(
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 2,
                              color: const Color(0xFF00E5FF),
                            ),
                          ),
                          const SizedBox(height: 12),
                          const Expanded(
                            child: TextField(
                              maxLines: null,
                              expands: true,
                              decoration: InputDecoration(
                                hintText:
                                    'Describe the current situation in natural language. Our AI will automatically categorize and dispatch necessary units...',
                                hintStyle: TextStyle(
                                  color: Color(0x66A5ABB8),
                                  fontSize: 14,
                                ),
                                border: InputBorder.none,
                                contentPadding: EdgeInsets.zero,
                              ),
                              style: TextStyle(color: Colors.white, fontSize: 14),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    flex: 1,
                    child: Container(
                      height: 200,
                      padding: const EdgeInsets.all(24),
                      decoration: BoxDecoration(
                        color: const Color(0x99121A25),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.white.withOpacity(0.05)),
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'VOICE_TRANSMISSION',
                                style: GoogleFonts.spaceGrotesk(
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                  letterSpacing: 2,
                                  color: const Color(0xFF00E5FF),
                                ),
                              ),
                              const SizedBox(height: 20),
                              Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: List.generate(6, (index) {
                                  double height = [16.0, 32.0, 48.0, 24.0, 40.0, 16.0][index];
                                  double opacity = [0.4, 0.6, 1.0, 0.6, 0.8, 0.4][index];
                                  return Container(
                                    width: 4,
                                    height: height,
                                    margin: const EdgeInsets.symmetric(horizontal: 2),
                                    decoration: BoxDecoration(
                                      color: const Color(0xFF00E5FF).withOpacity(opacity),
                                      borderRadius: BorderRadius.circular(4),
                                    ),
                                  );
                                }),
                              ),
                            ],
                          ),
                          ElevatedButton.icon(
                            onPressed: () {},
                            icon: const Icon(Icons.mic, size: 20),
                            label: Text(
                              'RECORD MEMO',
                              style: GoogleFonts.spaceGrotesk(
                                fontWeight: FontWeight.bold,
                                letterSpacing: 2,
                                fontSize: 12,
                              ),
                            ),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: const Color(0x1A00E5FF),
                              foregroundColor: const Color(0xFF00E5FF),
                              minimumSize: const Size(double.infinity, 56),
                              shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(8),
                                side: const BorderSide(color: Color(0x4D00E5FF)),
                              ),
                              elevation: 0,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 24),

              // Giant Action Button
              Container(
                width: double.infinity,
                height: 80,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(8),
                  gradient: const LinearGradient(
                    colors: [Color(0xFF00E5FF), Color(0xFF0052D4)],
                  ),
                  boxShadow: [
                    BoxShadow(
                      color: const Color(0xFF00E5FF).withOpacity(0.6),
                      blurRadius: 35,
                      spreadRadius: -5,
                    ),
                  ],
                ),
                child: ElevatedButton(
                  onPressed: () {},
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.transparent,
                    shadowColor: Colors.transparent,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        'INITIATE PROTOCOL',
                        style: GoogleFonts.spaceGrotesk(
                          fontSize: 22,
                          fontWeight: FontWeight.w900,
                          letterSpacing: 4,
                          color: const Color(0xFF001C54),
                        ),
                      ),
                      const SizedBox(width: 16),
                      const Icon(Icons.priority_high, color: Color(0xFF001C54), size: 30),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 32),

              // Sector Visual (Map)
              Container(
                decoration: BoxDecoration(
                  color: const Color(0xFF0C141E),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white.withOpacity(0.05)),
                ),
                child: Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            'SECTOR_VISUAL',
                            style: GoogleFonts.spaceGrotesk(
                              fontSize: 10,
                              fontWeight: FontWeight.bold,
                              letterSpacing: 2,
                              color: const Color(0xFF769AFF),
                            ),
                          ),
                          Row(
                            children: [
                              Container(
                                width: 8,
                                height: 8,
                                decoration: const BoxDecoration(
                                  color: Color(0xFF00E5FF),
                                  shape: BoxShape.circle,
                                ),
                              ),
                              const SizedBox(width: 8),
                              Text(
                                'LIVE GPS',
                                style: GoogleFonts.spaceGrotesk(
                                  fontSize: 10,
                                  fontWeight: FontWeight.bold,
                                  color: const Color(0xFF00E5FF),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    Container(
                      height: 250,
                      width: double.infinity,
                      color: const Color(0xFF121A25),
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          Opacity(
                            opacity: 0.4,
                            child: Image.network(
                              'https://maps.googleapis.com/maps/api/staticmap?center=40.7128,-74.0060&zoom=15&size=600x400&style=feature:all|element:all|saturation:-100|lightness:-50|invert_lightness:true&key=UNSET', // Placeholder
                              fit: BoxFit.cover,
                              width: double.infinity,
                              errorBuilder: (c, e, s) => Container(color: Colors.black26),
                            ),
                          ),
                          Container(
                            width: 32,
                            height: 32,
                            decoration: BoxDecoration(
                              color: const Color(0xFF00E5FF),
                              shape: BoxShape.circle,
                              border: Border.all(color: const Color(0xFF080F18), width: 4),
                              boxShadow: [
                                BoxShadow(
                                  color: const Color(0xFF00E5FF).withOpacity(0.8),
                                  blurRadius: 20,
                                ),
                              ],
                            ),
                            child: const Icon(Icons.location_on, size: 14, color: Color(0xFF005762)),
                          ),
                        ],
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text('LAT: 40.7128° N',
                              style: GoogleFonts.spaceGrotesk(fontSize: 12, color: Colors.blueGrey.shade400)),
                          Text('LON: 74.0060° W',
                              style: GoogleFonts.spaceGrotesk(fontSize: 12, color: Colors.blueGrey.shade400)),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Nearby Units
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: const Color(0xFF0C141E),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white.withOpacity(0.05)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'NEARBY UNITS',
                      style: GoogleFonts.spaceGrotesk(
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 2,
                        color: const Color(0xFF00E5FF),
                      ),
                    ),
                    const SizedBox(height: 16),
                    _unitTile(Icons.local_police, 'UNIT_742', '0.8km Away', const Color(0xFF769AFF)),
                    const SizedBox(height: 12),
                    _unitTile(Icons.medical_information, 'MEDIC_A2', 'En Route', const Color(0xFF00E5FF),
                        isHighlight: true),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Survival Protocol
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: const Color(0xFF0C141E),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white.withOpacity(0.05)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'SURVIVAL PROTOCOL',
                      style: GoogleFonts.spaceGrotesk(
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        letterSpacing: 2,
                        color: const Color(0xFFFF716C),
                      ),
                    ),
                    const SizedBox(height: 16),
                    _protocolItem(Icons.check_circle, 'Locate nearest exit and secure perimeter.'),
                    _protocolItem(Icons.warning, 'Remain in ROOM 412 until verification.', isError: true),
                    _protocolItem(Icons.check_circle, 'Enable device tracking for dispatch.'),
                  ],
                ),
              ),
              const SizedBox(height: 100), // Space for bottom nav
            ],
          ),
        ),
      ),
      bottomNavigationBar: Container(
        height: 80,
        decoration: BoxDecoration(
          color: const Color(0xFF080F18).withOpacity(0.6),
          border: const Border(top: BorderSide(color: Color(0x1A00E5FF), width: 1)),
          boxShadow: [
            BoxShadow(
              color: const Color(0xFF00E5FF).withOpacity(0.1),
              blurRadius: 20,
              offset: const Offset(0, -8),
            ),
          ],
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _navItem(Icons.speed, 'DASHBOARD', isActive: true),
            _navItem(Icons.emergency_share, 'DISPATCH'),
            _navItem(Icons.satellite_alt, 'INTEL'),
            _navItem(Icons.group, 'UNITS'),
          ],
        ),
      ),
    );
  }

  Widget _unitTile(IconData icon, String name, String distance, Color color, {bool isHighlight = false}) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xFF17202C),
        borderRadius: BorderRadius.circular(8),
        border: isHighlight ? Border.all(color: const Color(0xFF00E5FF), width: 1) : null,
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(width: 12),
              Text(
                name,
                style: GoogleFonts.spaceGrotesk(fontWeight: FontWeight.bold, fontSize: 14),
              ),
            ],
          ),
          Text(
            distance,
            style: GoogleFonts.spaceGrotesk(fontSize: 10, color: isHighlight ? color : Colors.blueGrey.shade400),
          ),
        ],
      ),
    );
  }

  Widget _protocolItem(IconData icon, String text, {bool isError = false}) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 16, color: isError ? const Color(0xFFFF716C) : Colors.blueGrey.shade400),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              text,
              style: GoogleFonts.inter(fontSize: 14, color: Colors.blueGrey.shade300),
            ),
          ),
        ],
      ),
    );
  }

  Widget _navItem(IconData icon, String label, {bool isActive = false}) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        if (isActive)
          Container(
            width: 40,
            height: 2,
            margin: const EdgeInsets.only(bottom: 8),
            decoration: const BoxDecoration(
              color: Color(0xFF00E5FF),
              boxShadow: [BoxShadow(color: Color(0xFF00E5FF), blurRadius: 8)],
            ),
          ),
        Icon(icon, color: isActive ? const Color(0xFF00E5FF) : Colors.blueGrey.shade600),
        const SizedBox(height: 4),
        Text(
          label,
          style: GoogleFonts.spaceGrotesk(
            fontSize: 10,
            fontWeight: FontWeight.w500,
            letterSpacing: 2,
            color: isActive ? const Color(0xFF00E5FF) : Colors.blueGrey.shade600,
          ),
        ),
      ],
    );
  }
}
