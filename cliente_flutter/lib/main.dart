import 'dart:convert';

import 'oferta_infantil.dart';
import 'privacidad.dart';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;

const _brand = Color(0xFF7036C4);
const _brandDark = Color(0xFF4C1D95);
const _brandSoft = Color(0xFFEDE9FE);
const _page = Color(0xFFF6F3FC);
const _ink = Color(0xFF19152F);
const _muted = Color(0xFF475569);
const _border = Color(0xFFD9D3E6);

class AlcaldiaData {
  const AlcaldiaData({
    required this.name,
    required this.period,
    required this.total,
    required this.children,
    required this.olderAdults,
    required this.children14,
    required this.source,
    required this.dataType,
  });

  final String name;
  final String period;
  final int total;
  final int children;
  final int olderAdults;
  final String source;
  final String dataType;
  final int children14;

  factory AlcaldiaData.fromJson(Map<String, dynamic> json) => AlcaldiaData(
        name: json['alcaldia'] as String,
        period: json['periodo'] as String,
        total: json['poblacion_total'] as int,
        children: json['poblacion_0_4'] as int,
        olderAdults: json['poblacion_60_mas'] as int,
        children14: json['poblacion_0_14'] as int,
        source: json['fuente'] as String,
        dataType: json['tipo_dato'] as String,
      );
}

Future<List<AlcaldiaData>> _loadAlcaldias() async {
  final raw = await rootBundle.loadString('assets/data/alcaldias.json');
  final decoded = jsonDecode(raw) as List<dynamic>;
  return decoded
      .map((item) => AlcaldiaData.fromJson(item as Map<String, dynamic>))
      .toList(growable: false);
}

const _apiUrl = String.fromEnvironment(
  'OBSERVATORIO_API_URL',
  defaultValue: 'http://127.0.0.1:8000',
);

typedef MatchingExecutor = Future<Map<String, dynamic>> Function({
  required String type,
  required String start,
  required String end,
  required List<String> days,
  required double radiusKm,
});

typedef SimulatorExecutor = Future<Map<String, dynamic>> Function(
  Map<String, dynamic> parameters,
);

void main() => runApp(const ObservatorioApp());

class ObservatorioApp extends StatelessWidget {
  const ObservatorioApp({
    super.key,
    this.matchingExecutor,
    this.simulatorExecutor,
  });
  final MatchingExecutor? matchingExecutor;
  final SimulatorExecutor? simulatorExecutor;

  @override
  Widget build(BuildContext context) {
    final scheme = ColorScheme.fromSeed(
      seedColor: _brand,
      brightness: Brightness.light,
    );
    return MaterialApp(
      title: 'Observatorio del cuidado CDMX',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: scheme.copyWith(
          primary: _brand,
          onPrimary: Colors.white,
          surface: Colors.white,
        ),
        scaffoldBackgroundColor: _page,
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          backgroundColor: _page,
          foregroundColor: _ink,
          elevation: 0,
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: Colors.white,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: _border),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: _border),
          ),
        ),
      ),
      home: ObservatoryShell(
        matchingExecutor: matchingExecutor,
        simulatorExecutor: simulatorExecutor,
      ),
    );
  }
}

class ObservatoryShell extends StatefulWidget {
  const ObservatoryShell({
    super.key,
    this.matchingExecutor,
    this.simulatorExecutor,
  });
  final MatchingExecutor? matchingExecutor;
  final SimulatorExecutor? simulatorExecutor;

  @override
  State<ObservatoryShell> createState() => _ObservatoryShellState();
}

class _ObservatoryShellState extends State<ObservatoryShell> {
  int _selectedIndex = 0;

  static const _destinations = [
    NavigationDestination(key: Key('nav_inicio'), icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Inicio'),
    NavigationDestination(key: Key('nav_mapa'), icon: Icon(Icons.map_outlined), selectedIcon: Icon(Icons.map), label: 'Mapa'),
    NavigationDestination(key: Key('nav_comparar'), icon: Icon(Icons.compare_arrows), label: 'Comparar'),
    NavigationDestination(key: Key('nav_busqueda'), icon: Icon(Icons.search), label: 'Búsqueda'),
    NavigationDestination(key: Key('nav_simuladores'), icon: Icon(Icons.calculate_outlined), label: 'Simuladores'),
    NavigationDestination(key: Key('nav_proyecto'), icon: Icon(Icons.info_outline), selectedIcon: Icon(Icons.info), label: 'Proyecto'),
  ];

  static const _railDestinations = [
    NavigationRailDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: Text('Inicio')),
    NavigationRailDestination(icon: Icon(Icons.map_outlined), selectedIcon: Icon(Icons.map), label: Text('Mapa')),
    NavigationRailDestination(icon: Icon(Icons.compare_arrows), label: Text('Comparar')),
    NavigationRailDestination(icon: Icon(Icons.search), label: Text('Búsqueda demo')),
    NavigationRailDestination(icon: Icon(Icons.calculate_outlined), label: Text('Simuladores')),
    NavigationRailDestination(icon: Icon(Icons.info_outline), selectedIcon: Icon(Icons.info), label: Text('Proyecto')),
  ];

  @override
  Widget build(BuildContext context) {
    final wide = MediaQuery.sizeOf(context).width >= 900;
    final content = IndexedStack(
      index: _selectedIndex,
      children: [
        HomeScreen(onNavigate: (index) => setState(() => _selectedIndex = index)),
        const MapScreen(),
        const CompareScreen(),
        SearchScreen(matchingExecutor: widget.matchingExecutor),
        SimulatorScreen(simulatorExecutor: widget.simulatorExecutor),
        const ProjectScreen(),
      ],
    );
    return Scaffold(
      appBar: AppBar(
        titleSpacing: wide ? 28 : 16,
        title: const _BrandHeader(),
        actions: [PopupMenuButton<String>(
          tooltip: 'Menú de información',
          onSelected: (_) => mostrarPrivacidad(context),
          itemBuilder: (_) => const [PopupMenuItem(value: 'privacidad', child: Text('Privacidad y uso de datos'))],
        )],
      ),
      body: Row(
        children: [
          if (wide)
            NavigationRail(
              selectedIndex: _selectedIndex,
              onDestinationSelected: (index) => setState(() => _selectedIndex = index),
              labelType: NavigationRailLabelType.all,
              backgroundColor: Colors.white,
              leading: const SizedBox(height: 12),
              destinations: _railDestinations,
            ),
          Expanded(child: Center(child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 1180),
            child: content,
          ))),
        ],
      ),
      bottomNavigationBar: wide
          ? null
          : NavigationBar(
              selectedIndex: _selectedIndex,
              onDestinationSelected: (index) => setState(() => _selectedIndex = index),
              destinations: _destinations,
            ),
    );
  }
}

