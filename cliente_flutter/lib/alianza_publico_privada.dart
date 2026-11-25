import 'package:flutter/material.dart';

const _purple = Color(0xFF7036C4);
const _purpleDark = Color(0xFF4C1D95);
const _purpleSoft = Color(0xFFEDE9FE);
const _ink = Color(0xFF19152F);
const _muted = Color(0xFF475569);
const _border = Color(0xFFD9D3E6);
const _annualCost = 14624331.31;
const _bmvHiringCost = 33934.0;

String _money(double value) {
  final digits = value.round().toString();
  final grouped = StringBuffer();
  for (var i = 0; i < digits.length; i++) {
    if (i > 0 && (digits.length - i) % 3 == 0) grouped.write(',');
    grouped.write(digits[i]);
  }
  return r'$' + grouped.toString();
}
class AlianzaPublicoPrivadaScreen extends StatefulWidget {
  const AlianzaPublicoPrivadaScreen({super.key});

  @override
  State<AlianzaPublicoPrivadaScreen> createState() => _AlianzaPublicoPrivadaScreenState();
}

class _AlianzaPublicoPrivadaScreenState extends State<AlianzaPublicoPrivadaScreen> {
  int _companyShare = 25;
  int _companies = 40;

  @override
  Widget build(BuildContext context) {
    final privateTotal = _annualCost * _companyShare / 100;
    final publicTotal = _annualCost - privateTotal;
    final perCompany = privateTotal / _companies;
    final hiringEquivalent = perCompany / _bmvHiringCost;

    return SingleChildScrollView(
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
            Text('Alianza público privada', style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: Colors.white, fontWeight: FontWeight.w800)),
          ]),
        ),
        const SizedBox(height: 12),
        const _Notice('Compara cómo se distribuiría el costo operativo estimado de un centro tipo. Los porcentajes y el número de empresas son escenarios de diseño, no convenios ni compromisos aprobados.'),
        const SizedBox(height: 16),
        _heading(context, 'Ajusta el escenario'),
        const SizedBox(height: 10),
        DropdownButtonFormField<int>(
          initialValue: _companyShare,
          isExpanded: true,
          decoration: const InputDecoration(labelText: 'Porcentaje del costo aportado por empresas'),
          items: const [
            DropdownMenuItem(value: 25, child: Text('25% empresas · 75% público')),
            DropdownMenuItem(value: 50, child: Text('50% empresas · 50% público')),
            DropdownMenuItem(value: 75, child: Text('75% empresas · 25% público')),
          ],
          onChanged: (value) => setState(() => _companyShare = value ?? _companyShare),
        ),
        const SizedBox(height: 12),
        DropdownButtonFormField<int>(
          initialValue: _companies,
          isExpanded: true,
          decoration: const InputDecoration(labelText: 'Empresas participantes'),
          items: const [
            DropdownMenuItem(value: 10, child: Text('10 empresas')),
            DropdownMenuItem(value: 20, child: Text('20 empresas')),
            DropdownMenuItem(value: 40, child: Text('40 empresas')),
          ],
          onChanged: (value) => setState(() => _companies = value ?? _companies),
        ),
        const SizedBox(height: 16),
        _heading(context, 'Reparto anual del costo'),
        const SizedBox(height: 10),
        _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text('Costo operativo indicativo: ${_money(_annualCost)} por centro/año', style: const TextStyle(color: _ink, fontWeight: FontWeight.w700)),
          const SizedBox(height: 12),
          _FundingBar(publicShare: 100 - _companyShare, companyShare: _companyShare),
          const SizedBox(height: 12),
          Wrap(spacing: 10, runSpacing: 10, children: [
            _Metric(title: 'Aportación pública', value: _money(publicTotal), note: '${100 - _companyShare}% del costo'),
            _Metric(title: 'Aportación empresarial total', value: _money(privateTotal), note: 'repartida entre las firmas'),
            _Metric(title: 'Aporte por empresa', value: _money(perCompany), note: 'con $_companies participantes'),
          ]),
          const SizedBox(height: 10),
          const Text('Base: Evalúa CDMX estimó operación sin obra a precios de 2024. El costo medio se actualizó indicativamente a octubre de 2026 con el INPC general.', style: TextStyle(color: _muted, fontSize: 12, height: 1.4)),
        ])),
        const SizedBox(height: 14),
        _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _CardTitle('Aporte por empresa según tamaño del consorcio'),
          const SizedBox(height: 4),
          const Text('El monto total empresarial se mantiene; aumenta o disminuye el aporte medio según cuántas firmas participen.', style: TextStyle(color: _muted, height: 1.4)),
          const SizedBox(height: 14),
          _Bars(maxValue: privateTotal / 10, rows: [
            _Bar('10 empresas', privateTotal / 10, _money(privateTotal / 10)),
            _Bar('20 empresas', privateTotal / 20, _money(privateTotal / 20)),
            _Bar('40 empresas', privateTotal / 40, _money(privateTotal / 40)),
          ]),
        ])),
        const SizedBox(height: 14),
        _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _CardTitle('Umbral para comparar con contratación'),
          const SizedBox(height: 7),
          Text('${hiringEquivalent.toStringAsFixed(1)} contrataciones equivalentes por empresa al año', style: Theme.of(context).textTheme.titleMedium?.copyWith(color: _purpleDark, fontWeight: FontWeight.w800)),
          const SizedBox(height: 6),
          Text('Comparación: ${_money(perCompany)} ÷ ${_money(_bmvHiringCost)} de costo promedio por contratación reportado por Grupo BMV.', style: const TextStyle(color: _muted, height: 1.4)),
          const SizedBox(height: 10),
          const _Notice('Es un umbral contable, no el número de salidas que ocurren o se evitarían. El promedio BMV mezcla tipos de contratación y no mide el costo completo de reemplazo.'),
        ])),
        const SizedBox(height: 14),
        _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _CardTitle('La evidencia laboral que orienta el piloto'),
          const SizedBox(height: 8),
          const _Metric(title: 'Mujeres en comercio minorista', value: '47.0%', note: 'CDMX · personal ocupado en 2023'),
          const SizedBox(height: 8),
          const _Metric(title: 'Mujeres en hoteles y restaurantes', value: '48.2%', note: 'CDMX · personal ocupado en 2023'),
          const SizedBox(height: 10),
          const Text('Rotación total reportada en México en 2019: comercio minorista, 25.1%–30.6% en empresas de 11–250 personas; hoteles y restaurantes, 27.2%–39.4% en esos tamaños.', style: TextStyle(color: _ink, height: 1.45)),
          const SizedBox(height: 6),
          const Text('Los datos de rotación son nacionales, históricos y no están desglosados por sexo. Ayudan a priorizar sectores; no prueban rotación actual en Iztapalapa ni efecto del cuidado.', style: TextStyle(color: _muted, fontSize: 12, height: 1.4)),
        ])),
        const SizedBox(height: 14),
        _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _CardTitle('Precedentes de participación empresarial'),
          const SizedBox(height: 8),
          const Wrap(spacing: 8, runSpacing: 8, children: [
            _Metric(title: 'Gentera · personal usuario', value: '54', note: 'personas progenitoras · 2024'),
            _Metric(title: 'Gentera · niñas y niños', value: '62', note: 'atendidos · CDMX · 2024'),
            _Metric(title: 'Coppel · apoyo escolar', value: '7,424', note: 'hijas e hijos con 50% de colegiatura'),
            _Metric(title: 'Coppel · lactancia', value: '18', note: 'salas reportadas · 2024'),
          ]),
          const SizedBox(height: 8),
          const Text('Documentan inversión y prestaciones privadas de cuidado. No publican ahorro atribuible ni efecto causal en rotación.', style: TextStyle(color: _muted, fontSize: 12, height: 1.4)),
        ])),
        const SizedBox(height: 14),
        const _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          _CardTitle('Mecanismo y límites'),
          SizedBox(height: 8),
          Text('En CECI en Empresa, la empresa aporta terreno, construcción y equipamiento. El IMSS cubre al patrón una cuota mensual por cada niña o niño inscrito conforme al convenio, además de regular y capacitar. No existe una cuota única que pueda aplicarse aquí sin convenio.', style: TextStyle(color: _ink, height: 1.45)),
          SizedBox(height: 10),
          _Notice('Ahorro observado por menor rotación: dato no publicado. La recuperación de inversión en cinco años difundida para CECI es una proyección con ocupación del 100%, no un retorno medido en Iztapalapa. El costo mostrado excluye construcción y remodelación.'),
        ])),
        const SizedBox(height: 14),
        _Card(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          const _CardTitle('Fuentes'),
          const SizedBox(height: 8),
          const _Source('Evalúa CDMX · evaluación y propuesta territorial', 'https://www.evalua.cdmx.gob.mx/storage/app/media/2024/se/ee/cuidados/evaluacion-cuidados-vf.pdf'),
          const _Source('IMSS · acuerdo CECI en Empresa, 2026', 'https://sidof.segob.gob.mx/notas/docFuente/5784757'),
          const _Source('Secretaría de Economía · modelo CECI en Empresa', 'https://www.gob.mx/se/prensa/economia-el-bid-y-la-cepal-impulsan-la-construccion-de-infraestructura-de-cuidados-en-empresas-y-parques-industriales?idiom=es-MX'),
          const _Source('Grupo BMV · Informe Anual Integrado 2025', 'https://www.bmv.com.mx/docs-pub/informeAnual/Informe%20Anual%20Integrado%20Grupo%20BMV_2025.pdf'),
          const _Source('INEGI · Censos Económicos 2024, CDMX', 'https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE_2024_Def_CdMx.pdf'),
          const _Source('Data México · comercio minorista y hoteles/restaurantes', 'https://www.economia.gob.mx/datamexico/es/profile/industry/retail-trade'),
          const _Source('Data México · hoteles y restaurantes', 'https://www.economia.gob.mx/datamexico/es/profile/industry/accommodation-and-food-services'),
          const _Source('IFC · caso Gentera', 'https://www.ifc.org/content/dam/ifc/doc/2025/family-friendly-policies-in-the-private-sector-in-mexico-en.pdf'),
          const _Source('IFC · caso Grupo Coppel', 'https://www.ifc.org/es/pressroom/2025/ifc-and-grupo-coppel-study'),
        ])),
      ]),
    );
  }

  static Widget _heading(BuildContext context, String title) => Text(title, style: Theme.of(context).textTheme.titleLarge?.copyWith(color: _ink, fontWeight: FontWeight.w800));
}

