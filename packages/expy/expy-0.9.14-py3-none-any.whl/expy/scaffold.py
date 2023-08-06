# coding:utf-8

import pyglet.window.key as key_
from expy import shared
from .colors import *
from .stim.draw import *
from .stim.sound import *
from .stim.display import *
from .io import *
from .response import *

np = shared.np

def timing(name):
    '''
    Get a value of timing parameter:
    If the setting gave a int, return it;
    If the setting gave a range, return a random int in that range.

    Parameters
    ----------
    name: str
        The name of timing parameter.
        
    Return
    ---------
    value: int
    '''
    val = shared.setting['timing'][name]
    if type(val) == float:
        return val
    else:
        return np.random.randint(int(val[0]*1000), int(val[1]*1000))/1000

def button(text='Click', w=0.1, h=0.1, x=0.0, y=0.0, color=C_maroon, font_size='stim_font_size', font_color=C_white):
    '''
    Draw a clicked rectangle button with text.

    Parameters
    ----------
    text: str
        The text on the button.
    w: float or int (default: 0.1)
        The width of rectangle.
        If w is float, it represents the width scale on screen,
        if int, it represents the width in pixel.
    h: float or int (default: 0.1)
        The height of rectangle.
        Similar with x. 
    x: int, or float (default: 0.0)
        The x coordinate of text. If x is int, the coordinate would be pixel number to the left margin of screen; If x is float (-1~1), the coordinate would be percentage of half screen to the screen center.
    y: int, or float (default: 0.0)
        The y coordinate of text. If y is int, the coordinate would be pixel number to the upper margin of screen; If y is float (-1~1), the coordinate would be percentage of half screen to the screen center.
    color: RGB tuple, or pre-defined variable (default:'C_maroon')
        The font color of text, you can either use an RGB value or a pre-defined color name. 
        The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
    font_size: int, or str (default: 'stim_font_size')
        The font size of text, you can either use a number or a pre-defined number name.
    font_color: RGB tuple, or pre-defined variable (default:'C_white')
        The font color of text, you can either use an RGB value or a pre-defined color name. 
        The pre-defined colors include C_black, C_white, C_red, C_lime, C_blue, C_yellow, C_aqua, C_fuchsia, C_silver, C_gray, C_maroon, C_olive, C_green, C_purple, C_teal, C_navy.
        
    Return
    ---------
    x: int
        X value of clicked position
    y: int
        Y value of clicked position 
    rt: int
        The second count since the function starts.
    button: int
        The id of clicked mouse button
    '''
    drawRect(w, h, x, y, color=color, show_now=False)  # Draw a button
    # Draw text on the canvas and display it
    drawText(text, size=font_size, color=font_color)
    (button, (x, y)), rt = waitForResponse(allowed_clicks=ClickRange(
        (x-w/2, x+w/2), (y-h/2, y+h/2), shared.mouse_.LEFT))  # Waiting for mouse click and get the click
    return x, y, rt, button

def textSlide(text, font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None):
    '''
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
    '''
    clear()
    if background_image:
        drawPic(background_image, show_now=False)
    drawText(text, font, size, color, rotation, x, y, anchor_x, anchor_y)
    

def getInput(pre_text, out_time=0, font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None):
    '''
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
    '''
    textSlide(pre_text, font, size, color, rotation, x, y, anchor_x, anchor_y, background_image)
    text = pre_text
    if not shared.start_tp:
        shared.start_tp = shared.time.time()
    while 1:
        inkey = waitForResponse(has_RT=False, out_time=out_time)
        if inkey in [key_.RETURN, 'None']:
            break
        elif inkey == key_.BACKSPACE:
            text = text[0:-1]
        elif inkey <= 127:
            text += (chr(inkey))
        elif 65456 <= inkey <= 65465:
            text += (chr(inkey-65408))
            
        textSlide(text, font, size, color, rotation, x, y, anchor_x, anchor_y, background_image)
    input_text = text[len(pre_text):]
    clear()
    return input_text

def getSubjectID(pre_text='Please enter the subject ID:'):
    '''
    Get subject's ID.

    Parameters
    ----------
    pre_text: str
        The text that will be displayed before user's input.
    '''
    shared.subject = getInput(pre_text)


def instruction(instruction_text=None, has_practice=False):
    '''
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
    '''
    if instruction_text is None:
        instruction_text = shared.setting['instruction']

    intro = '\n'.join(instruction_text).split('>\n')
    i = 0
    while True:
        if intro[i] == '[demo]':
            demo()
            i += 1
            continue

        if i == 0:
            textSlide(
                intro[i] + '\n\n\n(按“→”进入下一页)\n\n(Press "→" to the next page)')
        elif i == len(intro) - 1:
            textSlide(intro[
                      i] + '\n\n\n(按“←”返回上一页，按 [空格] 开始实验. )\n\n(Press "←" to the previous page, or Press "SPACE" to start the experiment)')
        else:
            textSlide(intro[
                      i] + '\n\n\n(按“←”返回上一页，按“→”进入下一页)\n\n(Press "←" to the previous page, or Press "→" to the next page)')

        resp = waitForResponse(has_RT=False)
        if resp == key_.LEFT and i > 0:
            i -= 1
        elif resp == key_.RIGHT and i < len(intro) - 1:
            i += 1
        elif resp in [key_.SPACE, key_.RETURN] and i == len(intro) - 1:
            clear()
            return resp

def alert(text, out_time=0, allowed_keys=[key_.RETURN], font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None):
    '''
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
    '''
    textSlide(text, font, size, color, rotation, x, y, anchor_x, anchor_y, background_image)
    resp = waitForResponse(allowed_keys, out_time, has_RT=False)
    clear()
    return resp

def alertAndGo(text, out_time=3, allowed_keys=[key_.RETURN], font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None):
    '''
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
    '''
    alert(text, out_time, allowed_keys, font, size, color, rotation, x, y, anchor_x, anchor_y, background_image)

def alertAndQuit(text, out_time=3, allowed_keys=[key_.RETURN], font=shared.default_font, size='normal_font_size', color=C_white, rotation=0, x=0.0, y=0.0, anchor_x='center', anchor_y='center', background_image=None):
    '''
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
    '''
    alert(text, out_time, allowed_keys, font, size, color, rotation, x, y, anchor_x, anchor_y, background_image)
    shared.pa.terminate()
    shared.pyglet.app.exit()
    shared.win.close()
    

rest_text = '实验暂停，您可以休息一会\n\
Now you can have a rest.\n\
如果休息结束请按 [空格] 继续实验。\n\
Please press [SPACE] key when you want to continue.\n'


def restTime(text=rest_text, background_image=None, background_music=None):
    '''
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
    '''
    if background_music:
        sound = loadSound(background_music)
        playing_track = playFreeSound(sound)
    
    textSlide(text, background_image=background_image)
    shared.time.sleep(3)
    shared.win.dispatch_events()
    shared.events = []
    text2 = text + '>>>'
    alert(text2, 0, key_.SPACE, background_image=background_image)
    if background_music:
        shared.states[playing_track] = False