class _BrandHeader extends StatelessWidget {
  const _BrandHeader();

  @override
  Widget build(BuildContext context) => Row(
        children: [
          Container(
            width: 34,
            height: 34,
            decoration: BoxDecoration(color: _brand, borderRadius: BorderRadius.circular(10)),
            child: const Icon(Icons.favorite, color: Colors.white, size: 19),
          ),
          const SizedBox(width: 10),
          const Flexible(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Observatorio del cuidado', style: TextStyle(fontSize: 15, fontWeight: FontWeight.w800)),
                Text('CDMX · demostración académica', style: TextStyle(fontSize: 12, color: _muted, fontWeight: FontWeight.normal)),
              ],
            ),
          ),
        ],
      );
}

class _Page extends StatelessWidget {
  const _Page({required this.kicker, required this.title, required this.child});
  final String kicker;
  final String title;
  final Widget child;

  @override
  Widget build(BuildContext context) => SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(20, 24, 20, 32),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(colors: [_brandDark, _brand]),
                borderRadius: BorderRadius.circular(18),
              ),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(kicker.toUpperCase(), style: const TextStyle(color: Color(0xFFEEE4FF), fontSize: 12, fontWeight: FontWeight.w700, letterSpacing: 1)),
                const SizedBox(height: 4),
                Text(title, style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: Colors.white, fontWeight: FontWeight.w800)),
              ]),
            ),
            const SizedBox(height: 12),
            child,
          ],
        ),
      );
}

class _Card extends StatelessWidget {
  const _Card({required this.child, this.color = const Color(0xFFF0E8FC)});
  final Color color;
  final Widget child;

  @override
  Widget build(BuildContext context) => Card(
        elevation: 0,
        color: color,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: const BorderSide(color: _border)),
        child: Padding(padding: const EdgeInsets.all(16), child: child),
      );
}

class _Notice extends StatelessWidget {
  const _Notice({required this.child});
  final String child;

  @override
  Widget build(BuildContext context) => Container(
        width: double.infinity,
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(color: const Color(0xFFE8F1FA), borderRadius: BorderRadius.circular(14)),
        child: Text(child, style: const TextStyle(color: _ink, height: 1.45)),
      );
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key, required this.onNavigate});
  final ValueChanged<int> onNavigate;

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Observatorio del cuidado',
        title: 'Economía del cuidado en CDMX',
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const _Notice(child: 'Explora los centros de cuidado infantil documentados en las 16 alcaldías. Consulta sus horarios publicados y compara la información disponible.'),
            const SizedBox(height: 16),
            Center(child: Image.asset('assets/portada.webp', width: 480, height: 140, fit: BoxFit.contain, excludeFromSemantics: true)),
            const SizedBox(height: 24),
            _Card(child: Text('¿Qué quieres explorar?', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800, color: _ink))),
            const SizedBox(height: 12),
            LayoutBuilder(builder: (context, constraints) {
              final columns = constraints.maxWidth >= 700 ? 3 : 1;
              return GridView.builder(
                itemCount: 5,
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: columns,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  mainAxisExtent: columns == 1 ? 160 : 140,
                ),
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemBuilder: (context, index) => [
                  _ActionCard(icon: Icons.map_outlined, title: 'Explorar mapa', description: 'Localiza centros y consulta sus horarios.', onTap: () => onNavigate(1)),
                  _ActionCard(icon: Icons.compare_arrows, title: 'Comparar alcaldías', description: 'Compara sedes con horario publicado y grupos de edad.', onTap: () => onNavigate(2)),
                  _ActionCard(icon: Icons.search, title: 'Probar búsqueda', description: 'Recorre un ejemplo demostrativo de búsqueda.', onTap: () => onNavigate(3)),
                  _ActionCard(icon: Icons.calculate_outlined, title: 'Simuladores', description: 'Calcula escenarios B2B/B2G sintéticos.', onTap: () => onNavigate(4)),
                  _ActionCard(icon: Icons.privacy_tip_outlined, title: 'Cómo usamos los datos', description: 'Consulta la privacidad del mapa y el aviso del piloto.', onTap: () => mostrarPrivacidad(context)),
                ][index],
              );
            }),
          ],
        ),
      );
}

class _ActionCard extends StatelessWidget {
  const _ActionCard({required this.icon, required this.title, required this.description, required this.onTap});
  final IconData icon;
  final String title;
  final String description;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) => Semantics(
        button: true,
        label: title,
        child: Material(
          color: Colors.transparent,
          borderRadius: BorderRadius.circular(16),
          clipBehavior: Clip.antiAlias,
          child: InkWell(
            onTap: onTap,
            canRequestFocus: true,
            borderRadius: BorderRadius.circular(16),
            child: _Card(
              color: switch (icon) {
                Icons.map_outlined => const Color(0xFFE1F4EF),
                Icons.compare_arrows => const Color(0xFFF0E8FC),
                Icons.search => const Color(0xFFFFEAD9),
                _ => const Color(0xFFE8F1FA),
              },
              child: Row(
          children: [
            CircleAvatar(backgroundColor: _brandSoft, foregroundColor: _brandDark, child: Icon(icon)),
            const SizedBox(width: 12),
            Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.center, children: [
              Text(title, maxLines: 1, overflow: TextOverflow.ellipsis, style: const TextStyle(fontWeight: FontWeight.w800, color: _ink)),
              const SizedBox(height: 4),
              Text(description, maxLines: 2, overflow: TextOverflow.ellipsis, style: const TextStyle(color: _muted, fontSize: 13, height: 1.3)),
            ])),
          ],
        ),
            ),
          ),
        ),
      );
}

const _alcaldias = ['Álvaro Obregón', 'Azcapotzalco', 'Benito Juárez', 'Coyoacán', 'Cuajimalpa de Morelos', 'Cuauhtémoc', 'Gustavo A. Madero', 'Iztacalco', 'Iztapalapa', 'La Magdalena Contreras', 'Miguel Hidalgo', 'Milpa Alta', 'Tláhuac', 'Tlalpan', 'Venustiano Carranza', 'Xochimilco'];

