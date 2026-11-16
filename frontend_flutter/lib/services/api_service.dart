import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // 10.0.2.2 is the special localhost alias for Android emulators to talk to your PC's FastAPI server
  final String baseUrl = "http://10.0.2.2:8000"; 

  Future<String> queryRag(String prompt) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/query'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"query": prompt}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['response'] ?? "No response received.";
      } else {
        return "Error: Server returned status code ${response.statusCode}";
      }
    } catch (e) {
      return "Error: Could not connect to backend.";
    }
  }
}