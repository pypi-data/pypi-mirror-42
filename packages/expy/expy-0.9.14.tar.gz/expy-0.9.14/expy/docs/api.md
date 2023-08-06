## Initialization

- **start(setting_file='setting.txt', fullscreen=True, winsize=(800, 600), mouse_visible=False, normal_font_size=20, stim_font_size=None, distance=60, diag=15, angel=1.6, font_color=C_white, background_color=C_gray, sample_rate=44100, port='', vsync=True)**


```
Initialize the experiment.
Note: todo.

Parameters
----------
setting_file: str (default: 'setting.txt')
    The filepath of setting
fullscreen: True(default), or False 
    Whether the window is fullscreen
winsize: (width,height) (default:(800, 600)) 
    The size of window
mouse_visible: True, or False(default)
    Set the mouse pointer visibility
normal_font_size: int (default:20) 
    The size of the text in normal font 
stim_font_size: int, or None(default) 
    The size of the text in stimulus font  
distance: int (default:60) 
    Distance from eyes to screen (cm)
diag: int (default:23) 
    The length of the screen diagonal (inch) 
angel: int (default:2.5) 
    Visual angel of single char (degree)
font_color: tuple RGBA (default:C_white) 
    The color of text
background_color: tuple RGBA (default:C_gray) 
    The color of background
sample_rate: int (default:44100) 
    Sample rate of sound mixer
port: str, or hex number (default:'') 
    Port name used to send trigger.
    Use str on serial port, and hex on parallel port 
vsync: True (default), or False 
    Vertical retrace synchronisation

Returns
-------
None
```

---
## Stimulus
### *Position*

