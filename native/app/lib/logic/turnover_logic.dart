// Phần còn lại của build_turnover_report (App.py) chạy trên app:
// lọc NV, sắp xếp, dòng Tổng, % MTD, GAP, Bình quân ngày, Nhận xét Top/Bottom.
// Số gốc từng NV (Chỉ tiêu, MTD, Thực hiện ngày) do Python tính sẵn trong JSON.
// Mọi thay đổi ở đây phải chạy lại pipeline/parity_check.py.
import 'pyfmt.dart';

const allNvLabel = 'Tất cả ĐDKD';

class Timegone {
  final int total, elapsed, remain;
  final double pct;
  Timegone(this.total, this.elapsed, this.remain, this.pct);
  factory Timegone.fromJson(Map<String, dynamic> j) => Timegone(
      j['total'] as int, j['elapsed'] as int, j['remain'] as int, (j['pct'] as num).toDouble());
}

class RawNvRow {
  final String code, name;
  final double target, today, mtd;
  RawNvRow(this.code, this.name, this.target, this.today, this.mtd);
  factory RawNvRow.fromJson(Map<String, dynamic> j) => RawNvRow(
        j['code'] as String,
        j['name'] as String,
        (j['target'] as num).toDouble(),
        (j['today'] as num).toDouble(),
        (j['mtd'] as num).toDouble(),
      );
}

class TurnoverDay {
  final Timegone timegone;
  final List<RawNvRow> rows;
  TurnoverDay(this.timegone, this.rows);
}

class TurnoverMonth {
  final String monthKey, monthLabel, title, salaryLabel, totalLabel;
  final int year, month;
  final String? dataMaxDate;
  final List<String> nv;
  final Map<String, TurnoverDay> days;

  TurnoverMonth({
    required this.monthKey,
    required this.monthLabel,
    required this.title,
    required this.salaryLabel,
    required this.totalLabel,
    required this.year,
    required this.month,
    required this.dataMaxDate,
    required this.nv,
    required this.days,
  });

  factory TurnoverMonth.fromJson(Map<String, dynamic> j) {
    final days = <String, TurnoverDay>{};
    (j['days'] as Map<String, dynamic>).forEach((k, v) {
      final d = v as Map<String, dynamic>;
      days[k] = TurnoverDay(
        Timegone.fromJson(d['timegone'] as Map<String, dynamic>),
        [for (final r in d['rows'] as List) RawNvRow.fromJson(r as Map<String, dynamic>)],
      );
    });
    return TurnoverMonth(
      monthKey: j['month_key'] as String,
      monthLabel: j['month_label'] as String,
      title: j['title'] as String,
      salaryLabel: (j['salary_label'] ?? '') as String,
      totalLabel: (j['total_label'] ?? '') as String,
      year: j['year'] as int,
      month: j['month'] as int,
      dataMaxDate: j['data_max_date'] as String?,
      nv: [for (final n in j['nv'] as List) n as String],
      days: days,
    );
  }
}

/// Một dòng bảng — các cột giống Streamlit.
class TurnoverRow {
  final String stt, code, name;
  final double target, today, mtd, gap, bq;
  final String pctLabel; // "64.6%"
  final double pct;
  final bool isTotal;
  TurnoverRow({
    required this.stt,
    required this.code,
    required this.name,
    required this.target,
    required this.today,
    required this.mtd,
    required this.pct,
    required this.pctLabel,
    required this.gap,
    required this.bq,
    this.isTotal = false,
  });

  /// Chuỗi hiển thị y như df_display của Streamlit.
  Map<String, String> display() => {
        'STT': stt,
        'Tên NVBH': name,
        'Chỉ Tiêu Doanh Số': vnNumber(target),
        'Thực Hiện Ngày': vnNumber(today),
        'Doanh Số MTD': vnNumber(mtd),
        '% MTD': pctLabel,
        'GAP': vnNumber(gap),
        'Bình quân ngày': vnNumber(bq, 1),
      };
}

class TurnoverReport {
  final List<TurnoverRow> rows; // không gồm dòng tổng
  final TurnoverRow total;
  final double teamTarget;
  final Timegone timegone;
  final String filterLabel;
  final String top3Text, bottom3Text;
  TurnoverReport(this.rows, this.total, this.teamTarget, this.timegone, this.filterLabel,
      this.top3Text, this.bottom3Text);

  /// Mốc tô màu cột %: set_color_moc_for_kpi('TURNOVER') = min(Timegone, 95).
  double get colorMoc => timegone.pct < 95.0 ? timegone.pct : 95.0;

  /// Nội dung "NHẬN XÉT & ĐÁNH GIÁ" — App.py dùng dấu phẩy ngăn nghìn ở đây.
  String get resultText =>
      'Đạt ${pyThousands(total.mtd, 0)} / ${pyThousands(teamTarget, 0)} VNĐ '
      '(${total.pctLabel} MTD). Thực hiện ngày: ${pyThousands(total.today, 0)} VNĐ.';
}

