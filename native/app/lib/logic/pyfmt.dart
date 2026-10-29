// Làm tròn / format số GIỐNG HỆT Python (App.py) để số trên app khớp Streamlit.
//
// - Python round(x, n) và f'{x:.nf}' làm tròn theo giá trị nhị phân chính xác,
//   trường hợp đúng .5 thì về số chẵn (banker's rounding).
//   Dart toStringAsFixed làm tròn .5 lên → phải xử lý riêng ca hoà.
// - pandas Series.sum() dùng pairwise summation của numpy → cộng đúng thứ tự numpy.
// Không import Flutter: tool/parity_cli.dart chạy file này bằng `dart run`.
import 'dart:typed_data';

/// x * 10^nd có đúng bằng k + 0.5 (chính xác tuyệt đối) không.
bool _isExactHalf(double x, int nd) {
  if (!x.isFinite) return false;
  final bd = ByteData(8)..setFloat64(0, x.abs());
  final bits = bd.getUint64(0);
  final expBits = (bits >> 52) & 0x7ff;
  final frac = bits & 0xfffffffffffff;
  final BigInt m;
  final int e;
  if (expBits == 0) {
    m = BigInt.from(frac);
    e = -1074;
  } else {
    m = BigInt.from(frac | (1 << 52));
    e = expBits - 1075;
  }
  // y = 2 * x * 10^nd = m * 10^nd * 2^(e+1); hoà khi y là số nguyên lẻ.
  final num = m * BigInt.from(10).pow(nd);
  final k = -(e + 1);
  if (k <= 0) {
    return k == 0 && num.isOdd;
  }
  final div = BigInt.one << k;
  if (num % div != BigInt.zero) return false;
  return (num ~/ div).isOdd;
}

/// Chuỗi x làm tròn nd chữ số thập phân, giống f'{x:.{nd}f}' của Python.
String pyFixed(double x, int nd) {
  if (!x.isFinite) return x.toString();
  var s = x.toStringAsFixed(nd);
  if (_isExactHalf(x, nd)) {
    // toStringAsFixed đã làm tròn ra xa 0; nếu kết quả lẻ thì lùi về chẵn.
    final neg = s.startsWith('-');
    final digits = s.replaceAll('-', '').replaceAll('.', '');
    final last = int.parse(digits[digits.length - 1]);
    if (last.isOdd) {
      final v = BigInt.parse(digits) - BigInt.one;
      var d = v.toString().padLeft(nd + 1, '0');
      if (nd > 0) d = '${d.substring(0, d.length - nd)}.${d.substring(d.length - nd)}';
      s = (neg ? '-' : '') + d;
    }
  }
  return s;
}

/// Python round(x, nd) → double.
double pyRound(double x, int nd) => double.parse(pyFixed(x, nd));

/// Python str(float) cho số % thông thường (37.3 → "37.3", 100.0 → "100.0").
String pyStr(double x) {
  if (x == x.truncateToDouble() && x.abs() < 1e16) {
    if (x == 0 && x.isNegative) return '-0.0';
    return '${x.toInt()}.0';
  }
  return x.toString();
}

/// f'{x:,.{nd}f}' (dấu phẩy ngăn cách nghìn).
String pyThousands(double x, int nd) {
  final s = pyFixed(x, nd);
  final neg = s.startsWith('-');
  final body = neg ? s.substring(1) : s;
  final dot = body.indexOf('.');
  final intPart = dot >= 0 ? body.substring(0, dot) : body;
  final decPart = dot >= 0 ? body.substring(dot) : '';
  final buf = StringBuffer();
  for (var i = 0; i < intPart.length; i++) {
    if (i > 0 && (intPart.length - i) % 3 == 0) buf.write(',');
    buf.write(intPart[i]);
  }
  return '${neg ? '-' : ''}$buf$decPart';
}

/// f'{x:,.{nd}f}'.replace(',', '.') — cách App.py hiển thị số trong bảng/card.
String vnNumber(double x, [int nd = 0]) => pyThousands(x, nd).replaceAll(',', '.');

/// numpy pairwise_sum (dùng bởi pandas Series.sum) cho mảng float64.
double npSum(List<double> a) => _pairwise(a, 0, a.length);

double _pairwise(List<double> a, int start, int n) {
  if (n < 8) {
    var res = 0.0;
    for (var i = 0; i < n; i++) {
      res += a[start + i];
    }
    return res;
  } else if (n <= 128) {
    final r = List<double>.generate(8, (j) => a[start + j]);
    var i = 8;
    for (; i < n - (n % 8); i += 8) {
      for (var j = 0; j < 8; j++) {
        r[j] += a[start + i + j];
      }
    }
    var res = ((r[0] + r[1]) + (r[2] + r[3])) + ((r[4] + r[5]) + (r[6] + r[7]));
    for (; i < n; i++) {
      res += a[start + i];
    }
    return res;
  } else {
    var n2 = n ~/ 2;
    n2 -= n2 % 8;
    return _pairwise(a, start, n2) + _pairwise(a, start + n2, n - n2);
  }
}

/// Sắp xếp ổn định (giữ thứ tự ban đầu khi bằng nhau) — giống pandas với ≤16 dòng.
List<T> stableSorted<T>(List<T> items, int Function(T a, T b) cmp) {
  final idx = List<int>.generate(items.length, (i) => i);
  idx.sort((i, j) {
    final c = cmp(items[i], items[j]);
    return c != 0 ? c : i.compareTo(j);
  });
  return [for (final i in idx) items[i]];
}
