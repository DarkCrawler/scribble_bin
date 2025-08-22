import 'package:flutter/material.dart';

import '../widgets/styled_text_temp.dart';

class GradientContainer extends StatelessWidget {
  @override
  Widget build(context) {
    // TODO: implement build
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            Color.fromARGB(255, 68, 51, 97),
            Color.fromARGB(68, 51, 97, 100),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Center(child: StyledTextTemp()),
    );
    //throw UnimplementedError();
  }
}
