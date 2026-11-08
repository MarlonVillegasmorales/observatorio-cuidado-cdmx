import 'package:flutter/material.dart';

const _brand = Color(0xFF6D28D9);
const _brandDark = Color(0xFF4C1D95);
const _brandSoft = Color(0xFFEDE9FE);
const _page = Color(0xFFF8FAFC);
const _ink = Color(0xFF172033);
const _muted = Color(0xFF475569);
const _border = Color(0xFFCBD5E1);

void main() => runApp(const ObservatorioApp());

class ObservatorioApp extends StatelessWidget {
  const ObservatorioApp({super.key});

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
      home: const ObservatoryShell(),
    );
  }
}

class ObservatoryShell extends StatefulWidget {
  const ObservatoryShell({super.key});

  @override
  State<ObservatoryShell> createState() => _ObservatoryShellState();
}

class _ObservatoryShellState extends State<ObservatoryShell> {
  int _selectedIndex = 0;

  static const _destinations = [
    NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Inicio'),
    NavigationDestination(icon: Icon(Icons.map_outlined), selectedIcon: Icon(Icons.map), label: 'Mapa'),
    NavigationDestination(icon: Icon(Icons.compare_arrows), label: 'Comparar'),
    NavigationDestination(icon: Icon(Icons.search), label: 'Búsqueda'),
    NavigationDestination(icon: Icon(Icons.info_outline), selectedIcon: Icon(Icons.info), label: 'Proyecto'),
  ];

  static const _railDestinations = [
    NavigationRailDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: Text('Inicio')),
    NavigationRailDestination(icon: Icon(Icons.map_outlined), selectedIcon: Icon(Icons.map), label: Text('Mapa')),
    NavigationRailDestination(icon: Icon(Icons.compare_arrows), label: Text('Comparar')),
    NavigationRailDestination(icon: Icon(Icons.search), label: Text('Búsqueda demo')),
    NavigationRailDestination(icon: Icon(Icons.info_outline), selectedIcon: Icon(Icons.info), label: Text('Proyecto')),
  ];

  @override
  Widget build(BuildContext context) {
    final wide = MediaQuery.sizeOf(context).width >= 900;
    final content = IndexedStack(
      index: _selectedIndex,
      children: const [
        HomeScreen(),
        MapScreen(),
        CompareScreen(),
        SearchScreen(),
        ProjectScreen(),
      ],
    );
    return Scaffold(
      appBar: AppBar(
        titleSpacing: wide ? 28 : 16,
        title: const _BrandHeader(),
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
            Text(kicker.toUpperCase(), style: const TextStyle(color: _brandDark, fontSize: 12, fontWeight: FontWeight.w800, letterSpacing: 1)),
            const SizedBox(height: 6),
            Text(title, style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: _ink, fontWeight: FontWeight.w800)),
            const SizedBox(height: 8),
            child,
          ],
        ),
      );
}

class _Card extends StatelessWidget {
  const _Card({required this.child});
  final Widget child;

  @override
  Widget build(BuildContext context) => Card(
        elevation: 0,
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
        decoration: BoxDecoration(color: _brandSoft, borderRadius: BorderRadius.circular(14)),
        child: Text(child, style: const TextStyle(color: _ink, height: 1.45)),
      );
}

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Observatorio del cuidado',
        title: 'Economía del cuidado en CDMX',
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Consulta datos territoriales, compara alcaldías y recorre una búsqueda demostrativa sin llenar formularios operativos.', style: TextStyle(color: _muted, height: 1.5)),
            const SizedBox(height: 16),
            const _Notice(child: 'Demostración académica: las cifras y resultados sintéticos no confirman plazas ni efectos laborales.'),
            const SizedBox(height: 24),
            Text('¿Qué quieres explorar?', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800, color: _ink)),
            const SizedBox(height: 12),
            LayoutBuilder(builder: (context, constraints) {
              final columns = constraints.maxWidth >= 700 ? 3 : 1;
              return GridView.builder(
                itemCount: 3,
                gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: columns,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  mainAxisExtent: columns == 1 ? 160 : 140,
                ),
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemBuilder: (context, index) => const [
                  _ActionCard(icon: Icons.map_outlined, title: 'Explorar mapa', description: 'Consulta una alcaldía y sus datos demográficos.'),
                  _ActionCard(icon: Icons.compare_arrows, title: 'Comparar alcaldías', description: 'Ordena indicadores demográficos autorizados.'),
                  _ActionCard(icon: Icons.search, title: 'Probar búsqueda', description: 'Recorre un ejemplo de compatibilidad sintética.'),
                ][index],
              );
            }),
          ],
        ),
      );
}

