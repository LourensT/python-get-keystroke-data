# python-get-keystroke-data
Simple program to collect keystroke data.

![Image of GUI](https://github.com/LourensT/python-get-keystroke-data/blob/master/GUI.PNG)

# Output
CSV file with the following rows:
(char, time, up/down),(char, time, up/down),(char, time, up/down)

example of output for an entry typing 'Thanks':
`('shift', 0, 'down'),"('T', 78, 'down')","('shift', 125, 'up')","('h', 187, 'down')","('t', 203, 'up')","('a', 265, 'down')","('h', 281, 'up')","('a', 390, 'up')","('n', 390, 'down')","('k', 453, 'down')","('n', 531, 'up')","('s', 546, 'down')","('k', 562, 'up')","('s', 609, 'up')"`
