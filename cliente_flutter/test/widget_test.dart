import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';

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

  testWidgets('navega a mapa y permite seleccionar una alcaldía', (tester) async {
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
  });

  testWidgets('avanza la búsqueda demo', (tester) async {
    await tester.pumpWidget(const ObservatorioApp());
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
    expect(find.text('Ejemplo sintético predefinido'), findsOneWidget);

    await tester.ensureVisible(find.text('Restablecer'));
    await tester.tap(find.text('Restablecer'));
    await tester.pumpAndSettle();
    expect(find.text('Paso 1 de 4 · Servicio'), findsOneWidget);
  });

  testWidgets('compara cifras territoriales cargadas', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: CompareScreen(
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
    expect(
      find.text('Personas por cada 100 habitantes · Censo 2020 observado'),
      findsOneWidget,
    );
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
