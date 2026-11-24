import 'package:web/web.dart' as web;

void descargarAviso(String archivo) {
  final enlace = web.HTMLAnchorElement()
    ..href = Uri.base.resolve('assets/assets/privacidad/$archivo').toString()
    ..download = archivo;
  enlace.click();
}
