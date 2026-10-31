import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'data/local_engine.dart';
import 'data/report_repository.dart';
import 'ui/theme.dart';
import 'ui/app_scale.dart';
import 'ui/home_shell.dart';

final appScale = AppScale();

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // Nhật ký (app Mac: Application Support/KPI Dashboard/filter.log): mở app + lỗi → dò khi app tự tắt
  LocalEngine.instance.log('app mở $appVersion', const {}, null);
  FlutterError.onError = (d) {
    LocalEngine.instance.log('lỗi giao diện: ${d.exceptionAsString()}', const {}, null);
    FlutterError.presentError(d);
  };
  PlatformDispatcher.instance.onError = (e, st) {
    LocalEngine.instance.log('lỗi: $e | ${st.toString().split('\n').take(4).join(' / ')}', const {}, null);
    return true;
  };
  await appScale.load();
  runApp(const KpiApp());
}

class KpiApp extends StatefulWidget {
  const KpiApp({super.key});

  @override
  State<KpiApp> createState() => _KpiAppState();
}

class _KpiAppState extends State<KpiApp> {
  final repo = ReportRepository();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'KPI Dashboard',
      debugShowCheckedModeBanner: false,
      theme: buildTheme(),
      locale: const Locale('vi'),
      supportedLocales: const [Locale('vi'), Locale('en')],
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      builder: (ctx, child) => ScaledApp(scale: appScale, child: child!),
      home: HomeShell(repo: repo),
    );
  }
}
