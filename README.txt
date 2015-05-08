-----------------------------------------------------------------------------

Q-Learning SanDbox (QLSD)

-----------------------------------------------------------------------------
Files
-----------------------------------------------------------------------------

./CORE/

- fSandDataGetter.py - loop which produces one step in the sandbox world; !!!Run it for train!!!
- fSandBox.py - main class contains all sandbox world and creatures;
- fSandController - Q controller;
- fSandFun - features extraction and support functions;
- fSandDemo* - final model working demonstration; !!!Run it for demo!!!

./CORE/models/

- W_iterations#_features# - model in numPy format;

./test/ - folder with experiments;
./img/ - folder with screenshots and media;

./CORE/deepmode/ - deep learning model based on neural networks;

-----------------------------------------------------------------------------
Dependencies
-----------------------------------------------------------------------------

- NumPy
- PyGame
- Pillow
- - libjpeg-dev (before Pillow on Ubuntu)
- Common sense (=

-----------------------------------------------------------------------------
Actions
-----------------------------------------------------------------------------

_______
|0|1|2|
|3|4|5|
|6|7|8|
___
|9| Stop

-----------------------------------------------------------------------------
Final models
-----------------------------------------------------------------------------

W_final_wd_stoper_3.npy - 7M iterations | Max fixed | Direct control | Without inertia | Final
W_final_wd_stoper_4.npy - 2M iterations | Max fixed | Direct control | Without inertia | Final
W_final_wd_stoper_2.npy - 7M iterations | Max NOT fixed | Direct control | Without inertia | Final

All other models are not final and just for comparing
-----------------------------------------------------------------------------
