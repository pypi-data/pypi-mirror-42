# coding:utf-8
import pandas as pd
import re

from expy import shared

np = shared.np
os = shared.os

def readSetting(filepath='setting.txt'):
    '''
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
    '''
    if os.path.exists(filepath): # if file exists
        # keep the encoding to utf-8
        try:
            with open(filepath,encoding='utf-8') as f:
                f.read()
        except:
            with open(filepath) as f:
                text = f.read()
            with open(filepath,'w',encoding='utf-8') as f:
                f.write(text)
    else: # if file does not exist
        with open(filepath,'w',encoding='utf-8') as f:
            f.writelines(['----\n',
                        '[subject_name_query]\n',
                        '请输入实验序号：\n',
                        '----\n',
                        '[instruction]\n',
                        '欢迎参加我们的实验！\n>\n请在准备完备后开始。\n',
                        '----\n',
                        '[block_start]\n',
                        '实验会在3秒后开始\n',
                        '----\n',
                        '[experiment_end]\n',
                        '实验结束~ 谢谢参与我们的实验!'])

    setting = dict()
    with open(filepath,encoding='utf-8') as f:
        try:
            for s in re.compile(r'[-]{2,}').split(f.read()):
                if len(s) > 0 and s != '\n':
                    if s[0] == '\n':
                        s = s[1:]
                    if s[-1] == '\n':
                        s = s[:-1]

                    name, *content = s.split('\n')
                    name = name[1:-1]
                    if name != 'timing_set' and len(content)==1:
                        setting[name] = content[0]
                    else:
                        setting[name] = content

            if 'timing_set' in setting:
                setting['timing'] = dict()
                # Set timing of each phase
                for dur in setting['timing_set']:
                    k, v = dur.replace(' ', '').split(':')
                    if '-' in v:
                        limit = v.split('-')
                        setting['timing'][k] = [float(limit[0]), float(limit[1])]
                    else:
                        setting['timing'][k] = float(v)
        except:
            raise ValueError('Please check your setting.txt!')

    return setting


def readStimuli(filepath, query=None, sheetname=0, return_list=True):
    '''
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
    '''
    if not os.path.exists(filepath):
        filepath = 'data/' + filepath

    if filepath.split('.')[-1] == 'csv':
        stimuli = pd.read_csv(filepath, sep=',', encoding='gbk')
    elif filepath.split('.')[-1] in ['xls', 'xlsx']:
        stimuli = pd.read_excel(filepath, sep=',', sheet_name=0)
    else:
        raise ValueError('Only support csv and Excel file')
    if type(query) == str:
        stimuli = stimuli.query(query)
        # .sample(n=4)
    stimuli.index = range(len(stimuli))
    if return_list:
        stimuli = [i for ind, i in list(stimuli.iterrows())]
    return stimuli


def readDir(dirpath, shuffle=True):
    '''
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
    '''
    files = [dirpath + '/' + f for f in os.listdir(dirpath)]
    if shuffle:
        np.random.shuffle(files)
    return files


def saveResult(resp, block_tag='', columns=['respKey', 'RT'], stim=None, stim_columns=None, saveas='csv'):
    '''
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
    '''
    if not os.path.exists('result'):
        os.mkdir('result')

    columns_count = len(resp[0]) if isinstance(resp[0], (list, tuple)) else 1
    if columns_count != len(columns):
        columns = [f'resp{i+1}' for i in range(columns_count)]
        print('Columns count setting doesn\'t match the result!')

    result = pd.DataFrame(resp, columns=columns)
    if not stim is None:
        if type(stim) is list:
            stim = pd.DataFrame(stim, columns=stim_columns)
        result = stim.join(result)

    if block_tag == '':
        if saveas == 'excel':
            result_file = 'result/%s_result.xlsx' %(shared.subject)
            if os.path.exists(result_file):
                old_data = pd.read_excel(result_file)
                pd.concat([old_data, result]).to_excel(result_file, index=None)
            else:
                result.to_excel(result_file, index=None)
        elif saveas == 'csv':
            result_file = 'result/%s_result.csv' %(shared.subject)
            if os.path.exists(result_file):
                old_data = pd.read_csv(result_file, encoding='gbk')
                pd.concat([old_data, result]).to_csv(result_file, encoding='gbk', index=None)
            else:
                result.to_csv(result_file, encoding='gbk', index=None)
    else:
        if saveas=='csv':
            result.to_csv('result/%s_%s_result.csv' % (shared.subject,
                                                       str(block_tag)), encoding='gbk', index=None)
        if saveas=='excel':
            result.to_excel('result/%s_%s_result.xlsx' %(shared.subject, str(block_tag)), index=None)

def log(*events, fn='log.txt', with_time=True):
    '''
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
    '''
    events = '\t'.join([str(e) for e in events])
    if with_time:
        events = f"{events}\t{shared.time.time()-shared.onset}\n"
    else:
        events = f"{events}\n"
    with open(fn,'a',encoding='utf-8') as f:
        f.write(events)

def sendTrigger(data, mode='P'):
    '''
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
    '''
    try:
        if mode == 'P':
            shared.port_dll.Out32(shared.setting['port'], data)
        elif mode == 'S':
            # send a string which might change
            if isinstance(data, bytes):
                shared.ser.write(data)
            else:
                shared.ser.write(bytes(data, encoding='utf-8'))
        else:
            raise ValueError('Only support "S" or "P" (serial/parallel) mode!')
    except:
        if shared.setting['port'] != '':
            print('The port might be closed.')


            # shared.ser.write(b'something') # send a string directly
            # a binary code
            # n=int('0b00010001',2)
            # shared.ser.write(n.to_bytes((n.bit_length()+7)//8, 'big')) # send

def getTrigger():
    try:
        msg = shared.ser.read()
        shared.start_tp = shared.time.time()

        return msg
    except:
        if shared.setting['port'] != '':
            print('The port might be closed.')
