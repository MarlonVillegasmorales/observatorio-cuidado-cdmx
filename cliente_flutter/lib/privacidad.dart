import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'privacidad_nativa.dart' if (dart.library.js_interop) 'privacidad_web.dart';

void mostrarPrivacidad(BuildContext context) {
  Navigator.of(context).push(MaterialPageRoute<void>(builder: (_) => const _Privacidad()));
}

class _Privacidad extends StatefulWidget {
  const _Privacidad();

  @override
  State<_Privacidad> createState() => _PrivacidadState();
}

class _PrivacidadState extends State<_Privacidad> {
  final contenido = rootBundle.loadString('assets/privacidad/aviso.json');

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Privacidad y uso de datos')),
      body: FutureBuilder<String>(
        future: contenido,
        builder: (context, snapshot) {
          if (snapshot.hasError) {
            return const Center(child: Text('No se pudo cargar la información de privacidad.'));
          }
          if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
          final aviso = jsonDecode(snapshot.data!) as Map<String, dynamic>;
          final bloques = aviso['bloques'] as List<dynamic>;
          return Center(child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 780),
            child: ListView(padding: const EdgeInsets.all(16), children: [
              for (final bloque in bloques)
                Card(color: const Color(0xfff0e8fc), child: Padding(
                  padding: const EdgeInsets.all(18),
                  child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                    Text(bloque['titulo'], style: Theme.of(context).textTheme.titleLarge),
                    const SizedBox(height: 8),
                    Text(bloque['texto']),
                    if (bloque == bloques.last) ...[
                      const Divider(),
                      Text(aviso['titulo'], style: Theme.of(context).textTheme.titleMedium),
                      Text('Versión ${aviso["version"]} · ${aviso["estado"]}'),
                      const SizedBox(height: 12),
                      if (kIsWeb)
                        FilledButton.icon(icon: const Icon(Icons.download),
                          label: const Text('Descargar aviso (PDF)'),
                          onPressed: () => descargarAviso(aviso['archivo']))
                      else
                        SelectableText('https://proyecto-cuidado-21dcb.web.app/assets/assets/privacidad/${aviso["archivo"]}'),
                    ],
                  ]),
                )),
            ]),
          ));
        },
      ),
    );
  }
}
