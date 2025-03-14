# TrannosRun
Dodge the police cars and try to collect as many guns as possible or you'll get caught, just like Trannos did. 

## Download the game:
Get the game by visiting [LabeledZed's itch.io page](https://labeledzed.itch.io/trannosrun)

or from [here](https://github.com/manydevs/trannosrun/releases/latest)

## Track list
View the full track list [here](https://github.com/manydevs/trannosrun/blob/main/soundlib.txt)

## Source code compilation instructions
- Clone the repo with Git by executing:
  ```git
  git clone https://github.com/manydevs/trannosrun.git
  ```
  or by clicking the download link:
  https://github.com/manydevs/trannosrun/archive/refs/heads/main.zip
  
- Fill in the Redis database information in line 170 of trannosrun.py
  
- Open a console window in the project's root directory and run:
  ```batch
  pip install requirements.txt
  python -m PyInstaller --onefile --windowed --hidden-import=pypresence --hidden-import=tqdm --hidden-import=requests --hidden-import=python-vlc --hidden-import=redis --hidden-import=pygame --add-data "assets\\bg.jpg;assets" --add-data "assets\\gani.png;assets" --add-data "assets\\mavro_jet.ico;assets" --add-data "assets\\mavro_jet.png;assets" --add-data "assets\\tseoi.png;assets" --add-data "assets\\xamene.png;assets" --add-data "assets\\collect.wav;assets" --upx-dir "D:\Data\Projects\pyProjects\tr2\upx-5.0.0-win64\upx.exe" --icon="packico.ico" --splash=splash.png trannosrun.py
  ```
  

###### Disclaimer: ManyDevs is not affiliated with Trapsion Entertainment, No Cap Label or Capital Music. Every asset that the game uses is publicly available and can be downloaded by anyone.