class _ActionCard extends StatelessWidget {
  const _ActionCard({required this.icon, required this.title, required this.description});
  final IconData icon;
  final String title;
  final String description;

  @override
  Widget build(BuildContext context) => _Card(
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
      );
}

const _alcaldias = ['Álvaro Obregón', 'Azcapotzalco', 'Benito Juárez', 'Coyoacán', 'Cuajimalpa', 'Cuauhtémoc', 'Gustavo A. Madero', 'Iztacalco', 'Iztapalapa', 'La Magdalena Contreras', 'Miguel Hidalgo', 'Milpa Alta', 'Tláhuac', 'Tlalpan', 'Venustiano Carranza', 'Xochimilco'];

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  String? _selected;

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Explorador territorial',
        title: 'Explora tu alcaldía',
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Selecciona una alcaldía para consultar sus datos preparados.', style: TextStyle(color: _muted)),
            const SizedBox(height: 14),
            const _Notice(child: 'La población corresponde al Censo 2020 de INEGI (ITER), agregada por alcaldía. Los grupos etarios describen población registrada y no equivalen a necesidad de cuidado.'),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              initialValue: _selected,
              decoration: const InputDecoration(labelText: 'Alcaldía'),
              hint: const Text('Selecciona una alcaldía'),
              items: _alcaldias.map((name) => DropdownMenuItem(value: name, child: Text(name))).toList(),
              onChanged: (value) => setState(() => _selected = value),
            ),
            const SizedBox(height: 16),
            _MapPlaceholder(selected: _selected),
            if (_selected != null) ...[
              const SizedBox(height: 20),
              Text('Datos de $_selected', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.w800, color: _ink)),
              const Text('Fuente: INEGI, Censo 2020 (ITER). Cartografía: Portal de Datos Abiertos de CDMX.', style: TextStyle(color: _muted, fontSize: 13)),
              const SizedBox(height: 12),
              const Wrap(spacing: 10, runSpacing: 10, children: [
                _Metric(title: 'Población total', value: 'Demo', note: 'Dato preparado'),
                _Metric(title: '0 a 4 años', value: 'Demo', note: 'Intervalo exacto'),
                _Metric(title: '60 años o más', value: 'Demo', note: 'Suma técnica'),
              ]),
              const SizedBox(height: 16),
              const _Card(child: _AgeBars()),
              const SizedBox(height: 12),
              const _Card(child: Text('Los conteos describen población registrada y no prueban necesidad de cuidado, demanda efectiva ni impacto social.', style: TextStyle(color: _muted, height: 1.4))),
            ],
          ],
        ),
      );
}

class _MapPlaceholder extends StatelessWidget {
  const _MapPlaceholder({this.selected});
  final String? selected;

  @override
  Widget build(BuildContext context) => Container(
        height: 250,
        width: double.infinity,
        decoration: BoxDecoration(color: _brandSoft, borderRadius: BorderRadius.circular(16), border: Border.all(color: _border)),
        child: Stack(
          alignment: Alignment.center,
          children: [
            const Icon(Icons.map, size: 72, color: Color(0xFFB7A1E8)),
            Positioned(top: 14, left: 16, child: Text('16 alcaldías · mapa demo', style: TextStyle(color: _brandDark, fontWeight: FontWeight.w800))),
            if (selected != null) Positioned(bottom: 14, child: Chip(label: Text(selected!), backgroundColor: Colors.white)),
          ],
        ),
      );
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
  const _AgeBars();

