import 'dart:convert';
import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'package:cliente_flutter/main.dart';

void main() {
  testWidgets('muestra la pantalla de inicio y cinco destinos', (tester) async {
    await tester.pumpWidget(const ObservatorioApp());
    await tester.pumpAndSettle();

    expect(find.text('Economía del cuidado en CDMX'), findsOneWidget);
    expect(find.text('Explorar mapa'), findsOneWidget);
    expect(find.text('Búsqueda'), findsOneWidget);
    expect(find.text('Proyecto'), findsOneWidget);
  });

  testWidgets('las tarjetas de inicio abren la sección correspondiente', (tester) async {
    tester.view..physicalSize = const Size(360, 800)..devicePixelRatio = 1;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
    await tester.pumpWidget(const ObservatorioApp());
    await tester.pumpAndSettle();

    await tester.ensureVisible(find.text('Explorar mapa').first);
    await tester.tap(find.text('Explorar mapa').first);
    await tester.pumpAndSettle();
    expect(find.byKey(const Key('nav_mapa')), findsOneWidget);

    await tester.tap(find.byKey(const Key('nav_inicio')));
    await tester.pumpAndSettle();
    await tester.ensureVisible(find.text('Comparar alcaldías').first);
    await tester.tap(find.text('Comparar alcaldías').first);
    await tester.pumpAndSettle();
    expect(find.text('Compara dos alcaldías'), findsOneWidget);

    await tester.tap(find.byKey(const Key('nav_inicio')));
    await tester.pumpAndSettle();
    await tester.ensureVisible(find.text('Probar búsqueda').first);
    await tester.tap(find.text('Probar búsqueda').first);
    await tester.pumpAndSettle();
    expect(find.text('Paso 1 de 4 · Servicio'), findsOneWidget);
  });

  testWidgets('navega a mapa y permite seleccionar una alcaldía', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: MapScreen(
            geometryFuture: rootBundle.loadString('assets/data/alcaldias.geojson'),
            dataFuture: Future.value([
              const AlcaldiaData(
                name: 'Iztapalapa',
                period: '2020',
                total: 1835486,
                children: 103148,
                children14: 366835,
                olderAdults: 262064,
                source: 'INEGI, Censo 2020 (ITER)',
                dataType: 'observado',
              ),
            ]),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('Explora tu alcaldía'), findsOneWidget);

    await tester.tap(find.byType(DropdownButtonFormField<String>));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Iztapalapa').last);
    await tester.pumpAndSettle();
    expect(find.text('Datos de Iztapalapa'), findsOneWidget);

    await tester.tap(find.text('Ver toda CDMX'));
    await tester.pumpAndSettle();
    expect(find.text('Datos de Iztapalapa'), findsNothing);
  });

  testWidgets('el polígono y el selector muestran las mismas sedes de Iztapalapa', (tester) async {
    final geo = File('assets/data/alcaldias.geojson').readAsStringSync();
    final raw = File('assets/data/directorio_infantil.json').readAsStringSync();
    final grupos = (jsonDecode(raw) as Map).cast<String, Map<String, dynamic>>();
    await tester.pumpWidget(MaterialApp(home: Scaffold(body: MapScreen(
      geometryFuture: Future.value(geo),
      ofertaFuture: Future.value(grupos),
      dataFuture: Future.value([]),
    ))));
    await tester.pumpAndSettle();
    void comprobar() {
      for (final label in ['42 · Sedes documentadas', '37 · Con horario publicado',
        '28 · Con capacidad exacta publicada', 'Iztapalapa · 88 %']) {
        expect(find.text(label), findsOneWidget);
      }
      expect(find.textContaining('8 sedes con punto en el mapa · 34 solo con domicilio'), findsOneWidget);
    }
    final mapa = find.bySemanticsLabel('Mapa territorial de las 16 alcaldías');
    await tester.ensureVisible(mapa);
    // Punto interior de Iztapalapa en la cartografía empaquetada, relativo al centro del mapa.
    final altura = tester.getSize(mapa).height - 28;
    await tester.tapAt(tester.getCenter(mapa) + Offset(0.1942 * altura, -0.04094 * altura));
    await tester.pumpAndSettle();
    comprobar();
    final reset = find.text('Ver toda CDMX');
    await tester.ensureVisible(reset);
    await tester.tap(reset);
    await tester.pumpAndSettle();
    expect(find.text('356 · Sedes documentadas'), findsOneWidget);
    final selector = find.byType(DropdownButtonFormField<String>);
    await tester.ensureVisible(selector);
    await tester.tap(selector);
    await tester.pumpAndSettle();
    await tester.tap(find.text('Iztapalapa').last);
    await tester.pumpAndSettle();
    comprobar();
  });

  testWidgets('la cartografía fallida conserva consulta por lista', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: MapScreen(
            dataFuture: Future.value([
              const AlcaldiaData(
                name: 'Iztapalapa',
                period: '2020',
                total: 1835486,
                children: 103148,
                children14: 366835,
                olderAdults: 262064,
                source: 'INEGI, Censo 2020 (ITER)',
                dataType: 'observado',
              ),
            ]),
            geometryFuture: Future.value('{"type":"FeatureCollection","features":[]}'),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(
      find.textContaining('Puedes seguir consultando por la lista'),
      findsOneWidget,
    );
  });

  testWidgets('avanza la búsqueda demo', (tester) async {
    await tester.pumpWidget(ObservatorioApp(
      matchingExecutor: ({
        required String type,
        required String start,
        required String end,
        required List<String> days,
        required double radiusKm,
      }) async => {
        'demo': true,
        'results': [
          {
            'estado': 'recomendada',
            'motivo': 'compatible',
            'distancia_km': 0.0,
          },
        ],
      },
    ));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('nav_busqueda')));
    await tester.pumpAndSettle();
    expect(find.text('Paso 1 de 4 · Servicio'), findsOneWidget);

    await tester.tap(find.text('Continuar'));
    await tester.pumpAndSettle();
    expect(find.text('Paso 2 de 4 · Horario'), findsOneWidget);

    await tester.tap(find.text('Atrás'));
    await tester.pumpAndSettle();
    expect(find.text('Paso 1 de 4 · Servicio'), findsOneWidget);

    await tester.tap(find.text('Continuar'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Continuar'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Ver resultados'));
    await tester.pumpAndSettle();
    expect(find.text('Recomendación sintética'), findsOneWidget);

    await tester.ensureVisible(find.text('Restablecer'));
    await tester.tap(find.text('Restablecer'));
    await tester.pumpAndSettle();
    expect(find.text('Paso 1 de 4 · Servicio'), findsOneWidget);
  });

  testWidgets('compara cifras territoriales cargadas', (tester) async {
    final raw = File('assets/data/directorio_infantil.json').readAsStringSync();
    final grupos = (jsonDecode(raw) as Map).cast<String, Map<String, dynamic>>();
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: CompareScreen(
            ofertaFuture: Future.value(grupos),
            dataFuture: Future.value([
              const AlcaldiaData(
                name: 'Iztapalapa',
                period: '2020',
                total: 1835486,
                children: 103148,
                children14: 366835,
                olderAdults: 262064,
                source: 'INEGI, Censo 2020 (ITER)',
                dataType: 'observado',
              ),
              const AlcaldiaData(
                name: 'Benito Juárez',
                period: '2020',
                total: 434153,
                children: 16642,
                children14: 51243,
                olderAdults: 87344,
                source: 'INEGI, Censo 2020 (ITER)',
                dataType: 'observado',
              ),
            ]),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('Compara dos alcaldías'), findsOneWidget);
    expect(find.text('Iztapalapa · 88 %'), findsOneWidget);
    expect(find.text('37 de 42 sedes documentadas tienen horario publicado.'), findsOneWidget);
    final segundo = find.byType(DropdownButtonFormField<String>).last;
    await tester.ensureVisible(segundo);
    await tester.tap(segundo);
    await tester.pumpAndSettle();
    await tester.tap(find.text('Cuauhtémoc').last);
    await tester.pumpAndSettle();
    expect(find.text('Cuauhtémoc · 50 %'), findsOneWidget);
    expect(find.text('21 de 42 sedes documentadas tienen horario publicado.'), findsOneWidget);
    expect(
      find.text('Personas por cada 100 habitantes · Censo 2020 observado'),
      findsOneWidget,
    );
  });

  testWidgets('calcula el simulador mediante el servicio inyectado', (tester) async {
    await tester.pumpWidget(ObservatorioApp(
      simulatorExecutor: (parameters) async => {
        'demo': true,
        'b2b': {
          'ahorro_bruto': 120000.0,
          'beneficio_neto': null,
        },
        'b2g': {
          'isn_impuesto': 1000.0,
          'imss_patronal': 2000.0,
          'infonavit_aportacion': 500.0,
        },
      },
    ));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const Key('nav_simuladores')));
    await tester.pumpAndSettle();
    await tester.ensureVisible(find.text('Calcular escenario'));
    await tester.tap(find.text('Calcular escenario'));
    await tester.pumpAndSettle();
    expect(find.textContaining('Beneficio neto: no calculable'), findsOneWidget);
  });

  testWidgets('mantiene el shell en los anchos objetivo', (tester) async {
    for (final width in [360.0, 390.0, 768.0, 1440.0]) {
      tester.view
        ..physicalSize = Size(width, 800)
        ..devicePixelRatio = 1;
      await tester.pumpWidget(const ObservatorioApp());
      await tester.pumpAndSettle();
      expect(find.text('Economía del cuidado en CDMX'), findsOneWidget);
    }
    tester.view.resetPhysicalSize();
    tester.view.resetDevicePixelRatio();
  });
}
