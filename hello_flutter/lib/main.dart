import 'package:flutter/material.dart';
import 'package:hello_flutter/pages/gradient_container.dart';

void main() {
  runApp(
    MaterialApp(
      home: Scaffold(
        //backgroundColor: Color.fromARGB(255, 118, 98, 145),
        //scaffold back ground color pick
        //container used for styling and layout settings
        body: GradientContainer(),
      ),
    ),
  );
}

// NOTES

// backgroundColor: Color.fromARGB(255, 118, 98, 145) -> scaffold does not provide gradient

// MULTI LINE