class MapScreen extends StatefulWidget {
  const MapScreen({super.key, this.dataFuture, this.geometryFuture, this.ofertaFuture});
  final Future<Map<String, Registro>>? ofertaFuture;
  final Future<List<AlcaldiaData>>? dataFuture;
  final Future<String>? geometryFuture;

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  String? _selected;
  late final Future<List<AlcaldiaData>> _dataFuture;
  late final Future<String> _geometryFuture;
  late final _oferta = widget.ofertaFuture ?? cargarOfertaInfantil();

  @override
  void initState() {
    super.initState();
    _dataFuture = widget.dataFuture ?? _loadAlcaldias();
    _geometryFuture = widget.geometryFuture ?? rootBundle.loadString('assets/data/alcaldias.geojson');
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<AlcaldiaData>>(
        future: _dataFuture,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return const _Page(
              kicker: 'Explorador territorial',
              title: 'No se pudieron cargar los datos',
              child: _Notice(
                child: 'El archivo territorial estático no está disponible. '
                    'La aplicación no ejecuta ETL ni descarga datos durante la visita.',
              ),
            );
          }
          if (!snapshot.hasData) {
            return _renderMap(context, const []);
          }
          return _renderMap(context, snapshot.data!);
        },
      );
  }

  Widget _renderMap(BuildContext context, List<AlcaldiaData> data) {
    AlcaldiaData? selectedData;
    for (final item in data) {
      if (item.name == _selected) {
        selectedData = item;
        break;
      }
    }
    return _Page(
        kicker: 'Explorador territorial',
        title: 'Explora tu alcaldía',
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const _Notice(child: 'Elige una alcaldía. Los puntos representan sedes reales de cuidado. Las cifras de población son indicadores agregados por alcaldía.'),
            const SizedBox(height: 14),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              key: ValueKey(_selected),
              isExpanded: true,
              initialValue: _selected,
              decoration: const InputDecoration(labelText: 'Alcaldía'),
              hint: const Text('Selecciona una alcaldía'),
              items: _alcaldias.map((name) => DropdownMenuItem(value: name, child: Text(name))).toList(),
              onChanged: (value) => setState(() => _selected = value),
            ),
            const SizedBox(height: 16),
            FutureBuilder<String>(
              future: _geometryFuture,
              builder: (context, geometrySnapshot) {
                if (geometrySnapshot.hasError) {
                  return const _Notice(
                    child: 'No se pudo cargar la cartografía. Puedes seguir consultando las 16 alcaldías mediante la lista.',
                  );
                }
                if (!geometrySnapshot.hasData) {
                  return const _Card(
                    child: Center(child: Text('Cargando cartografía territorial...')),
                  );
                }
                return FutureBuilder<Map<String, Registro>>(
                  future: _oferta,
                  builder: (context, oferta) {
                    final puntos = <Offset>[];
                    for (final grupo in oferta.data?.values ?? <Registro>[]) {
                      if (_selected != null && grupo['nombre'] != _selected) continue;
                      for (final sede in grupo['sedes']) {
                        final p = sede['punto'];
                        if (p != null) puntos.add(Offset(p[1], p[0]));
                      }
                    }
                    return _TerritorialMap(
                  puntos: puntos,
                  geoJson: geometrySnapshot.data!,
                  selected: _selected,
                  onSelected: (value) => setState(() => _selected = value),
                  onReset: () => setState(() => _selected = null),
                );
                  },
                );
              },
            ),
            const SizedBox(height: 10),
            OutlinedButton.icon(
              onPressed: () => setState(() => _selected = null),
              icon: const Icon(Icons.location_on_outlined),
              label: const Text('Ver toda CDMX'),
            ),
            FutureBuilder<Map<String, Registro>>(
              future: _oferta,
              builder: (context, snapshot) {
                if (snapshot.hasError) return const Text('Directorio infantil no disponible.');
                if (!snapshot.hasData) return const Text('Cargando directorio infantil…');
                final grupos = snapshot.data!.values.where((g) =>
                    _selected == null || g['nombre'] == _selected).toList();
                return OfertaInfantil(key: ValueKey(_selected), grupos: grupos, alcaldia: _selected);
              },
            ),
            if (selectedData != null) ...[
              const SizedBox(height: 20),
              _Card(child: Text('Datos de ${selectedData.name}', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800, color: _ink))),
              _Card(child: Text('${selectedData.source} · periodo ${selectedData.period} · ${selectedData.dataType}', style: const TextStyle(color: _muted, fontSize: 13))),
              const SizedBox(height: 12),
              Wrap(spacing: 10, runSpacing: 10, children: [
                _Metric(title: 'Población total', value: '${selectedData.total}', note: 'Personas registradas'),
                _Metric(title: '0 a 4 años', value: '${selectedData.children}', note: 'Intervalo exacto'),
                _Metric(title: '60 años o más', value: '${selectedData.olderAdults}', note: 'Suma de grupos'),
              ]),
              const SizedBox(height: 16),
              ExpansionTile(title: const Text('Población por grupos de edad'), children: [_AgeBars(data: selectedData)]),
              const SizedBox(height: 12),
              const _Card(child: Text('Los conteos describen población registrada y no prueban necesidad de cuidado, demanda efectiva ni impacto social.', style: TextStyle(color: _muted, height: 1.4))),
            ],
          ],
        ),
      );
  }
}

class _GeoFeature {
  const _GeoFeature({required this.key, required this.name, required this.rings});
  final String key;
  final String name;
  final List<List<Offset>> rings;
}

class _TerritorialMap extends StatefulWidget {
  const _TerritorialMap({
    required this.puntos,
    required this.geoJson,
    required this.selected,
    required this.onSelected,
    required this.onReset,
  });

  final List<Offset> puntos;
  final String geoJson;
  final String? selected;
  final ValueChanged<String> onSelected;
  final VoidCallback onReset;

  @override
  State<_TerritorialMap> createState() => _TerritorialMapState();
}

class _TerritorialMapState extends State<_TerritorialMap> {
  List<_GeoFeature> _features = const [];
  String? _error;
  final GlobalKey _mapKey = GlobalKey();