  @override
  Widget build(BuildContext context) => Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('Población por grupos de edad', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800, color: _ink)),
        const SizedBox(height: 4),
        const Text('Representación visual sintética para esta fase.', style: TextStyle(color: _muted, fontSize: 13)),
        const SizedBox(height: 14),
        for (final item in const [('0–14 años', .72), ('15–59 años', .95), ('60 años o más', .38)])
          Padding(padding: const EdgeInsets.only(bottom: 10), child: Row(children: [
            SizedBox(width: 105, child: Text(item.$1, style: const TextStyle(color: _muted, fontSize: 13))),
            Expanded(child: LinearProgressIndicator(value: item.$2, minHeight: 12, borderRadius: BorderRadius.circular(8), color: _brand, backgroundColor: _brandSoft)),
          ])),
      ]);
}

class CompareScreen extends StatefulWidget {
  const CompareScreen({super.key});

  @override
  State<CompareScreen> createState() => _CompareScreenState();
}

class _CompareScreenState extends State<CompareScreen> {
  String _a = 'Iztapalapa';
  String _b = 'Benito Juárez';

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Comparación territorial',
        title: 'Compara dos alcaldías',
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('Explora cómo cambia la composición de la población entre dos zonas.', style: TextStyle(color: _muted)),
          const SizedBox(height: 16),
          LayoutBuilder(builder: (context, constraints) {
            final vertical = constraints.maxWidth < 560;
            final fields = [
              DropdownButtonFormField<String>(initialValue: _a, decoration: const InputDecoration(labelText: 'Alcaldía A'), items: _alcaldias.map((x) => DropdownMenuItem(value: x, child: Text(x))).toList(), onChanged: (x) { if (x != null) setState(() => _a = x); }),
              DropdownButtonFormField<String>(initialValue: _b, decoration: const InputDecoration(labelText: 'Alcaldía B'), items: _alcaldias.where((x) => x != _a).map((x) => DropdownMenuItem(value: x, child: Text(x))).toList(), onChanged: (x) { if (x != null) setState(() => _b = x); }),
            ];
            return vertical ? Column(children: [fields[0], const SizedBox(height: 12), fields[1]]) : Row(children: [Expanded(child: fields[0]), const SizedBox(width: 12), Expanded(child: fields[1])]);
          }),
          const SizedBox(height: 20),
          _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            Text('Composición demográfica', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800, color: _ink)),
            const SizedBox(height: 4),
            const Text('Personas por cada 100 habitantes · datos demo', style: TextStyle(color: _muted, fontSize: 13)),
            const SizedBox(height: 16),
            _ComparisonRow(label: '0 a 14 años', first: _a, firstValue: .58, second: _b, secondValue: .42),
            _ComparisonRow(label: '60 años o más', first: _a, firstValue: .35, second: _b, secondValue: .52),
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
  final double firstValue;
  final String second;
  final double secondValue;

  @override
  Widget build(BuildContext context) => Padding(padding: const EdgeInsets.only(bottom: 16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(label, style: const TextStyle(fontWeight: FontWeight.w700, color: _ink)),
        const SizedBox(height: 8),
        _BarLabel(name: first, value: firstValue),
        _BarLabel(name: second, value: secondValue, color: const Color(0xFFA78BFA)),
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
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  int _step = 0;
  String _type = 'Cuidado infantil';
  bool _searched = false;

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Exploración guiada · demostración',
        title: 'Búsqueda demostrativa de cuidado',
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('Explora cómo se comparan filtros con una oferta sintética. No es un servicio de reserva.', style: TextStyle(color: _muted)),
          const SizedBox(height: 14),
          const _Notice(child: 'Datos sintéticos: una recomendación no confirma una plaza real ni registra personas.'),
          const SizedBox(height: 18),
          LinearProgressIndicator(value: (_step + 1) / 4, minHeight: 8, borderRadius: BorderRadius.circular(8), color: _brand, backgroundColor: _brandSoft),
          const SizedBox(height: 8),
          Text('Paso ${_step + 1} de 4 · ${['Servicio', 'Horario', 'Distancia', 'Resultados'][_step]}', style: const TextStyle(color: _muted, fontWeight: FontWeight.w600)),
          const SizedBox(height: 16),
          if (_step == 0) DropdownButtonFormField<String>(initialValue: _type, decoration: const InputDecoration(labelText: '¿Qué tipo de cuidado buscas?'), items: const [DropdownMenuItem(value: 'Cuidado infantil', child: Text('Cuidado infantil')), DropdownMenuItem(value: 'Cuidado para personas mayores', child: Text('Cuidado para personas mayores'))], onChanged: (value) { if (value != null) setState(() => _type = value); }),
          if (_step == 1) const _Card(child: Text('Lunes y martes · 09:00 a 12:00', style: TextStyle(color: _ink, fontWeight: FontWeight.w700))),
          if (_step == 2) const _Card(child: Text('Distancia máxima aproximada: 10 km', style: TextStyle(color: _ink, fontWeight: FontWeight.w700))),
          if (_step == 3) _SearchResult(searched: _searched, type: _type),
          const SizedBox(height: 18),
          Wrap(spacing: 10, runSpacing: 10, children: [
            if (_step > 0) OutlinedButton(onPressed: () => setState(() => _step--), child: const Text('Atrás')),
            FilledButton(onPressed: () => setState(() {
              if (_step < 3) {
                _step++;
              } else {
                _searched = true;
              }
            }), child: Text(_step == 2 ? 'Ver resultados' : _step == 3 ? 'Actualizar resultados' : 'Continuar')),
          ]),
        ]),
      );
}

