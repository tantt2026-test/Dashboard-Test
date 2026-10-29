import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

import 'data/report_repository.dart';
import 'ui/theme.dart';
import 'ui/turnover_page.dart';

void main() {
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
      home: TurnoverPage(repo: repo),
    );
  }
}