class _FundingBar extends StatelessWidget {
  const _FundingBar({required this.publicShare, required this.companyShare});
  final int publicShare, companyShare;
  @override
  Widget build(BuildContext context) => Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Row(children: [
          Expanded(flex: publicShare, child: Container(height: 22, decoration: const BoxDecoration(color: _purpleDark, borderRadius: BorderRadius.horizontal(left: Radius.circular(8))))),
          Expanded(flex: companyShare, child: Container(height: 22, decoration: const BoxDecoration(color: Color(0xFFA78BFA), borderRadius: BorderRadius.horizontal(right: Radius.circular(8))))),
        ]),
        const SizedBox(height: 6),
        Row(children: [
          Expanded(child: Text('Público ${publicShare}%', style: const TextStyle(color: _purpleDark, fontWeight: FontWeight.w700, fontSize: 12))),
          Expanded(child: Text('Empresas ${companyShare}%', textAlign: TextAlign.end, style: const TextStyle(color: _purpleDark, fontWeight: FontWeight.w700, fontSize: 12))),
        ]),
      ]);
}

class _Metric extends StatelessWidget {
  const _Metric({required this.title, required this.value, required this.note});
  final String title, value, note;
  @override
  Widget build(BuildContext context) => SizedBox(width: 155, child: Card(
        elevation: 0, color: const Color(0xFFF6F3FC), margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14), side: const BorderSide(color: _border)),
        child: Padding(padding: const EdgeInsets.all(12), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title, style: const TextStyle(color: _muted, fontWeight: FontWeight.w600, fontSize: 12)),
          const SizedBox(height: 6),
          Text(value, style: Theme.of(context).textTheme.titleMedium?.copyWith(color: _ink, fontWeight: FontWeight.w800)),
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
        elevation: 0, color: Colors.white, margin: EdgeInsets.zero,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16), side: const BorderSide(color: _border)),
        child: Padding(padding: const EdgeInsets.all(16), child: child),
      );
}

