import 'package:flutter_app/api.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  DailyPictureAPI api;
  setUp(() => api = DailyPictureAPI());
  test('Daily Picture API responds to pull image request.', () async {
    var response = await api.pullImage('cat');
    print(response);
    assert(response.isNotEmpty);
  });
}