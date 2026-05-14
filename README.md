# StreamMaster
Streaming utility for OBS studio, specialized in TEKKEN 8 & STREET FIGHTER 6 streams. You can customize to add a specific game.

DISCLAIMER:
I'm new to coding. For this software whenever I was stuck or something wasn't working out like it should used AI to debug and problem solving. For art and graphics no type of AI was involved. As well, photoshop editable files (.psd) are present in the images folder for full transparency.

HOW TO USE: <br>
These are html files that OBS reads and you manage through the executable file. 

In order to OBS to show them, create a new scene and add the specific .html file (These files are inside the 'Templates' folder).
Every file name is very self-explanatory.

Each file has a specific resolution: <br>
Scoreboard should be 1920x100 <br>
Versus should be 1920x1080 <br>
Winner should be 1920x1080 <br>
Bracket should be 1920x1080 <br>
Results should be 1920x1080 <br> 

If font is not properly loaded, install it to your system and that should fix it. It is inside 'Templates'.

After proper setup, open StreamMaster.exe. GUI is a little archaic.

SCOREBOARD: <br>
You can stablish names, teams and country (in text in case you want to add a specific region instead.) <br> For changes to be applied in OBS, click 'Save All Changes'.

PLAYER vs PLAYER: <br> 
Stablish name and character. There's a dropdown for characters instead of text entry.
The images used for Player vs Player are the default SF6 renders inside a square, as every SF6 render was different, it was difficult to stablish size and coordinates so they all fit.<br>
For changes to be applied in OBS, click 'Save All Changes'.

WINNER SCREEN: <br>
Stablish name, character, team and country. Same graphics as Player vs Player.<br> For changes to be applied in OBS, click 'Save All Changes'.

TOP 8 (Bracket:) <br>
Players are in order but not named. Use here as guide:<br>
Players 1 and 2 are the players for Winners Semis Match 1<br>
Players 3 and 4 are the players for Winners Semis Match 2<br>
Players 5 and 6 are the players for Losers Round 1 match 1<br>
Players 7 and 8 are the players for Losers Round 1 match 2<br>

With all players added to TOP 8, Save and go to 'Bracket Control' Tab.<br>
In Bracket control you can add results to matches, the software has the logic to handle the results automatically, the results are then processed to Top 8 results screen once you finish the tournament.

CUSTOMIZATION:
You can use the .psd templates however you like to. But if you need to move the position from texts that are going to be edited by the executable, you gotta edit their position in the respective html file. The same with the default font. This applies for text sizes and character images sizes. 

CHANGELOG:<br>
StreamMaster Tekken Edition Ver0.5<br>
-Event name and Match Info has been reposition so it doesn't clash with Tekken 8's default timer. This version is a little bigger in file size due to more chars and newer fonts.

StreamMaster Ver 0.5<br>
-Compiled icon to executable file, though not in the window lmao

StreamMaster Ver 0.4<br>
-Scroll has been fixed in the Top 8 Bracket tab.<br>
-Added more relevant information regarding who is who in 'Bracket Control'

StreamMaster Ver 0.3<br>
-A command prompt window no longer displays with the executable file. Only the GUI will be seen.

StreamMaster Ver 0.2<br>
-'Save All Changes' button has been moved from bottom to top. <br>
-Optional bracket reset added: if clicked the bracket reset option will be added and will be shown in bracket screen. 

StreamMaster Ver 0.1<br>
-First functional version, archaic GUI
