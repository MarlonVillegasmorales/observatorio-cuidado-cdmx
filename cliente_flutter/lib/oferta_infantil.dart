import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

typedef Registro = Map<String, dynamic>;

Future<Map<String, Registro>> cargarOfertaInfantil() async {
  final raw = await rootBundle.loadString(
    'assets/data/directorio_infantil.json',
  );
  return (jsonDecode(raw) as Registro).cast<String, Registro>();
}

class ResumenHorario extends StatelessWidget {
  const ResumenHorario({super.key, required this.nombre, required this.sedes, required this.horario});
  final String nombre;
  final int sedes;
  final int horario;

  @override
  Widget build(BuildContext context) {
    final proporcion = sedes > 0 ? horario / sedes : null;
    final porcentaje = proporcion == null ? 'Sin dato' : '${(100 * proporcion).round()} %';
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Text('$nombre · $porcentaje', style: Theme.of(context).textTheme.titleLarge),
        if (proporcion != null) LinearProgressIndicator(value: proporcion),
        Text('$horario de $sedes sedes documentadas tienen horario publicado.'),
      ]),
    );
  }
}

class OfertaInfantil extends StatelessWidget {
  const OfertaInfantil({
    super.key,
    required this.grupos,
    required this.alcaldia,
  });
  final List<Registro> grupos;
  final String? alcaldia;

  @override
  Widget build(BuildContext context) {
    int total(String campo) =>
        grupos.fold<int>(0, (n, g) => n + (g['resumen'][campo] as int));
    final sedes = grupos
        .expand((g) => (g['sedes'] as List).cast<Registro>())
        .toList();
    final ubicadas = sedes.where((s) => s.containsKey('punto')).length;
    final porRed = <String, List<Registro>>{};
    for (final s in sedes) {
      for (final u in (s['unidades'] as List).cast<Registro>()) {
        porRed.putIfAbsent(u['red'] as String, () => []).add(u);
      }
    }
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Oferta infantil documentada',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            Wrap(
              spacing: 8,
              runSpacing: 4,
              children: [
                for (final (campo, etiqueta) in const [
                  ('sedes_unicas', 'Sedes documentadas'),
                  ('con_horario', 'Con horario publicado'),
                  ('con_capacidad_exacta', 'Con capacidad exacta publicada'),
                ])
                  Chip(label: Text('${total(campo)} · $etiqueta')),
              ],
            ),
            ResumenHorario(nombre: alcaldia ?? 'Toda la CDMX', sedes: total('sedes_unicas'), horario: total('con_horario')),
            Text(
              "$ubicadas sedes con punto en el mapa · ${sedes.length - ubicadas} solo con domicilio en el directorio. Los datos corresponden al periodo de cada fuente.",
            ),
            ExpansionTile(
              title: const Text('Lugares y disponibilidad'),
              children: [
                Text(
                  "${total('con_capacidad_exacta')} centros publicaron cuántas personas podían atender y ${total('con_rango_o_tope')} publicaron un rango o límite.",
                ),
                Text(
                  total('con_vacantes_fechadas') == 0
                      ? 'Todavía se desconoce cuántos lugares están libres.'
                      : "${total('con_vacantes_fechadas')} centros informaron lugares libres con fecha.",
                ),
              ],
            ),
            if (alcaldia == null)
              const ExpansionTile(
                title: Text('México · 2022 | Personas y horas de cuidado'),
                children: [
                  Text(
                    'En México, 31.7 millones de personas de 15 años o más cuidaron a alguien de su hogar o de otro hogar en 2022. El 75.1 % de quienes brindaron cuidados eran mujeres. Entre las personas cuidadoras principales, las mujeres dedicaron en promedio 38.9 horas semanales y los hombres, 30.6.',
                  ),
                  SelectableText(
                    'INEGI · ENASIC 2022 · resultados nacionales\nhttps://www.inegi.org.mx/programas/enasic/2022/',
                  ),
                ],
              ),
            const ExpansionTile(
              title: Text('Cómo protegemos tus datos'),
              children: [
                Text(
                  'Puedes consultar el mapa sin dar tu nombre ni tu ubicación. Los puntos representan centros de cuidado. El directorio publica domicilios institucionales y cifras por sede. Los datos de niñas, niños, familias y personas trabajadoras quedan fuera de este directorio.',
                ),
              ],
            ),
            if (alcaldia != null)
              ExpansionTile(
                title: const Text('Consultar sedes y fuentes'),
                children: [
                  for (final red in (porRed.keys.toList()..sort()))
                    ExpansionTile(
                      title: Text(red),
                      children: [
                        for (final u in porRed[red]!)
                          ExpansionTile(
                            title: Text(u['nombre']),
                            children: [
                              Padding(
                                padding: const EdgeInsets.all(10),
                                child: SelectableText(
                                  [
                                    u['domicilio'],
                                    if (u['apertura'] != null)
                                      "Horario ${u['apertura']}–${u['cierre']} · ${u['periodo_horario']}",
                                    if (u['apertura_extra'] != null)
                                      "Horario extraordinario ${u['apertura_extra']}–${u['cierre_extra']}",
                                    if (u['capacidad_exacta'] != null)
                                      "Capacidad ${u['capacidad_exacta']} · ${u['periodo_capacidad']}",
                                    if (u['capacidad_max'] != null)
                                      "Capacidad ${u['capacidad_min'] ?? 'hasta'} ${u['capacidad_min'] == null ? '' : '– '}${u['capacidad_max']} · ${u['periodo_capacidad']}",
                                    u['fecha_vacantes'] == null
                                        ? 'Vacantes: sin dato fechado'
                                        : "Vacantes: ${u['vacantes']} · ${u['fecha_vacantes']}",
                                    "Fuente · ${u['periodo_fuente']}\n${u['fuente_url']}",
                                    if (u['fuente_capacidad_url'] != null)
                                      "Fuente de capacidad\n${u['fuente_capacidad_url']}",
                                    if (u['nota'] != null) u['nota'],
                                  ].join('\n'),
                                ),
                              ),
                            ],
                          ),
                      ],
                    ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
