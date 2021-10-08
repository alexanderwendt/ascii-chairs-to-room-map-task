The following program has been written to solve an exercise in text handling. The task is to get a room plan as ascii
text and assign chairs to a certain room based on the ascii map with rooms
and postions for chairs. The challenge is to use the ascii map to map the chairs to a certain room, even if the room shape is like a 'u'

The room structure looks like this:

+-----------+------------------------------------+
|           |                             S      |
| (office)  |         (living room)              |
|         P |                                    |
+--------------------------+---------------------+
                           |  (balcony)          | 
                           |                 P   | 
                           +---------------------+
						   
Chairs have the characters W, C, P, S and the room names are written in the following format: ([ROOM NAME])

The task was solved by using an ascii agent with one field of vision. The vision could look like this.

 ['+' ' ' ' ']
 ['+' '0' ' ']
 ['+' '+' '+']
 
 
where + are walls and 0 is the room id. It goes through each room like an autonomous vacuum cleaner to map each room to a room id.

The following steps were made to create a room map:
1. start at any point in the room
2. turn right and move to the right to the first wall
3. at the wall, assign the room a global room id. In case a room id was already found, that room id was used instead
4. use the "right rule" to go through the room, always turning to the right and at each empty field, assign that room the room id
5. eventually the whole gets mapped and the next room is done

A finished map of the room looks like this:

Final room map:
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+00000000000+111111111111111111111111111111111111+22222222222222222222222+
+00000000000+111111111111111111111111111111111111+22222222222222222222222+
+00000000000+111111111111111111111111111111111111+22222222222222222222222+
+00000000000+111111111111111111111111111111111111+22222222222222222222222+
+00000000000+111111111111111111111111111111111111+22222222222222222222222+
+00000000000+111111111111111111111111111111111111+22222222222222222222222+
+++++++++++++11111111111111+++++++++++11111111111+++++++++++++++++++++++++
+33333333333+11111111111111+333333333+11111111111+3333333333+444444444444+
+33333333333+11111111111111+333333333+11111111111+3333333333+444444444444+
+33333333333+11111111111111+333333333+11111111111+3333333333+444444444444+
+33333333333++++++++++++++++333333333+++++++++++++3333333333+444444444444+
+333333333333333333333333333333333333+55555555555+3333333333+444444444444+
+333333333333333333333333333333333333+55555555555+3333333333+444444444444+
+333333333333333333333333333333333333+55555555555+3333333333+444444444444+
++++++++++++++++33333333333+++++++++++55555555555+3333333333+444444444444+
+66666666666666+33333333333+555555555555555555555+3333333333+444444444444+
+66666666666666+33333333333+555555555555555555555+3333333333+444444444444+
+66666666666666+33333333333+555555555555555555555+3333333333+444444444444+
+66666666666666+33333333333+555555555555555555555+3333333333+444444444444+
++++++++++++++++33333333333+++++++++++++++++++++++3333333333++++++++++++++
+77777777777777+33333333333+888888888888888888888+3333333333+999999999999+
+77777777777777+33333333333+888888888888888888888+3333333333+999999999999+
+77777777777777+33333333333+888888888888888888888+3333333333+999999999999+
+77777777777777+33333333333+888888888888888888888+3333333333+999999999999+
+77777777777777+33333333333+888888888888888888888+3333333333+999999999999+
+77777777777777+33333333333+888888888888888888888+3333333333+999999999999+
+77777777777777+33333333333+888888888888888888888+3333333333+999999999999+
+77777777777777+33333333333+888888888888888888888+3333333333+999999999999+
+7777777777777+333333333333+++++++++++++++++++++++3333333333+999999999999+
+777777777777+3333333333333333333333333333333333333333333333+999999999999+
+77777777777+33333333333333333333333333333333333333333333333+999999999999+
+7777777777+333333333333333333333333333333333333333333333333+999999999999+
+++++++++++3333333333333333333333333333333333333333333333333+999999999999+
+33333333333333333333333333333333333333333333333333333333333+999999999999+
+333333333333333333333333333333333333333333333333+++++++++++++++++++++++++

Then, for each room, the chairs and room names are mapped to a room id.

The result of the program is a list returns the number of different chair types for the appartment,
the number of different chair types per room. The output should look like this, sorted in alphabethically order:

total:
W: 4, P: 0, S: 2, C: 1
living room:
W: 3, P: 0, S: 2, C: 1
office:
W: 1, P: 0, S: 0, C: 0

Usage: python main.py --map_path=task_map/rooms_extended.txt --output=result_rooms_extended.txt

parser.add_argument("-p", '--map_path', default='task_map/rooms_test.txt',
                    help='Input rooms file', required=False)
parser.add_argument("-o", '--output', default='result.txt',
                   help='Save output file path', required=False)
