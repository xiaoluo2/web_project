import 'package:url_launcher/url_launcher.dart';
import 'package:flutter/material.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter/widgets.dart';

class Picture extends StatelessWidget {
  final String url;
  final String thumbnail;

  Picture({
    @required this.thumbnail,
    @required this.url,
  });

  factory Picture.fromJSON(Map<String, dynamic> json) {
    return Picture(url: json['url'], thumbnail: json['thumbnail']);
  }

  void _launchUrl(String url) async {
    if (await canLaunch(url)) {
      await (launch(url));
    } else {
      throw 'Could not launch $url';
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: () => _launchUrl(url),
      child: Container(
        margin: const EdgeInsets.all(5),
        child: CachedNetworkImage(
          imageUrl: thumbnail,
          placeholder: (context, url) => CircularProgressIndicator(),
          errorWidget: (context, url, error) => Icon(Icons.error),
        ),
      ),
    );
  }
}
