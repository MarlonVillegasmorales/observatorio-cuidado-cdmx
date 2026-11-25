import 'package:flutter/material.dart';

const _purple = Color(0xFF7036C4);
const _purpleDark = Color(0xFF4C1D95);
const _purpleSoft = Color(0xFFEDE9FE);
const _ink = Color(0xFF19152F);
const _muted = Color(0xFF475569);
const _border = Color(0xFFD9D3E6);

class PropuestaPublicaScreen extends StatelessWidget {
  const PropuestaPublicaScreen({super.key});

  @override
  Widget build(BuildContext context) => SingleChildScrollView(
        padding: const EdgeInsets.fromLTRB(20, 24, 20, 32),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [_purpleDark, _purple]),
              borderRadius: BorderRadius.circular(18),
            ),
            child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
              const Text('PILOTO TERRITORIAL · IZTAPALAPA', style: TextStyle(color: Color(0xFFEEE4FF), fontSize: 12, fontWeight: FontWeight.w700, letterSpacing: 1)),
              const SizedBox(height: 5),
              Text('Propuesta pública de cuidado infantil', style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: Colors.white, fontWeight: FontWeight.w800)),
            ]),
          ),
          const SizedBox(height: 12),
          const _Notice('Cobertura: CACI públicos para niñas y niños de 0 a 2 años, 2023. La expansión propuesta por Evalúa considera población de 0 a 5 años.'),
          const SizedBox(height: 16),
          _heading(context, 'Cobertura pública en 2023'),
          const SizedBox(height: 10),
          const Wrap(spacing: 10, runSpacing: 10, children: [
            _Metric(title: 'Cobertura Iztapalapa', value: '5.5%', note: 'población de 0–2 años'),
            _Metric(title: 'Matrícula', value: '3,164', note: 'niñas y niños'),
            _Metric(title: 'Población 0–2', value: '57,907', note: 'Iztapalapa'),
            _Metric(title: 'CACI públicos', value: '48', note: 'centros reportados'),
          ]),
          const SizedBox(height: 14),
          _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const _CardTitle('Comparación de cobertura'),
            const SizedBox(height: 5),
            const Text('Iztapalapa está debajo del promedio de CDMX, pero no registra la cobertura más baja. Milpa Alta tuvo 2.9%.', style: TextStyle(color: _muted, height: 1.4)),
            const SizedBox(height: 16),
            const _Bars(maxValue: 12, rows: [
              _Bar('Milpa Alta', 2.9, '2.9%'),
              _Bar('Iztapalapa', 5.5, '5.5%'),
              _Bar('CDMX', 10.7, '10.7%'),
            ]),
            const SizedBox(height: 6),
            const Text('Fuente: Evalúa CDMX · CACI públicos para 0–2 años · 2023.', style: TextStyle(color: _muted, fontSize: 12)),
          ])),
          const SizedBox(height: 14),
          _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const _CardTitle('Distancia media al CACI más cercano'),
            const SizedBox(height: 5),
            const Text('Promedios de 2020 para colonias en zonas ampliadas de concentración infantil. No son tiempos de viaje ni distancias actuales por domicilio.', style: TextStyle(color: _muted, height: 1.4)),
            const SizedBox(height: 16),
            const _Bars(maxValue: 2500, rows: [
              _Bar('Gobierno CDMX', 2319, '2,319 m'),
              _Bar('Alcaldía', 1260, '1,260 m'),
              _Bar('Privado', 906, '906 m'),
              _Bar('Comunitario', 757, '757 m'),
            ]),
            const SizedBox(height: 6),
            const Text('Fuente: Evalúa CDMX · análisis espacial · 2020.', style: TextStyle(color: _muted, fontSize: 12)),
          ])),
          const SizedBox(height: 18),
          _heading(context, 'Expansión territorial propuesta'),
          const SizedBox(height: 10),
          const Wrap(spacing: 10, runSpacing: 10, children: [
            _Metric(title: 'Espacios propuestos', value: '41', note: 'no reportados como construidos'),
            _Metric(title: 'Población potencial', value: '67,146', note: 'niñas y niños de 0–5 años'),
            _Metric(title: 'Centro tipo', value: '117', note: 'plazas de referencia'),
          ]),
          const SizedBox(height: 14),
          _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            const _CardTitle('Costo anual de operación por centro'),
            const SizedBox(height: 5),
            const Text('Promedio derivado de la estimación para 41 espacios. Excluye construcción y remodelación.', style: TextStyle(color: _muted, height: 1.4)),
            const SizedBox(height: 16),
            const _Bars(maxValue: 16, rows: [
              _Bar('Precios 2024', 13.72, '\$13.72 M'),
              _Bar('Actualiz. oct. 2026', 14.62, '\$14.62 M'),
            ]),
            const SizedBox(height: 10),
            const _Notice('\$14.62 millones por centro/año. Aproximadamente \$124,994 por plaza/año a ocupación plena. Actualización indicativa por INPC general; no es cotización ni presupuesto autorizado.'),
            const SizedBox(height: 8),
            const Text('Cálculo: \$562.58 millones ÷ 41 = \$13.72 millones por centro. INPC: 137.949 (dic. 2024) a 147.026 (oct. 2026).', style: TextStyle(color: _muted, fontSize: 12, height: 1.4)),
          ])),
          const SizedBox(height: 16),
          _heading(context, 'Fuentes y datos pendientes'),
          const SizedBox(height: 10),
          const _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
            _Source('Evalúa CDMX · evaluación del sistema de cuidados', 'https://www.evalua.cdmx.gob.mx/storage/app/media/2024/se/ee/cuidados/evaluacion-cuidados-vf.pdf'),
            _Source('Evalúa CDMX · opinión técnica de presupuesto 2024–2025', 'https://www.evalua.cdmx.gob.mx/storage/app/media/2024/se/opinion-de-presupuesto-para-2024-2025.pdf'),
            _Source('INEGI · INPC octubre de 2026', 'https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/inpc/inpc_2q2026_11.pdf'),
            _Source('INEGI · INPC diciembre de 2024', 'https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/inpc/inpc_2q2025_01.pdf'),
            SizedBox(height: 6),
            _Notice('Pendiente: seleccionar inmueble y validar obra, permisos y capacidad autorizada. Evalúa identifica 41 espacios, pero la tabla no publica nombres y coordenadas.'),
          ])),
        ]),
      );

  static Widget _heading(BuildContext context, String title) => Text(
        title,
        style: Theme.of(context).textTheme.titleLarge?.copyWith(color: _ink, fontWeight: FontWeight.w800),
      );
}