  @override
  void initState() {
    super.initState();
    try {
      _features = _parseGeoJson(widget.geoJson);
      if (_features.length != 16) {
        throw const FormatException('Se esperaban 16 geometrías');
      }
    } catch (_) {
      _error = 'La cartografía no pudo interpretarse.';
    }
  }

  List<_GeoFeature> _parseGeoJson(String raw) {
    final decoded = jsonDecode(raw) as Map<String, dynamic>;
    final features = decoded['features'] as List<dynamic>;
    final result = <_GeoFeature>[];
    for (final item in features) {
      final map = item as Map<String, dynamic>;
      final properties = map['properties'] as Map<String, dynamic>;
      final geometry = map['geometry'] as Map<String, dynamic>;
      final rings = <List<Offset>>[];
      if (geometry['type'] == 'Polygon') {
        for (final ring in geometry['coordinates'] as List<dynamic>) {
          rings.add(_parseRing(ring as List<dynamic>));
        }
      } else if (geometry['type'] == 'MultiPolygon') {
        for (final polygon in geometry['coordinates'] as List<dynamic>) {
          for (final ring in polygon as List<dynamic>) {
            rings.add(_parseRing(ring as List<dynamic>));
          }
        }
      }
      if (rings.isEmpty) continue;
      result.add(_GeoFeature(
        key: properties['clave'] as String,
        name: properties['alcaldia'] as String,
        rings: rings,
      ));
    }
    return result;
  }

  List<Offset> _parseRing(List<dynamic> ring) => ring
      .map((point) {
        final coordinates = point as List<dynamic>;
        return Offset((coordinates[0] as num).toDouble(), (coordinates[1] as num).toDouble());
      })
      .toList(growable: false);

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return _Notice(child: '$_error Puedes seguir consultando por la lista.');
    }
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          height: 250,
          width: double.infinity,
          clipBehavior: Clip.antiAlias,
          decoration: BoxDecoration(
            color: _brandSoft,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: _border),
          ),
          child: GestureDetector(
            key: _mapKey,
            behavior: HitTestBehavior.opaque,
            onTapUp: (details) => _selectAt(details.localPosition),
            child: Semantics(
              label: 'Mapa territorial de las 16 alcaldías',
              button: true,
              child: CustomPaint(
                painter: _AlcaldiaPainter(features: _features, selected: widget.selected, puntos: widget.puntos),
                child: const SizedBox.expand(),
              ),
            ),
          ),
        ),
        const SizedBox(height: 10),
      ],
    );
  }

  void _selectAt(Offset local) {
    final bounds = _MapBounds.fromFeatures(_features);
    final renderBox = _mapKey.currentContext?.findRenderObject() as RenderBox?;
    if (renderBox == null) return;
    final mapping = _MapMapping.fromBounds(bounds, renderBox.size, const EdgeInsets.all(14));
    final geo = mapping.toGeo(local);
    for (final feature in _features) {
      if (feature.rings.any((ring) => _pointInPolygon(geo, ring))) {
        widget.onSelected(feature.name);
        return;
      }
    }
  }

  bool _pointInPolygon(Offset point, List<Offset> ring) {
    var inside = false;
    for (var i = 0, j = ring.length - 1; i < ring.length; j = i++) {
      final a = ring[i];
      final b = ring[j];
      final intersect = ((a.dy > point.dy) != (b.dy > point.dy)) &&
          (point.dx < (b.dx - a.dx) * (point.dy - a.dy) / ((b.dy - a.dy) == 0 ? 1 : b.dy - a.dy) + a.dx);
      if (intersect) inside = !inside;
    }
    return inside;
  }
}

class _MapBounds {
  const _MapBounds(this.minX, this.minY, this.maxX, this.maxY);
  final double minX;
  final double minY;
  final double maxX;
  final double maxY;

  static _MapBounds fromFeatures(List<_GeoFeature> features) {
    var minX = double.infinity;
    var minY = double.infinity;
    var maxX = -double.infinity;
    var maxY = -double.infinity;
    for (final feature in features) {
      for (final ring in feature.rings) {
        for (final point in ring) {
          if (point.dx < minX) minX = point.dx;
          if (point.dy < minY) minY = point.dy;
          if (point.dx > maxX) maxX = point.dx;
          if (point.dy > maxY) maxY = point.dy;
        }
      }
    }
    return _MapBounds(minX, minY, maxX, maxY);
  }
}

class _MapMapping {
  const _MapMapping(this.left, this.top, this.scaleX, this.scaleY, this.bounds);
  final double left;
  final double top;
  final double scaleX;
  final double scaleY;
  final _MapBounds bounds;

  static _MapMapping fromBounds(_MapBounds bounds, Size size, EdgeInsets padding) {
    final width = size.width - padding.horizontal;
    final height = size.height - padding.vertical;
    final geoWidth = bounds.maxX - bounds.minX;
    final geoHeight = bounds.maxY - bounds.minY;
    final scale = (width / geoWidth) < (height / geoHeight)
        ? width / geoWidth
        : height / geoHeight;
    final drawnWidth = geoWidth * scale;
    final drawnHeight = geoHeight * scale;
    return _MapMapping(
      padding.left + (width - drawnWidth) / 2,
      padding.top + (height - drawnHeight) / 2,
      scale,
      scale,
      bounds,
    );
  }

  Offset toCanvas(Offset geo) => Offset(
        left + (geo.dx - bounds.minX) * scaleX,
        top + (bounds.maxY - geo.dy) * scaleY,
      );

  Offset toGeo(Offset canvas) => Offset(
        bounds.minX + (canvas.dx - left) / scaleX,
        bounds.maxY - (canvas.dy - top) / scaleY,
      );
}

class _AlcaldiaPainter extends CustomPainter {
  const _AlcaldiaPainter({required this.features, required this.selected, required this.puntos});
  final List<Offset> puntos;
  final List<_GeoFeature> features;
  final String? selected;

