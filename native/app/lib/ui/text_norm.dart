// Chuẩn hoá chữ để tìm kiếm không dấu: "Lê Thị Thơm" ~ "le thi thom".
const _from = 'àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ';
const _to = 'aaaaaaaaaaaaaaaaaeeeeeeeeeeeiiiiiooooooooooooooooouuuuuuuuuuuyyyyyd';

final Map<int, int> _map = {
  for (var i = 0; i < _from.length; i++) _from.codeUnitAt(i): _to.codeUnitAt(i),
};

String fold(String s) {
  final lower = s.toLowerCase();
  final out = StringBuffer();
  for (final c in lower.codeUnits) {
    out.writeCharCode(_map[c] ?? c);
  }
  return out.toString();
}