class _Metric extends StatelessWidget {
  const _Metric({required this.title, required this.value, required this.note});
  final String title, value, note;
  @override
  Widget build(BuildContext context) => SizedBox(width: 155, child: Card(
        elevation: 0,
        color: Colors.white,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: const BorderSide(color: _border)),
        child: Padding(padding: const EdgeInsets.all(14), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title, style: const TextStyle(color: _muted, fontWeight: FontWeight.w600, fontSize: 12)),
          const SizedBox(height: 7),
          Text(value, style: Theme.of(context).textTheme.titleLarge?.copyWith(color: _ink, fontWeight: FontWeight.w800)),
          const SizedBox(height: 3),
          Text(note, style: const TextStyle(color: _muted, fontSize: 11, height: 1.3)),
        ])),
      ));
}

class _Card extends StatelessWidget {
  const _Card({required this.child});
  final Widget child;
  @override
  Widget build(BuildContext context) => Card(
        elevation: 0,
        color: Colors.white,
        margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: const BorderSide(color: _border)),
        child: Padding(padding: const EdgeInsets.all(16), child: child),
      );
}

class _CardTitle extends StatelessWidget {
  const _CardTitle(this.text);
  final String text;
  @override
  Widget build(BuildContext context) => Text(text, style: Theme.of(context).textTheme.titleMedium?.copyWith(color: _ink, fontWeight: FontWeight.w800));
}

class _Notice extends StatelessWidget {
  const _Notice(this.text);
  final String text;
  @override
  Widget build(BuildContext context) => Container(
        width: double.infinity,
        padding: const EdgeInsets.all(14),
        decoration: BoxDecoration(color: const Color(0xFFE8F1FA), borderRadius: BorderRadius.circular(14)),
        child: Text(text, style: const TextStyle(color: _ink, height: 1.45)),
      );
}

class _Bar {
  const _Bar(this.label, this.value, this.display);
  final String label, display;
  final double value;
}

class _Bars extends StatelessWidget {
  const _Bars({required this.rows, required this.maxValue});
  final List<_Bar> rows;
  final double maxValue;
  @override
  Widget build(BuildContext context) => Column(children: [
        for (final row in rows)
          Padding(padding: const EdgeInsets.only(bottom: 13), child: Column(children: [
            Row(children: [
              SizedBox(width: 116, child: Text(row.label, style: const TextStyle(color: _muted, fontSize: 12))),
              Expanded(child: ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: LinearProgressIndicator(
                  value: (row.value / maxValue).clamp(0.0, 1.0),
                  minHeight: 13,
                  color: row.label == 'Iztapalapa' || row.label.startsWith('Actualiz.') ? _purple : _purpleDark,
                  backgroundColor: _purpleSoft,
                ),
              )),
            ]),
            Align(alignment: Alignment.centerRight, child: Padding(
              padding: const EdgeInsets.only(top: 3),
              child: Text(row.display, style: const TextStyle(color: _ink, fontSize: 12, fontWeight: FontWeight.w700)),
            )),
          ])),
      ]);
}

class _Source extends StatelessWidget {
  const _Source(this.title, this.url);
  final String title, url;
  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 9),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title, style: const TextStyle(color: _ink, fontWeight: FontWeight.w700, fontSize: 12)),
          SelectableText(url, style: const TextStyle(color: _purpleDark, fontSize: 10, decoration: TextDecoration.underline)),
        ]),
      );
}
