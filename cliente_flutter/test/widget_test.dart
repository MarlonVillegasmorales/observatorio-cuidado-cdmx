import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/material.dart';

import 'package:cliente_flutter/main.dart';

void main() {
  testWidgets('muestra la pantalla de inicio y cinco destinos', (tester) async {
    await tester.pumpWidget(const ObservatorioApp());

    expect(find.text('Economía del cuidado en CDMX'), findsOneWidget);
    expect(find.text('Explorar mapa'), findsOneWidget);
    expect(find.text('Búsqueda'), findsOneWidget);
    expect(find.text('Proyecto'), findsOneWidget);
  });

  testWidgets('navega a mapa y permite seleccionar una alcaldía', (tester) async {
    await tester.pumpWidget(const ObservatorioApp());

    await tester.tap(find.text('Mapa'));
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
    await tester.tap(find.text('Búsqueda'));
    await tester.pumpAndSettle();
    expect(find.text('Paso 1 de 4 · Servicio'), findsOneWidget);

    await tester.tap(find.text('Continuar'));
    await tester.pumpAndSettle();
    expect(find.text('Paso 2 de 4 · Horario'), findsOneWidget);
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
