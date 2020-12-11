
import 'package:dio/dio.dart';
import 'dart:convert';

class DailyPictureAPI {
  BaseOptions options = BaseOptions(
      baseUrl: 'https://api.dailypicture.xyz',
    );
    
  Dio dio = Dio();

  DailyPictureAPI() {
    dio = Dio(options);
  }
  
  //call pull image api and return thumbnail and image url
  Future<Map<String, dynamic>> pullImage(String query) async {
      Response response;

      const url = '/pull_image';
      final body = {"query": query};
      try {
        response = await dio.post(
          url,
          data: body,
          options: Options(
            headers: {
              Headers.contentTypeHeader: "application/json",
              },
          ),
          );
      } on DioError catch(e, st){
        print(e);
        print(st);
      }
      Map<String, dynamic> imageUrls;
      imageUrls = json.decode(response.data);
      print(imageUrls);
      return imageUrls;

  }

}