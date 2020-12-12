import 'dart:async';
import 'package:flutter/material.dart';
import 'models.dart';
import 'api.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Daily Picture',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(
        title: 'Daily Picture Demo',
        key: UniqueKey(),
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  DailyPictureAPI _api;
  StreamController<List<Map<String, dynamic>>> _controller;
  Stream<List<Map<String, dynamic>>> _stream;
  List<Map<String, dynamic>> _data;
  
  final TextEditingController _textEditingController = TextEditingController();
  bool _showSendButton = false;

  @override
  void initState() {
    _api = DailyPictureAPI();
    _data = [];
    _controller = StreamController<List<Map<String, dynamic>>>();
    _stream = _controller.stream;
    _textEditingController.addListener(() {
      setState(() {
        _showSendButton = _textEditingController.text.length > 0;
      });
    });
    super.initState();
  }

  void _addPicture(query) async {
    var response = await _api.pullImage(query);
    // var response = {'url': 'http://images.dailypicture.xyz/f2d168293fed0e1a9599e4899.jpeg', 'thumbnail': 'http://images.dailypicture.xyz/f2d168293fed0e1a9599e4899.jpeg'};
    _data.add(response);
    _controller.add(_data);
  }

  void _clearPictures() {
    _data.clear();
    _controller.add(_data);
  }

  GridView _pictureGrid(List<Map<String, dynamic>> data){
    List<Picture> list;
    list = _data.map((json) => Picture.fromJSON(json)).toList();
    return GridView.count(
      crossAxisCount: 5,
      children: list,
      );
  }

  Widget _getSendButton(){
    if (_showSendButton) {
      return IconButton(
        icon: Icon(Icons.add_photo_alternate),
        onPressed: () => {
          _addPicture(_textEditingController.text)
        },
      );
    } else {
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
            children: [Container(
              height: 50,
              width: 300,
              child: TextField(
                controller: _textEditingController,
                decoration: InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'What would you like to see?',
                  floatingLabelBehavior: FloatingLabelBehavior.never,
                  suffixIcon: _getSendButton(), 
                ),
              ),
            ),
            Container(
              height: 50,
              width: 120,
              child: ElevatedButton(
                child: Text('Clear Pictures'),
                onPressed: () => _clearPictures(),
              ),
            ),]
            ),
            Expanded(
              child: StreamBuilder<List<Map<String, dynamic>>>(
                initialData: _data,
                stream: _stream,
                builder: (BuildContext context, AsyncSnapshot<List<Map<String, dynamic>>> snapshot) {
                  if (snapshot.hasError) {
                    return Icon(Icons.error);
                  }
                  if (snapshot.hasData) {
                    return _pictureGrid(snapshot.data);
                  } else {
                    return CircularProgressIndicator();
                  }
                },
              ),
            ),
          ]),
    );
  }
}