  @override
  void paint(Canvas canvas, Size size) {
    final bounds = _MapBounds.fromFeatures(features);
    final mapping = _MapMapping.fromBounds(bounds, size, const EdgeInsets.all(14));
    for (final feature in features) {
      final isSelected = feature.name == selected;
      final paint = Paint()
        ..color = isSelected ? _brand : const Color(0xFFD7C5F0)
        ..style = PaintingStyle.fill;
      final border = Paint()
        ..color = isSelected ? _brandDark : const Color(0xFF9A86C7)
        ..strokeWidth = isSelected ? 2.5 : 1
        ..style = PaintingStyle.stroke;
      for (final ring in feature.rings) {
        if (ring.length < 3) continue;
        final path = Path();
        final first = mapping.toCanvas(ring.first);
        path.moveTo(first.dx, first.dy);
        for (final point in ring.skip(1)) {
          final canvasPoint = mapping.toCanvas(point);
          path.lineTo(canvasPoint.dx, canvasPoint.dy);
        }
        path.close();
        canvas.drawPath(path, paint);
        canvas.drawPath(path, border);
      }
    }
    final halo = Paint()..color = Colors.white;
    final marcador = Paint()..color = const Color(0xFF075E55);
    for (final punto in puntos) {
      final centro = mapping.toCanvas(punto);
      canvas.drawCircle(centro, 3.2, halo);
      canvas.drawCircle(centro, 2.2, marcador);
    }
  }

  @override
  bool shouldRepaint(covariant _AlcaldiaPainter oldDelegate) =>
      oldDelegate.selected != selected || oldDelegate.features != features || oldDelegate.puntos != puntos;
}

class _Metric extends StatelessWidget {
  const _Metric({required this.title, required this.value, required this.note});
  final String title;
  final String value;
  final String note;

  @override
  Widget build(BuildContext context) => SizedBox(
        width: 210,
        child: _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title, style: const TextStyle(color: _muted, fontWeight: FontWeight.w600)),
          const SizedBox(height: 8),
          Text(value, style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: _ink, fontWeight: FontWeight.w800)),
          Text(note, style: const TextStyle(color: _muted, fontSize: 12)),
        ])),
      );
}

class _AgeBars extends StatelessWidget {
  const _AgeBars({required this.data});
  final AlcaldiaData data;

  @override
  Widget build(BuildContext context) => Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Población por grupos de edad', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800, color: _ink)),
        const SizedBox(height: 4),
        const Text('Conteos observados del archivo territorial estático.', style: TextStyle(color: _muted, fontSize: 13)),
        const SizedBox(height: 14),
        for (final item in [
          ('0–4 años', data.children / data.total),
          ('5–59 años', (data.total - data.children - data.olderAdults) / data.total),
          ('60 años o más', data.olderAdults / data.total),
        ])
          Padding(padding: const EdgeInsets.only(bottom: 10), child: Row(children: [
            SizedBox(width: 105, child: Text(item.$1, style: const TextStyle(color: _muted, fontSize: 13))),
            Expanded(child: LinearProgressIndicator(value: item.$2, minHeight: 12, borderRadius: BorderRadius.circular(8), color: _brand, backgroundColor: _brandSoft)),
          ])),
      ]);
}

class CompareScreen extends StatefulWidget {
  const CompareScreen({super.key, this.dataFuture, this.ofertaFuture});
  final Future<Map<String, Registro>>? ofertaFuture;
  final Future<List<AlcaldiaData>>? dataFuture;

  @override
  State<CompareScreen> createState() => _CompareScreenState();
}

class _CompareScreenState extends State<CompareScreen> {
  late final _oferta = widget.ofertaFuture ?? cargarOfertaInfantil();
  String _a = 'Iztapalapa';
  String _b = 'Benito Juárez';
  late final Future<List<AlcaldiaData>> _dataFuture =
      widget.dataFuture ?? _loadAlcaldias();

  @override
  Widget build(BuildContext context) => FutureBuilder<List<AlcaldiaData>>(
        future: _dataFuture,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return const _Page(
              kicker: 'Comparación territorial',
              title: 'No se pudieron cargar los datos',
              child: _Notice(child: 'La comparación requiere el archivo territorial preparado. No se calculan valores de sustitución.'),
            );
          }
          if (!snapshot.hasData) {
            return const _Page(
              kicker: 'Comparación territorial',
              title: 'Compara dos alcaldías',
              child: Center(child: Text('Cargando datos preparados...')),
            );
          }
          return _render(context, snapshot.data!);
        },
      );

  double? _ratio(List<AlcaldiaData> data, String name, String group) {
    for (final item in data) {
      if (item.name == name) {
        if (item.total == 0) return null;
        final value = group == '60+' ? item.olderAdults : item.children14;
        return value / item.total;
      }
    }
    return null;
  }

  Widget _render(BuildContext context, List<AlcaldiaData> data) => _Page(
        kicker: 'Comparación territorial',
        title: 'Compara dos alcaldías',
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _Notice(child: 'Sedes con horario publicado indica qué proporción de centros documentó su horario. La disponibilidad de lugares requiere información de vacantes con fecha.'),
          const SizedBox(height: 16),
          LayoutBuilder(builder: (context, constraints) {
            final vertical = constraints.maxWidth < 560;
            final fields = [
              DropdownButtonFormField<String>(initialValue: _a, isExpanded: true, isDense: true, decoration: const InputDecoration(labelText: 'Alcaldía A', isDense: true, contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 10)), items: _alcaldias.map((x) => DropdownMenuItem(value: x, child: Text(x))).toList(), onChanged: (x) { if (x != null) setState(() { if (_b == x) _b = _a; _a = x; }); }),
              DropdownButtonFormField<String>(initialValue: _b, isExpanded: true, isDense: true, decoration: const InputDecoration(labelText: 'Alcaldía B', isDense: true, contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 10)), items: _alcaldias.where((x) => x != _a).map((x) => DropdownMenuItem(value: x, child: Text(x))).toList(), onChanged: (x) { if (x != null) setState(() => _b = x); }),
            ];
            return vertical ? Column(children: [fields[0], const SizedBox(height: 12), fields[1]]) : Row(children: [Expanded(child: fields[0]), const SizedBox(width: 12), Expanded(child: fields[1])]);
          }),
          const SizedBox(height: 20),
          FutureBuilder<Map<String, Registro>>(
            future: _oferta,
            builder: (context, snapshot) {
              if (snapshot.hasError) return const Text('Directorio infantil no disponible.');
              if (!snapshot.hasData) return const Text('Cargando directorio infantil.');
              final grupos = {for (final g in snapshot.data!.values) g['nombre']: g};
              final par = [_a, _b];
              if (par.any((nombre) => (grupos[nombre]?['resumen']['sedes_unicas'] ?? 0) == 0)) {
                return const Text('Falta información del directorio para comparar este par.');
              }
              return _Card(color: const Color(0xFFE1F4EF), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Centros con horario publicado', style: Theme.of(context).textTheme.titleMedium),
                for (final nombre in par)
                  ResumenHorario(nombre: nombre, sedes: grupos[nombre]!['resumen']['sedes_unicas'], horario: grupos[nombre]!['resumen']['con_horario']),
                ExpansionTile(
                  title: const Text('Fuentes de los horarios'),
                  children: [
                    const Text('Cada porcentaje usa todas las sedes documentadas de su alcaldía. El horario corresponde al periodo publicado por cada fuente.'),
                    for (final nombre in par)
                      ListTile(title: Text(nombre), subtitle: SelectableText(
                        ({
                          for (final sede in grupos[nombre]!['sedes'])
                            for (final unidad in sede['unidades'])
                              if (unidad['apertura'] != null)
                                "${unidad['red']} · ${unidad['periodo_horario']}\n${unidad['fuente_url']}",
                        }.toList()..sort()).join('\n\n'),
                      )),
                  ],
                ),
              ]));
            },
          ),
          const SizedBox(height: 12),
          _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Composición demográfica', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800, color: _ink)),
            const SizedBox(height: 4),
            const Text('Personas por cada 100 habitantes · Censo 2020 observado', style: TextStyle(color: _muted, fontSize: 13)),
            const SizedBox(height: 16),
            _ComparisonRow(label: '0 a 14 años', first: _a, firstValue: _ratio(data, _a, '0-14'), second: _b, secondValue: _ratio(data, _b, '0-14')),
            _ComparisonRow(label: '60 años o más', first: _a, firstValue: _ratio(data, _a, '60+'), second: _b, secondValue: _ratio(data, _b, '60+')),
          ])),
          const SizedBox(height: 12),
          const _Notice(child: 'Fuente: INEGI, Censo 2020, ITER. Las proporciones son descriptivas y no constituyen una evaluación de impacto.'),
        ]),
      );
}