class _CardTitle extends StatelessWidget {
  const _CardTitle(this.text);
  final String text;
  @override
  Widget build(BuildContext context) => Text(text, style: const TextStyle(color: _ink, fontWeight: FontWeight.w800, fontSize: 16));
}

class _Notice extends StatelessWidget {
  const _Notice(this.text);
  final String text;
  @override
  Widget build(BuildContext context) => Container(
        width: double.infinity, padding: const EdgeInsets.all(14),
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
          Padding(padding: const EdgeInsets.only(bottom: 12), child: Column(children: [
            Row(children: [
              SizedBox(width: 110, child: Text(row.label, style: const TextStyle(color: _muted, fontSize: 12))),
              Expanded(child: ClipRRect(
                borderRadius: BorderRadius.circular(8),
                child: LinearProgressIndicator(
                  value: (row.value / maxValue).clamp(0.0, 1.0).toDouble(),
                  minHeight: 13, color: _purple, backgroundColor: _purpleSoft,
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
  const _Source(this.label, this.url);
  final String label, url;
  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(bottom: 9),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(label, style: const TextStyle(color: _ink, fontWeight: FontWeight.w700, fontSize: 12)),
          SelectableText(url, style: const TextStyle(color: _purpleDark, fontSize: 10, decoration: TextDecoration.underline)),
        ]),
      );
}