enum PctColor { red, green, purple }

/// color_pct_bg của App.py.
PctColor pctColor(double v, double moc) {
  if (v < moc) return PctColor.red;
  if (v <= moc + 5) return PctColor.green;
  return PctColor.purple;
}

bool nvSelected(List<String> filter) => filter.isNotEmpty && !filter.contains(allNvLabel);

/// _gap_and_bq_day(target, mtd, remain_days, as_int=False)
(double, double) gapAndBq(double target, double mtd, int remainDays) {
  final gap = target - mtd;
  final bq = remainDays > 0 ? gap / remainDays : gap;
  return (gap, pyRound(bq, 1));
}

TurnoverReport buildTurnover(TurnoverMonth month, String isoDate, List<String> filterNv) {
  final day = month.days[isoDate];
  if (day == null) {
    throw ArgumentError('Không có dữ liệu ngày $isoDate');
  }
  final remain = day.timegone.remain;
  final filtered = nvSelected(filterNv);

  var src = day.rows;
  if (filtered) {
    final want = filterNv.map((e) => e.trim()).toSet();
    src = src.where((r) => want.contains(r.name) || want.contains(r.code)).toList();
  }
  // Python: duyệt all_sms (mã NV đã sort), rồi sort_values('_ratio') tăng dần.
  final byCode = stableSorted<RawNvRow>(src, (a, b) => a.code.compareTo(b.code));
  double ratio(RawNvRow r) => r.target != 0 ? r.mtd / r.target : 0.0;
  final sorted = stableSorted<RawNvRow>(byCode, (a, b) => ratio(a).compareTo(ratio(b)));

  final rows = <TurnoverRow>[];
  for (var i = 0; i < sorted.length; i++) {
    final r = sorted[i];
    final pct = r.target != 0 ? pyRound(r.mtd / r.target * 100, 1) : 0.0;
    final (gap, bq) = gapAndBq(r.target, r.mtd, remain);
    rows.add(TurnoverRow(
      stt: '${i + 1}',
      code: r.code,
      name: r.name,
      target: r.target,
      today: r.today,
      mtd: r.mtd,
      pct: pct,
      pctLabel: '${pyStr(pct)}%',
      gap: gap,
      bq: bq,
    ));
  }

  final totalMtd = npSum([for (final r in rows) r.mtd]);
  final totalToday = npSum([for (final r in rows) r.today]);
  final teamTgt = npSum([for (final r in rows) r.target]);
  final totalPct = teamTgt != 0 ? pyRound(totalMtd / teamTgt * 100, 1) : 0.0;
  final (tGap, tBq) = gapAndBq(teamTgt, totalMtd, remain);
  final label = filtered ? filterNv.join(', ') : allNvLabel;
  final total = TurnoverRow(
    stt: '-',
    code: 'TỔNG CỘNG',
    name: filtered ? label : month.totalLabel,
    target: teamTgt,
    today: totalToday,
    mtd: totalMtd,
    pct: totalPct,
    pctLabel: '${pyStr(totalPct)}%',
    gap: tGap,
    bq: tBq,
    isTotal: true,
  );

  // Nhận xét: sort theo % đã làm tròn (như App.py đọc lại cột '% MTD'), giảm dần, bằng nhau giữ thứ tự gốc.
  double shown(TurnoverRow r) => double.tryParse(r.pctLabel.replaceAll('%', '')) ?? r.pct;
  final byPct = stableSorted<TurnoverRow>(rows, (a, b) => shown(b).compareTo(shown(a)));
  final top3 = byPct.take(3).toList();
  final bottom3 = byPct.length <= 3 ? byPct.reversed.toList() : byPct.sublist(byPct.length - 3).reversed.toList();
  String fmt(List<TurnoverRow> l) => l.map((r) => '${r.name} (${r.pctLabel})').join(', ');

  return TurnoverReport(rows, total, teamTgt, day.timegone, label, fmt(top3), fmt(bottom3));
}

/// Ngày mặc định giống Streamlit: hôm qua (giờ VN), kẹp trong tháng.
String defaultReportDate(TurnoverMonth m, DateTime nowUtc) {
  final vn = nowUtc.add(const Duration(hours: 7));
  final t1 = DateTime.utc(vn.year, vn.month, vn.day).subtract(const Duration(days: 1));
  final start = DateTime.utc(m.year, m.month, 1);
  final end = DateTime.utc(m.year, m.month + 1, 1).subtract(const Duration(days: 1));
  var d = t1;
  if (d.isBefore(start)) d = start;
  if (d.isAfter(end)) d = end;
  return isoDate(d);
}

String isoDate(DateTime d) =>
    '${d.year.toString().padLeft(4, '0')}-${d.month.toString().padLeft(2, '0')}-${d.day.toString().padLeft(2, '0')}';