class _ComparisonRow extends StatelessWidget {
  const _ComparisonRow({required this.label, required this.first, required this.firstValue, required this.second, required this.secondValue});
  final String label;
  final String first;
  final double? firstValue;
  final String second;
  final double? secondValue;

  @override
  Widget build(BuildContext context) => Padding(padding: const EdgeInsets.only(bottom: 16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.w700, color: _ink)),
        const SizedBox(height: 8),
        if (firstValue != null && secondValue != null) ...[
          _BarLabel(name: first, value: firstValue!),
          _BarLabel(name: second, value: secondValue!, color: const Color(0xFFA78BFA)),
        ] else
          const Text('Sin datos comparables para este par.'),
      ]));
}

class _BarLabel extends StatelessWidget {
  const _BarLabel({required this.name, required this.value, this.color = _brand});
  final String name;
  final double value;
  final Color color;

  @override
  Widget build(BuildContext context) => Row(children: [
        SizedBox(width: 125, child: Text(name, overflow: TextOverflow.ellipsis, style: const TextStyle(color: _muted, fontSize: 12))),
        Expanded(child: LinearProgressIndicator(value: value, minHeight: 10, borderRadius: BorderRadius.circular(8), color: color, backgroundColor: _brandSoft)),
        const SizedBox(width: 8),
        Text('${(value * 100).round()}%', style: const TextStyle(fontWeight: FontWeight.w700, color: _ink)),
      ]);
}

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key, this.apiUrl = _apiUrl, this.matchingExecutor});
  final String apiUrl;
  final MatchingExecutor? matchingExecutor;

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  int _step = 0;
  String _type = 'Cuidado infantil';
  bool _searched = false;
  bool _loading = false;
  String? _error;
  List<dynamic> _results = const [];

  Future<void> _executeSearch() async {
    setState(() {
      _loading = true;
      _error = null;
      _searched = true;
      _step = 3;
    });
    try {
      final type = _type == 'Cuidado infantil' ? 'infantil' : 'mayores';
      final body = widget.matchingExecutor != null
          ? await widget.matchingExecutor!(
              type: type,
              start: '09:00',
              end: '12:00',
              days: const ['lun', 'mar'],
              radiusKm: 10,
            )
          : await _fetchMatching(type);
      if (!mounted) return;
      setState(() {
        _results = body['results'] as List<dynamic>;
        _loading = false;
      });
    } catch (exc) {
      if (!mounted) return;
      setState(() {
        _error = 'No se pudo consultar el matching. ${exc.toString()}';
        _loading = false;
      });
    }
  }

  Future<Map<String, dynamic>> _fetchMatching(String type) async {
    final response = await http.post(
      Uri.parse('${widget.apiUrl}/api/matching'),
      headers: const {'Content-Type': 'application/json'},
      body: jsonEncode({
        'tipo': type,
        'inicio': '09:00',
        'fin': '12:00',
        'dias': ['lun', 'mar'],
        'radio_km': 10,
      }),
    );
    if (response.statusCode != 200) {
      throw Exception('El servicio respondió con código ${response.statusCode}');
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Exploración guiada · demostración',
        title: 'Búsqueda demostrativa de cuidado',
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _Notice(child: 'Elige el tipo de servicio. El ejemplo compara días, horarios y distancia con una oferta simulada.'),
          const SizedBox(height: 14),
          const _Notice(child: 'Resultado simulado. No confirma disponibilidad ni genera una solicitud o reserva.'),
          const SizedBox(height: 18),
          LinearProgressIndicator(value: (_step + 1) / 4, minHeight: 8, borderRadius: BorderRadius.circular(8), color: _brand, backgroundColor: _brandSoft),
          const SizedBox(height: 8),
          _Card(child: Text('Paso ${_step + 1} de 4 · ${['Servicio', 'Horario', 'Distancia', 'Resultados'][_step]}', style: const TextStyle(color: _muted, fontWeight: FontWeight.w600))),
          const SizedBox(height: 16),
          if (_step == 0) DropdownButtonFormField<String>(isExpanded: true, initialValue: _type, decoration: const InputDecoration(labelText: '¿Qué tipo de cuidado buscas?'), items: const [DropdownMenuItem(value: 'Cuidado infantil', child: Text('Cuidado infantil')), DropdownMenuItem(value: 'Cuidado para personas mayores', child: Text('Cuidado para personas mayores'))], onChanged: (value) { if (value != null) setState(() => _type = value); }),
          if (_step == 1) const _Card(child: Text('Lunes y martes · 09:00 a 12:00', style: TextStyle(color: _ink, fontWeight: FontWeight.w700))),
          if (_step == 2) const _Card(child: Text('Distancia máxima aproximada: 10 km', style: TextStyle(color: _ink, fontWeight: FontWeight.w700))),
          if (_step == 3) _MatchingResult(
            loading: _loading,
            error: _error,
            results: _results,
            onRetry: _executeSearch,
          ),
          const SizedBox(height: 18),
          Wrap(spacing: 10, runSpacing: 10, children: [
            if (_step > 0) OutlinedButton(onPressed: () => setState(() => _step--), child: const Text('Atrás')),
            if (_step > 0 || _searched) OutlinedButton(
              onPressed: () => setState(() {
                _step = 0;
                _type = 'Cuidado infantil';
                _searched = false;
                _error = null;
                _results = const [];
              }),
              child: const Text('Restablecer'),
            ),
            FilledButton(onPressed: () => setState(() {
              if (_step == 2) {
                _executeSearch();
              } else if (_step < 3) {
                _step++;
              } else {
                _searched = true;
              }
            }), child: Text(_step == 2 ? 'Ver resultados' : _step == 3 ? 'Actualizar resultados' : 'Continuar')),
          ]),
        ]),
      );
}