class _SearchResult extends StatelessWidget {
  const _SearchResult({required this.searched, required this.type});
  final bool searched;
  final String type;

  @override
  Widget build(BuildContext context) => _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text(searched ? 'Centro demo compatible' : 'Completa los filtros', style: Theme.of(context).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w800, color: _ink)),
        const SizedBox(height: 8),
        Text(searched ? 'Recomendación sintética · $type' : 'Ejecuta la búsqueda para ver resultados.', style: const TextStyle(color: _muted)),
        if (searched) const Padding(padding: EdgeInsets.only(top: 8), child: Text('Resultado demostrativo; requiere verificación institucional y no confirma una plaza.', style: TextStyle(color: _muted, fontSize: 13))),
      ]));
}

class ProjectScreen extends StatelessWidget {
  const ProjectScreen({super.key});

  @override
  Widget build(BuildContext context) => _Page(
        kicker: 'Sobre este proyecto',
        title: 'Información del proyecto',
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const Text('Una lectura breve del propósito, alcance y límites del observatorio.', style: TextStyle(color: _muted)),
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
                _InfoCard(title: 'Qué puedes hacer', text: 'Consultar indicadores de las 16 alcaldías, comparar zonas y recorrer una búsqueda sintética.'),
                _InfoCard(title: 'Qué sigue siendo demostrativo', text: 'Las ofertas y resultados no representan plazas ni centros verificados.'),
              ][index],
            );
          }),
          const SizedBox(height: 20),
          const Text('Fuentes y metodología', style: TextStyle(fontSize: 19, fontWeight: FontWeight.w800, color: _ink)),
          const SizedBox(height: 8),
          const _Card(child: Text('Se conservan fuentes tabulares y cartográficas del repositorio. ENUT describe CDMX; la distribución proporcional por alcaldía es exploratoria. El matching demostrativo compara tipo de servicio, días, horario, radio y cupo.', style: TextStyle(color: _muted, height: 1.45))),
          const SizedBox(height: 16),
          const Text('Limitaciones esenciales', style: TextStyle(fontSize: 19, fontWeight: FontWeight.w800, color: _ink)),
          const SizedBox(height: 8),
          const _Notice(child: 'La infraestructura contabilizada no demuestra cupos disponibles; distancia geográfica no es tiempo de viaje; la estimación territorial no mide abandono laboral ni causalidad. No se recogen datos personales.'),
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
