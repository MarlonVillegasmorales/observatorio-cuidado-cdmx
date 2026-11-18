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
            Text(
              "${total('sedes_unicas')} sedes · ${total('con_horario')} con horario · ${total('con_capacidad_exacta')} con capacidad exacta · ${total('con_rango_o_tope')} con rango o límite · ${total('con_vacantes_fechadas')} con vacantes fechadas",
            ),
            Text(
              "${sedes.where((s) => s.containsKey('punto')).length} sedes con coordenadas. Los datos corresponden al periodo de cada fuente.",
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