- **getPos(x=shared.win_width // 2, y=shared.win_height // 2, w=0, h=0, anchor_x='center', anchor_y='center')**


```
Caluate the screen position of object

Parameters
----------
x: float or int (default: shared.win_width // 2)
    If x is float, it represents the x-offset(-1~1 scale) from the object benchmark to the screen center,
    if int, it represents the x-offset(pixel) from the object benchmark to the screen upperleft.
y: float or int (default: shared.win_height // 2)
    Similar with x
w: float or int (default: 0)
    If w is float, it represents the width scale on screen,
    if int, it represents the width in pixel.
h: float or int (default: 0)
    Similar with x 
anchor_x: str (default:'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default:'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.


Returns
-------
(x, y): (int, int)
    The position of the object's lowerleft corner

```

### *Text*

- **drawText(text, font=shared.default_font, size='stim_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', show_now=True, display=True, timeit=False, trigger=None)**


```
Draw text with complex format on the canvas. The text will show as multiple lines splited by the '\n'. 

Parameters
----------
text: str
    The content of text.
font: str (default: shared.default_font)
    The font name of text.
size:int, or str (default: 'stim_font_size')
    The font size of text, you can either use a number or a pre-defined number name.
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
rotation: int (default: 0)
    The rotation angle of text.
x: int, or float (default: 0.0)
    The x coordinate of text. If x is int, the coordinate would be pixel number to the left margin of screen; If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default: 0.0)
    The y coordinate of text. If y is int, the coordinate would be pixel number to the upper margin of screen; If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
anchor_x: str (default: 'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default: 'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
show_now: True(default), False
    If True, the function will put the canvas onto the screen immediately (with a potential delay);
    otherwise, the canvas will be put until `show` function.
(beta testing) trigger: (content, mode)
(beta testing) timeit: True, False (default)

Returns
-------
(width, height): Width and height of the text sprite
```

### *Shape*

- **drawRect(w, h, x=0.0, y=0.0, fill=True, color=C_white, width=1, anchor_x='center', anchor_y='center', show_now=True, display=True, timeit=False, trigger=None)**


```
Draw rectangle on the canvas.

Parameters
----------
w: float or int (default: 0)
    The width of rectangle.
    If w is float, it represents the width scale on screen,
    if int, it represents the width in pixel.
h: float or int (default: 0)
    The height of rectangle.
    Similar with x. 
x: int, or float (default:0.0)
    The x coordinate of rectangle.
    If x is int, the coordinate would be pixel number to the left margin of screen;
    If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default:0.0)
    The y coordinate of rectangle.
    If y is int, the coordinate would be pixel number to the upper margin of screen;
    If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
fill: True(default), False
    Whether to fill out the blank in rectangle
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
width: int (default: 1)
    The width of each line
anchor_x: str (default:'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default:'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
show_now: True(default), False
    If True, the function will put the canvas onto the screen. 
(beta testing) trigger: (content, mode)
(beta testing) timeit: True, False (default)

Returns
-------
None
```


- **drawCircle(r, x=0.0, y=0.0, fill=True, color=C_white, width=1, anchor_x='center', anchor_y='center', show_now=True, display=True, timeit=False, trigger=None)**


```
Draw circle on the canvas.

Parameters
----------
r: int
    The radius of circle in pixel.
x: int, or float (default:0.0)
    The x coordinate of circle.
    If x is int, the coordinate would be pixel number to the left margin of screen;
    If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default:0.0)
    The y coordinate of circle.
    If y is int, the coordinate would be pixel number to the upper margin of screen;
    If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
fill: True(default), False
    Whether to fill out the blank in circle
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
width: int (default: 1)
    The width of each line
anchor_x: str (default:'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default:'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
show_now: True(default), False
    If True, the function will put the canvas onto the screen. 
(beta testing) trigger: (content, mode)
(beta testing) timeit: True, False (default)

Returns
-------
None
```


- **drawPoints(points, color=C_white, size=1, show_now=True, display=True, timeit=False, trigger=None)**


```
Draw point(s) on the canvas.

Parameters
----------
points: list of tuple
    The x-y points list
    If the x,y are given as float, they would be interpret as an relative position[-1~+1] to the center on the screen;
    or if they are given as int, they would be interpret as pixel indicators to the lowerleft corner on the screen.
    Examples:
        [(0.0,0.0), (0.5,0), (0.5,0.5)]
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
size: int (default: 1)
    The size of each point
show_now: True(default), False
    If True, the function will put the canvas onto the screen. 
(beta testing) trigger: (content, mode)
(beta testing) timeit: True, False (default)

Returns
-------
None
```


- **drawLines(points, color=C_white, width=1, close=False, show_now=True, display=True, timeit=False, trigger=None)**


```
Draw line(s) on the canvas.

Parameters
----------
points: list of tuple
    The turning x-y points of lines
    If the x,y are given as float, they would be interpret as an relative position[-1~+1] to the center on the screen;
    or if they are given as int, they would be interpret as pixel indicators to the lowerleft corner on the screen.
    Examples:
        [(0.0,0.0), (0.5,0), (0.5,0.5)]
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
width: int (default: 1)
    The width of each line
close: True, False(default)
    Whether to connect the last point with the first one. 
    If True, the polygon could be drawn.
show_now: True(default), False
    If True, the function will put the canvas onto the screen.
(beta testing) trigger: (content, mode)
(beta testing) timeit: True, False (default)

Returns
-------
None
```

### *Picture*

- **drawPic(path, w=0, h=0, x=0.0, y=0.0, rotate=0, anchor_x='center', anchor_y='center', show_now=True, display=True, timeit=False, trigger=None)**


```
Draw loaded image on the canvas.

Parameters
----------
path: str
    The file path of target image
w: int(default:0), or float 
    The width of image.
    If w is float, it represents the width scale on screen;
    if int, it represents the width in pixel.
h: int(default:0), or float 
    The height of image.
    If w is float, it represents the height scale on screen;
    if int, it represents the height in pixel.
x: int, or float (default:0.0)
    The x coordinate of image.
    If x is int, the coordinate would be pixel number to the left margin of screen;
    If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default:0.0)
    The y coordinate of image.
    If y is int, the coordinate would be pixel number to the upper margin of screen;
    If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
rotation: int (default:0)
    The rotation angle of object.
anchor_x: str (default:'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default:'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
show_now: True(default), False
    If True, the function will put the canvas onto the screen. 
(beta testing) trigger: (content, mode)
(beta testing) timeit: True, False (default)

Returns
-------
None
```

### *Sound*

- **loadSound(path, offset=0, duration=None, stereo_array_format=True)**


```
Load a sound file, and return data array (stereo format)

Parameters
----------
path: str
    The file path of target sound
offset: number (default:0)
    The onset of target sound
duration: number, or None(default)
    The duration of target sound
stereo_array_format: True(default), or False
    Whether return a stereo array

Returns
-------
output: array
    The sound data
```


- **loadManySound(dirpath, filenames, ext='wav', offset=0.0, duration=None, stereo_array_format=True)**


```
Read a list of music file, then concatnate them and return data array (stereo format).

Parameters
----------
dirpath: str
    The directory path of target sounds
filenames: str
    The filenames of target sounds (without filename extension)
ext: str
    The filename extension of target sounds
offset: number (default:0)
    The onset of target sounds
duration: number, or None(default)
    The duration of target sounds
stereo_array_format: True(default), or False
    Whether return a stereo array

Returns
-------
output: array
    The sound data
```


- **makeBeep(frequency, duration, stereo_array_format=True)**


```
Making a beep (pure-frequency) sound (stereo format).

Parameters
----------
frequency: number
    The frequency of sound
duration: number
    The duration of sound
stereo_array_format: True(default), or False
    Whether return a stereo array

Returns
-------
output: array
    The sound data
```


- **makeNoise(duration, stereo_array_format=True)**


```
Making a white noise (stereo format).

Parameters
----------
duration: number
    The duration of sound
stereo_array_format: True(default), or False
    Whether return a stereo array

Returns
-------
output: array
    The sound data
```


- **makeSound(data)**


```
Read np.array object, then convert it into sound array (stereo format).

Parameters
----------
data: np.array
    The raw sound data array

Returns
-------
output: array
    The sound data
```


- **playSound(sound, busy=True, playing_track=None, timeit=False, trigger=None, triggerbox=False)**


```
Play a sound array, and the experiment procedure will be blocked by this function

Parameters
----------
sound: array
    The sound data
busy: True(default), or False
    Whether the experiment procedure will be blocked by the this function
playing_track: int, str, or None(default)
    The name of current track
(beta testing) timeit: True, False (default)
(beta testing) trigger: (content, mode)

Returns
-------
None
```


- **playBusySound(sound, timeit=False, trigger=None, triggerbox=False)**


```
Play a sound array, and the experiment procedure will be blocked by this function

Parameters
----------
sound: array
    The sound data
(beta testing) timeit: True, False (default)
(beta testing) trigger: (content, mode)

Returns
-------
None
```


- **playFreeSound(sound, playing_track=None, timeit=False, trigger=None)**


```
Play a sound array, and the experiment procedure won't be blocked by this function

Parameters
----------
sound: array
    The sound data
playing_track: int, str, or None(default)
    The name of current track
(beta testing) timeit: True, False (default)
(beta testing) trigger: (content, mode)

Returns
-------
playing_track
```


- **playAlterableSound(sound, effect=changeVolume, key_up=key_.RIGHT, key_down=key_.LEFT, key_confirm=key_.ENTER, timeit=False, trigger=None)**


```
Play a sound array, and the sound can be modified while playingr 

Parameters
----------
sound: array
    The sound data
effect: function (default: changeVolume)
    The function of how to change the sound by a given index.
key_up: keyname (default: key_.RIGHT)
    The key indicating up of the index.
key_down: keyname (default: key_.LEFT)
    The key indicating down of the index.
key_confirm: keyname (default: key_.ENTER)
    The key indicating the end of change detection.
(beta testing) timeit: True, False (default)
(beta testing) trigger: (content, mode)

Returns
-------
None
```


- **toStereoArray(sound)**


```
Force the sound data to stereo hex array

Parameters
----------
sound: array or np.array
    The original sound data

Returns
-------
output: array
    The stereo hex array version of sound data
```


- **changeVolume(raw, scale)**


```
Change the volume

Parameters
----------
raw: np.array
    The raw sound data
scale: num
    The change scale

Returns
-------
value: np.array
    The changed sound data
```


- **changePitch(raw, scale)**


```
Change the pitch

Parameters
----------
raw: np.array
    The raw sound data
scale: num
    The change scale

Returns
-------
value: np.array
    The changed sound data
```


- **changeOnTracks(data, func, scale_list, stereo_array_format=True)**


```
Change the sound on each track

Parameters
----------
data: np.array or array
    The raw sound data
func: method name
    The action of change 
scale: list
    The change scale of each track
stereo_array_format: True(default), or False
    Whether return a stereo array

Returns
-------
output: array
    The sound data
```


### *Video*

- **loadVideo(path)**


```
Load a video array

Parameters
----------
path: str
    The file path of target video

Returns
-------
player: pyglet.media.Player
    playVideo() could use it 
```


- **playVideo(video, pauseKey=key_.SPACE, x=0.0, y=0.0, anchor_x='center', anchor_y='center')**


```
Play a loaded video

Parameters
----------
video: pyglet.media.Player
    The player of target video
pauseKey: (default: key_.SPACE)
    The name for pausekey
x: int, or float (default:0.0)
    The x coordinate of text. If x is int, the coordinate would be pixel number to the left margin of screen; If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default:0.0)
    The y coordinate of text. If y is int, the coordinate would be pixel number to the upper margin of screen; If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
anchor_x: str (default:'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default:'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.

Returns
-------
None
```

### *Display controller*

- **show(out_time=False, clean_screen=True, stop_signal=None, backup=None, debugging=True)**


```
Display current canvas buffer, and keep the display during a limited period.

Parameters
----------
out_time: num(>0), False(default)
    The time limit of current function. (unit: second)
clean_screen: True(default), False
    Whether clear the screen after get the screen or not. 
stop_signal: None (default), str
    If the stop_signal is str, this method would be blocked until a stop_signal was received from the 0.0.0.0:36
backup: None, or a screen backup
    Give a prepared screen to display

Returns
-------
None
```


- **clear(debugging=True)**


```
Clear the screen

Parameters
----------
None

Returns
-------
None
```


- **getScreen(clean_screen=True)**


```
Get a backup of current canvas

Parameters
----------
clean_screen: True(default), False
    Whether clear the screen after get the screen or not. 

Returns
-------
None
```

---
## Response
### *Keyboard & Mouse & Joystick*

- **waitForResponse(allowed_keys=[], out_time=0, has_RT=True, allowed_clicks=[], action_while_pressing=None ,suspending=False)**


```
Waiting for a allowed keypress event during a limited period
(Press F12 would suspend the procedure and press ESC would end the program)

Parameters
----------
allowed_keys: None(default), Keyname, list, or dict
    The allowed key(s).
    You can leave nothing, 
            a Keyname (eg. key_.F), 
            a list of Keyname (eg. [key_.F,key_.J]), 
            or a dict of Keyname (eg. [key_.F:'F',key_.J:'J']) here.
    You could look into the Keyname you want in http://expy.readthedocs.io/en/latest/keymap/
out_time: num(>0), 0(default)
    The time limit of current function. While the past time exceeds the limitation, the function terminates.
has_RT: True(default), False
    Return a past time or not
allowed_clicks: None(default), ClickRange object, list, or dict
    The allowed mouse click event(s).
    You can leave nothing, 
            a ClickRange object (eg. C1), 
            a list of ClickRange object (eg. [C1, C2]), 
            or a dict of ClickRange object (eg. {C1:'F',C2:'J'}) here.
action_while_pressing: None(default), tuple
    If None, the pressing will be ingored.
    Otherwise, the tuple will be unpacked. 
        The first element is the function, and the rest are(is) the paramenter(s) of the function.

suspending: True, False(default)
    Label the suspend state. If true, the F12 wouldn't suspend the program.

Returns
-------
KEY: None, int, or defined value
    1. If allowed_keys is None, return the id of any pressed key
    2. If allowed_keys is a List (eg. [key_.F,key_.J]), return the id of allowed pressed key
    3. If allowed_keys is a Dict (eg. [key_.F:'F',key_.J:'J']), return the value of allowed pressed key
    4. Return None if the time is out and no allowed keypress
(Only if has_RT is True)
    (Only if action_while_pressing is None) RT: int
        The second count since the function starts.
    (Only if action_while_pressing is tuple) RT: (int, int)
        The second count until pressed, and the second count while pressing.
```

### *Sound Recorder*

- **environmentNoise(sampling_time, weights=(1.1,3,5,1.1,2,3), chunk=1024)**


```
Record the sound in a certain duration as the environment noise, and calcuate its amplitude and zero-crossing rate.

Parameters
----------
sampling_time: number
    The duration of noise sampling
weights: tuple (default: (1.1,3,5,1.1,2,3))
    (The weight of noise threshold of zero-crossing rate,
    The weight of low threshold of zero-crossing rate,
    The weight of high threshold of zero-crossing rate,
    The weight of noise threshold of sound amplitude,
    The weight of low threshold of sound amplitude,
    The weight of high threshold of sound amplitude)
chunk: int (default: 1024)
    The frame size

Returns
-------
zcr0: number
    The noise threshold of zero-crossing rate
zcr1: number
    The low threshold of zero-crossing rate
zcr2: number
    The high threshold of zero-crossing rate 
amp0: number
    The noise threshold of sound amplitude
amp1: number
    The low threshold of sound amplitude
amp2: number
    The high threshold of sound amplitude
```


- **recordSound(vad_levels, rec_length_min=0, rec_length_max=None, sound_length_max=None, trim_side='both', feedback=False, chunk=1024, playing_track=None, blocking=True, path='')**


```
Record sound from the microphone.

Parameters
----------
vad_levels: tuple
    (The noise threshold of zero-crossing rate,
    The low threshold of zero-crossing rate,
    The high threshold of zero-crossing rate,
    The noise threshold of sound amplitude,
    The low threshold of sound amplitude,
    The high threshold of sound amplitude)
rec_length_min: number(s) (default: 0)
    The second count of minimal recording time
rec_length_max: number(s), or None (default)
    The second count of maximal recording time
sound_length_max: number(s), or None (default)
    The second count of maximal sound length
trim_side: str (default: 'both')
    The trimming way of recorded sound
    Options: 'both', 'left', 'right', 'none'
feedback: True, or False(default)
    Whether the sound feedbacks while recording
chunk: int (default: 1024)
    The frame size
playing_track: int, str, or None(default)
    The name of current track
blocking: True(default), or False
    Whether the experiment procedure would be blocked by the current function
path: str (default: '')
    The file path of target sound. If the path is undefined(''), the sound won't be recorded.
Returns
-------

If recorded:
    rec_data, onset time
    (rec_data: np.array
        The recorded sound array in stereo)
If recorded nothing:
    [], 0
If not blocking:
    None
```

---
## IO
### *Read*

- **readSetting(filepath='setting.txt')**


```
Read the setting file and put the items into a dict.
If the 'timing_set' is in the file, create a "timing" in the dict to put the timing parameter.

Parameters
----------
filepath: str (default:'setting.txt')
    The path of the setting file.

Returns
-------
setting: dict
    todo.
```


- **readStimuli(filepath, query=None, sheetname=0, return_list=True)**


```
Get the stimuli from a csv/excel file

Parameters
----------
filepath: str
    The path of the data file
query: str, None(default)
    The query expression (e.g. 'block==1' or 'block>1 and cond=="A"')
sheetname: int (default:0)
    The sheet id of an excel.
return_list: True(default), False
    If return_list is True, then return a list of rows instead of whole table

Returns
-------
stimuli: list of rows(pandas.Series), or whole table (pandas.DataFrame)
    The selected stimuli data
```


- **readDir(dirpath, shuffle=True)**


```
List the files in a directory

Parameters
----------
dirpath: str
    The path of target directory
shuffle: True, False(default)
    Whether shuffle the list or not 

Return
---------
files: list
    The filename list
```

### *Save*

- **saveResult(resp, block_tag='', columns=['respKey', 'RT'], stim=None, stim_columns=None, saveas='csv')**


```
Save experiment result to a file named {subjectID}_result.csv.
The file would be updated after each block.
The subjectID equals to "shared.subject", and you could set it by `shared.subject = getInput('please enter the ID:')`.
If stim is not None, the stimuli data would attach to the response result.

Parameters
----------
resp: list
    The list of response data (dict hasn't been supported)
block_tag: str (default:''), or int
    The tag of current block
columns: list
    The names of response data columns
stim: pandas.DataFrame, or list
    The data of stimuli
stim_columns: None, or list
    The names of stimuli data columns
saveas: 'csv' (default), or 'excel'
    The file format of saved file. 

Return
---------
None
```

### *Record the log*

- **log(*events, fn='log.txt', with_time=True)**


```
Record the log to a file in the working directory.

Parameters
----------
events: single parameter or multiple parameters
    The events which to be logged. If got multiple parameters, they will be seperated by blank.
fn: str (default: 'log.txt' in the working directory)
    The target log file name or path. 
with_time: bool (default: True)
    Whether add the time stamp to the line end.  

Return
---------
None
```

### *Send trigger*

- **sendTrigger(data, mode='P')**


```
Send trigger

Parameters
----------
data: int, or str
    The trigger content
mode: 'P', or 'S'
    The port type: 'P' refers to parallel port, 'S' refers to serial port

Return
---------
None
```

---
## Other Scaffolds

- **textSlide(text, font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None)**


```
Display a new text slide right now.

Parameters
----------
text: str
    The text on the screen.
font: str (default:'shared.default_font')
    The fontname of the text.
size:int, or str (default: 'normal_font_size')
    The font size of text, you can either use a number or a pre-defined number name.
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
rotation: int (default: 0)
    The rotation angle of text.
x: int, or float (default: 0.0)
    The x coordinate of text. If x is int, the coordinate would be pixel number to the left margin of screen; If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default: 0.0)
    The y coordinate of text. If y is int, the coordinate would be pixel number to the upper margin of screen; If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
anchor_x: str (default: 'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default: 'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
background_image: str, or None(default)
    The path of background picture.
    
Return
---------
None
```


- **getInput(pre_text, out_time=0, font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None)**


```
Get user input until "ENTER" pressed, then give it to a variable

Parameters
----------
pre_text: str
    The text that will be displayed before user's input.
out_time: num(>0) or 0(default)
    The time limitation of this function.
font: str (default:'shared.default_font')
    The fontname of the text.
size:int, or str (default: 'normal_font_size')
    The font size of text, you can either use a number or a pre-defined number name.
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
rotation: int (default: 0)
    The rotation angle of text.
x: int, or float (default: 0.0)
    The x coordinate of text. If x is int, the coordinate would be pixel number to the left margin of screen; If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default: 0.0)
    The y coordinate of text. If y is int, the coordinate would be pixel number to the upper margin of screen; If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
anchor_x: str (default: 'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default: 'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
background_image: str, or None(default)
    The path of background picture.

Return
---------
input_text: str
    The content of user's input.
```


- **getSubjectID(pre_text='Please enter the subject ID:')**


```
Get subject's ID.

Parameters
----------
pre_text: str
    The text that will be displayed before user's input.
```


- **instruction(instruction_text=None, has_practice=False)**


```
Show the instruction of experiment
(press 'left' to back, 'right' to continue)

Parameters
----------
instruction_text: None (default), list of str
    The text that will be displayed as instruction. If None, the instruction text in the setting file will be loaded.

Return
---------
resp: Keyname/int
    The last pressed key name.
```


- **alert(text, out_time=0, allowed_keys=[key_.RETURN], font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None)**


```
Display a new text slide right now, and keep the screen until user's response.

Parameters
----------
text: str
    The text on the screen.
allowed_keys: Keyname, or list of Keyname (default:[key_.RETURN])
    The allowed user's response.
out_time: num(>0) or 0(default)
    The display time limitation of this function.
font: str (default:'shared.default_font')
    The fontname of the text.
size:int, or str (default: 'normal_font_size')
    The font size of text, you can either use a number or a pre-defined number name.
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
rotation: int (default: 0)
    The rotation angle of text.
x: int, or float (default: 0.0)
    The x coordinate of text. If x is int, the coordinate would be pixel number to the left margin of screen; If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default: 0.0)
    The y coordinate of text. If y is int, the coordinate would be pixel number to the upper margin of screen; If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
anchor_x: str (default: 'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default: 'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
background_image: str, or None(default)
    The path of background picture.
    
Return
---------
resp: Keyname/int
    The last pressed key name.
```


- **alertAndGo(text, out_time=3, allowed_keys=[key_.RETURN], font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None)**


```
Display a new text slide right now, 
and keep the screen in a given period of time, or until user pressed SPACE or key_.RETURN

Parameters
----------
text: str
    The text on the screen.
allowed_keys: Keyname, or list of Keyname (default:[key_.RETURN])
    The allowed user's response.
out_time: out_time: num(>0) (default: 3)
    The display time limitation of this function.
font: str (default:'shared.default_font')
    The fontname of the text.
size:int, or str (default: 'normal_font_size')
    The font size of text, you can either use a number or a pre-defined number name.
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
rotation: int (default: 0)
    The rotation angle of text.
x: int, or float (default: 0.0)
    The x coordinate of text. If x is int, the coordinate would be pixel number to the left margin of screen; If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default: 0.0)
    The y coordinate of text. If y is int, the coordinate would be pixel number to the upper margin of screen; If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
anchor_x: str (default: 'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default: 'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
background_image: str, or None(default)
    The path of background picture.
    
Return
---------
None
```


- **alertAndQuit(text, out_time=3, allowed_keys=[key_.RETURN], font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None)**


```
Display a new text slide right now, 
and keep the screen in a given period of time, or until user pressed SPACE or key_.RETURN,
then quit the program.

Parameters
----------
text: str
    The text on the screen.
allowed_keys: Keyname, or list of Keyname (default:[key_.RETURN])
    The allowed user's response.
out_time: out_time: num(>0) (default: 3)
    The display time limitation of this function.
font: str (default:'shared.default_font')
    The fontname of the text.
size:int, or str (default: 'normal_font_size')
    The font size of text, you can either use a number or a pre-defined number name.
color: RGB tuple, or pre-defined variable (default:'C_white')
    The font color of text, you can either use an RGB value or a pre-defined color name. 
    The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
rotation: int (default: 0)
    The rotation angle of text.
x: int, or float (default: 0.0)
    The x coordinate of text. If x is int, the coordinate would be pixel number to the left margin of screen; If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
y: int, or float (default: 0.0)
    The y coordinate of text. If y is int, the coordinate would be pixel number to the upper margin of screen; If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
anchor_x: str (default: 'center')
    The position benchmark on this object to the given x.
    Options: 'center', 'left', or 'right'.
anchor_y: str (default: 'center')
    The position benchmark on this object to the given y.
    Options: 'center', 'top', or 'bottom'.
background_image: str, or None(default)
    The path of background picture.
    
Return
---------
None
```


- **restTime(text=rest_text, background_image=None, background_music=None)**


```
Suspend the experiment and ask participant to rest:
1. Display a blank screen in 3s,
2. Display a new text slide which tells user to rest, 
3. keep the screen until user pressed SPACE.

Parameters
----------
text: str
    The text on the screen.
background_image: str, or None(default)
    The path of background picture.
    
Return
---------
None
```


- **normalProcedure(trial_func, trial_list='trial_list.csv',  practice_list=None, practice_func=None, onset_block=1, instruction_setting='instruction')**


```
General framework of experiment procedure.

Parameters
----------
trial_func: method name
    Name of trial method
trial_list: str (default: 'trial_list.csv')
    Name of trial list
practice_list: str, or None (default)
    Name of practice trial list
onset_block: int (default: 1)
    Number of onset block
instruction_setting: str (default: 'instruction'), or None
    Name of instruction in the setting file

Returns
-------
None
```