class _MatchingResult extends StatelessWidget {
  const _MatchingResult({
    required this.loading,
    required this.error,
    required this.results,
    required this.onRetry,
  });
  final bool loading;
  final String? error;
  final List<dynamic> results;
  final VoidCallback onRetry;

  static const reasons = {
    'compatible': 'Servicio, horario, días, distancia y cupo son compatibles.',
    'sin_servicio_compatible': 'No hay un servicio sintético de este tipo.',
    'sin_compatibilidad_horaria': 'La franja solicitada no coincide con la oferta.',
    'fuera_de_radio': 'La oferta compatible está fuera de la distancia elegida.',
    'sin_cupo': 'La oferta compatible no tiene cupo sintético disponible.',
  };

  @override
  Widget build(BuildContext context) {
    if (loading) {
      return const _Card(
        child: Column(children: [
          CircularProgressIndicator(),
          SizedBox(height: 12),
          Text('Consultando el motor de matching sintético...'),
        ]),
      );
    }
    if (error != null) {
      return _Card(
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('No se pudo obtener el resultado', style: TextStyle(fontWeight: FontWeight.w800)),
          const SizedBox(height: 8),
          Text(error!, style: const TextStyle(color: _muted)),
          const SizedBox(height: 12),
          OutlinedButton(onPressed: onRetry, child: const Text('Reintentar')),
        ]),
      );
    }
    if (results.isEmpty) {
      return const _Notice(child: 'No hubo solicitudes ni resultados para mostrar.');
    }
    return Column(
      children: [
        for (final raw in results.take(5))
          _Card(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              Text(raw['estado'] == 'recomendada'
                  ? 'Recomendación sintética'
                  : 'Sin compatibilidad en esta demostración'),
              const SizedBox(height: 6),
              Text(reasons[raw['motivo']] ?? 'Motivo no disponible',
                  style: const TextStyle(color: _muted)),
              if (raw['distancia_km'] != null)
                Text('Distancia geográfica: ${raw['distancia_km']} km',
                    style: const TextStyle(color: _muted, fontSize: 13)),
            ]),
          ),
      ],
    );
  }
}

class SimulatorScreen extends StatefulWidget {
  const SimulatorScreen({super.key, this.apiUrl = _apiUrl, this.simulatorExecutor});
  final String apiUrl;
  final SimulatorExecutor? simulatorExecutor;

  @override
  State<SimulatorScreen> createState() => _SimulatorScreenState();
}

class _SimulatorScreenState extends State<SimulatorScreen> {
  int _employees = 100;
  double _salary = 12000;
  double _leavers = 10;
  double _rotationReduction = 20;
  double _costIntervention = 0;
  bool _hasInterventionCost = false;
  bool _loading = false;
  String? _error;
  Map<String, dynamic>? _result;

  Future<void> _calculate() async {
    setState(() {
      _loading = true;
      _error = null;
      _result = null;
    });
    try {
      final parameters = {
        'numero_empleadas': _employees,
        'salario_promedio': _salary,
        'bajas_anuales': _leavers,
        'reduccion_rotacion_pct': _rotationReduction,
        'costo_reclutamiento': 6000,
        'costo_capacitacion': 4500,
        'costo_vacante_productividad': 16800,
        'costo_admin_transferencia': 3500,
        'dias_cotizados': 365,
        'factor_integracion_sbc': 1.049315,
        'tasa_imss_patronal': 0.204,
        'tasa_isn_cdmx': 0.04,
        'tasa_infonavit': 0.05,
        'costo_intervencion': _hasInterventionCost ? _costIntervention : null,
      };
      final body = widget.simulatorExecutor != null
          ? await widget.simulatorExecutor!(parameters)
          : await _fetchSimulator(parameters);
      if (!mounted) return;
      setState(() {
        _result = body;
        _loading = false;
      });
    } catch (exc) {
      if (!mounted) return;
      setState(() {
        _error = 'No se pudo calcular el escenario. ${exc.toString()}';
        _loading = false;
      });
    }
  }

