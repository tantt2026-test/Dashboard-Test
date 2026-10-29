import '../logic/turnover_logic.dart';
import 'theme.dart';

String _hex(int argb) => '#${(argb & 0xFFFFFF).toRadixString(16).padLeft(6, '0')}';

/// Bảng Turnover → cùng định dạng bảng của report_doc.py để dùng chung ReportTable
/// (tự co theo màn hình, căn giữa, lọc, toàn màn hình). Cột % tô màu theo mốc như Streamlit.
Map<String, dynamic> turnoverTableData(TurnoverReport report) {
  const cols = [
    'STT', 'Tên NVBH', 'Chỉ Tiêu Doanh Số', 'Thực Hiện Ngày',
    'Doanh Số MTD', '% MTD', 'GAP', 'Bình quân ngày',
  ];
  final moc = report.colorMoc;
  Map<String, dynamic> row(TurnoverRow r) {
    final d = r.display();
    final (bg, fg) = pctColors(pctColor(r.pct, moc));
    return {
      'cells': [
        for (final c in cols)
          {
            'x': d[c]!,
            if (c == '% MTD') ...{'bg': _hex(bg.toARGB32()), 'fg': _hex(fg.toARGB32()), 'b': 1},
            if (c == 'Tên NVBH') 'b': 1,
            if (r.isTotal && c != '% MTD') ...{'bg': '#1a365d', 'fg': '#ffffff', 'b': 1},
          }
      ]
    };
  }

  return {
    't': 'tbl',
    'fz': 2,
    'h': [
      [for (final c in cols) {'x': c, 'b': 1}]
    ],
    'b': [
      for (final r in [...report.rows, report.total]) row(r)['cells']
    ],
  };
}
