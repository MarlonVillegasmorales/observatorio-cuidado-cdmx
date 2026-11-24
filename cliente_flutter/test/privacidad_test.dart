import 'dart:convert';
import 'dart:io';

import 'package:cliente_flutter/main.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  for (final width in [360.0, 1440.0]) {
    testWidgets('Privacidad por tarjeta y menú a ${width}px', (tester) async {
      rootBundle.evict('assets/privacidad/aviso.json');
      final messenger = tester.binding.defaultBinaryMessenger;
      messenger.setMockMessageHandler('flutter/assets', (message) async {
        final key = utf8.decode(message!.buffer.asUint8List(message.offsetInBytes, message.lengthInBytes));
        final file = File('build/unit_test_assets/$key');
        return file.existsSync() ? ByteData.sublistView(file.readAsBytesSync()) : null;
      });
      addTearDown(() => messenger.setMockMessageHandler('flutter/assets', null));
      tester.view..physicalSize = Size(width, 800)..devicePixelRatio = 1;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);
      await tester.pumpWidget(const ObservatorioApp());
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump();

      final tarjeta = find.text('Cómo usamos los datos');
      await tester.ensureVisible(tarjeta);
      await tester.tap(tarjeta);
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump();
      expect(find.text('Datos del mapa y del directorio'), findsOneWidget);
      expect(find.text('Datos de las demostraciones'), findsOneWidget);
      final documento = find.text('Documentación del piloto');
      await tester.scrollUntilVisible(documento, 250, scrollable: find.byType(Scrollable).last);
      expect(find.textContaining('Versión 1.0'), findsOneWidget);
      await tester.pageBack();
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump();
      await tester.tap(find.byTooltip('Menú de información'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump();
      await tester.tap(find.text('Privacidad y uso de datos'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump();
      expect(find.text('Datos del mapa y del directorio'), findsOneWidget);
      expect(tester.takeException(), isNull);
    });
  }
}