  Future<Map<String, dynamic>> _fetchSimulator(
    Map<String, dynamic> parameters,
  ) async {
    final response = await http.post(
      Uri.parse('${widget.apiUrl}/api/simular'),
      headers: const {'Content-Type': 'application/json'},
      body: jsonEncode(parameters),
    );
    if (response.statusCode != 200) {
      throw Exception('El servicio respondió con código ${response.statusCode}');
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Escenarios sintéticos',
        title: 'Simuladores B2B y B2G',
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _Notice(child: 'Usa cifras hipotéticas o agregadas de la empresa. Estos resultados son ilustrativos. No estiman impacto observado ni beneficio neto sin costo de intervención.'),
          const SizedBox(height: 16),
          DropdownButtonFormField<int>(
            initialValue: _employees,
            isExpanded: true,
            decoration: const InputDecoration(labelText: 'Número de empleadas'),
            items: const [
              DropdownMenuItem(value: 50, child: Text('50 empleadas')),
              DropdownMenuItem(value: 100, child: Text('100 empleadas')),
              DropdownMenuItem(value: 200, child: Text('200 empleadas')),
            ],
            onChanged: (value) => setState(() => _employees = value ?? _employees),
          ),
          const SizedBox(height: 12),
          TextFormField(
            initialValue: _salary.toStringAsFixed(0),
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: 'Salario promedio mensual (MXN)'),
            onChanged: (value) => _salary = double.tryParse(value) ?? _salary,
          ),
          const SizedBox(height: 12),
          TextFormField(
            initialValue: _leavers.toStringAsFixed(0),
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: 'Bajas anuales'),
            onChanged: (value) => _leavers = double.tryParse(value) ?? _leavers,
          ),
          const SizedBox(height: 12),
          TextFormField(
            initialValue: _rotationReduction.toStringAsFixed(0),
            keyboardType: TextInputType.number,
            decoration: const InputDecoration(labelText: 'Reducción de rotación (%)'),
            onChanged: (value) => _rotationReduction = double.tryParse(value) ?? _rotationReduction,
          ),
          const SizedBox(height: 12),
          SwitchListTile(
            contentPadding: EdgeInsets.zero,
            title: const Text('Tengo costo de intervención'),
            value: _hasInterventionCost,
            onChanged: (value) => setState(() => _hasInterventionCost = value),
          ),
          if (_hasInterventionCost)
            TextFormField(
              initialValue: _costIntervention.toStringAsFixed(0),
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: 'Costo de intervención (MXN)'),
              onChanged: (value) => _costIntervention = double.tryParse(value) ?? _costIntervention,
            ),
          const SizedBox(height: 16),
          FilledButton.icon(
            onPressed: _loading ? null : _calculate,
            icon: const Icon(Icons.calculate),
            label: Text(_loading ? 'Calculando...' : 'Calcular escenario'),
          ),
          if (_loading) const Padding(padding: EdgeInsets.only(top: 16), child: LinearProgressIndicator()),
          if (_error != null) ...[
            const SizedBox(height: 16),
            _Notice(child: _error!),
            OutlinedButton(onPressed: _calculate, child: const Text('Reintentar')),
          ],
          if (_result != null) ...[
            const SizedBox(height: 16),
            _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('Ahorro bruto B2B', style: TextStyle(fontWeight: FontWeight.w800)),
              Text('${(_result!['b2b']['ahorro_bruto'] as num).toStringAsFixed(2)} MXN'),
              const SizedBox(height: 8),
              Text(
                _result!['b2b']['beneficio_neto'] == null
                    ? 'Beneficio neto: no calculable sin costo de intervención'
                    : 'Beneficio neto: ${(_result!['b2b']['beneficio_neto'] as num).toStringAsFixed(2)} MXN',
              ),
            ])),
            const SizedBox(height: 12),
            _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('Flujos públicos B2G', style: TextStyle(fontWeight: FontWeight.w800)),
              Text('ISN — impuesto: ${(_result!['b2g']['isn_impuesto'] as num).toStringAsFixed(2)} MXN'),
              Text('IMSS — aportación: ${(_result!['b2g']['imss_patronal'] as num).toStringAsFixed(2)} MXN'),
              Text('INFONAVIT — aportación: ${(_result!['b2g']['infonavit_aportacion'] as num).toStringAsFixed(2)} MXN'),
            ])),
          ],
        ]),
      );
}

class ProjectScreen extends StatelessWidget {
  const ProjectScreen({super.key});

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Sobre este proyecto',
        title: 'Información del proyecto',
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _Notice(child: 'Una lectura breve del propósito, alcance y límites del observatorio.'),
          const SizedBox(height: 16),
          LayoutBuilder(builder: (context, constraints) {
            final columns = constraints.maxWidth >= 700 ? 3 : 1;
            return GridView.builder(
              itemCount: 3,
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: columns,
                crossAxisSpacing: 12,
                mainAxisSpacing: 12,
                mainAxisExtent: columns == 1 ? 116 : 140,
              ),
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemBuilder: (context, index) => const [
                _InfoCard(title: 'Para qué sirve', text: 'Convertir datos de cuidado en evidencia para decisiones y explorar la vinculación con centros comunitarios.'),
                _InfoCard(title: 'Qué puedes hacer', text: 'Consultar indicadores, comparar zonas, ejecutar matching sintético y calcular escenarios B2B/B2G.'),
                _InfoCard(title: 'Qué sigue siendo demostrativo', text: 'Las ofertas y escenarios no representan plazas, centros verificados ni impacto observado.'),
              ][index],
            );
          }),
          const SizedBox(height: 20),
          const _Card(child: Text('Fuentes y metodología', style: TextStyle(fontSize: 19, fontWeight: FontWeight.w800, color: _ink))),
          const SizedBox(height: 8),
          const _Card(child: Text('Se conservan fuentes tabulares y cartográficas del repositorio. ENUT describe CDMX; la distribución proporcional por alcaldía es exploratoria. Flutter usa una API mínima para matching y simuladores; si el backend no está disponible, conserva la consulta territorial local.', style: TextStyle(color: _muted, height: 1.45))),
          const SizedBox(height: 16),
          const _Card(child: Text('Limitaciones esenciales', style: TextStyle(fontSize: 19, fontWeight: FontWeight.w800, color: _ink))),
          const SizedBox(height: 8),
          const _Notice(child: 'La infraestructura contabilizada no demuestra cupos disponibles; distancia geográfica no es tiempo de viaje; la estimación territorial no mide abandono laboral ni causalidad. La consulta del mapa no exige un registro familiar.'),
        ]),
      );
}

class _InfoCard extends StatelessWidget {
  const _InfoCard({required this.title, required this.text});
  final String title;
  final String text;

  @override
  Widget build(BuildContext context) => _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, mainAxisAlignment: MainAxisAlignment.center, children: [
        Text(title, style: const TextStyle(fontWeight: FontWeight.w800, color: _ink)),
        const SizedBox(height: 8),
        Text(text, style: const TextStyle(color: _muted, fontSize: 13, height: 1.35)),
      ]));
}
