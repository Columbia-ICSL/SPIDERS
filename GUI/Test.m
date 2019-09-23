function varargout = Test(varargin)
% TEST MATLAB code for Test.fig
%      TEST, by itself, creates a new TEST or raises the existing
%      singleton*.
%
%      H = TEST returns the handle to a new TEST or the handle to
%      the existing singleton*.
%
%      TEST('CALLBACK',h Object,eventData,handles,...) calls the local
%      function named CALLBACK in TEST.M with the given input arguments.
%
%      TEST('Property','Value',...) creates a new TEST or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Test_OpeningFcn gets cal  led.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Test_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Test

% Last Modified by Jingping Nie May 31 2019
% Make the time and response match

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Test_OpeningFcn, ...
                   'gui_OutputFcn',  @Test_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before Test is made visible.
function Test_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Test (see VARARGIN)

% Choose default command line output for Test
handles.output = hObject;
handles.counter = 1;
handles.counter1 = 1;
handles.TrialIndex = 1;
handles.PictureTrialIndex = 1;
handles.VideoTrialIndex=1;
% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Test wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Test_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
set(handles.editText,'enable','off');
set(handles.text6,'Visible','off');
set(handles.text7,'Visible','off');
load('PictureStim.mat')%load('picture.mat')
handles.picture=picture;
PictureTrialIndex = handles.PictureTrialIndex;
guidata(hObject,handles);
set(handles.pushbutton2,'Visible','off');
set(handles.pushbutton4,'Visible','off');
set(handles.pushbutton5,'Visible','off');
set(handles.pushbutton6,'Visible','off');
%----------------------
a = get(handles.editText,'String');
respPicTimeStart.time=posixtime(datetime('now'));%GetTime(handles);
handles.respPicTimeStart(handles.counter) = respPicTimeStart;
respPicTimeStart = handles.respPicTimeStart;
save (['.\Subject\' num2str(a) 'PictureTimestart'],'respPicTimeStart');
%----------------------
if handles.PictureTrialIndex < length(handles.picture)
    set(handles.pushbutton1,'Visible','off');
    posixtime(datetime('now'))
    PlayPicture(hObject,handles);
else
    msgbox('Wait','Wait for Assistance!','Warn');
    set(handles.pushbutton2,'Visible','on');
    set(handles.pushbutton4,'Visible','on');
    set(handles.pushbutton1,'Visible','on');
    set(handles.pushbutton5,'Visible','off');
    set(handles.pushbutton6,'Visible','off');
end



function PlayPicture (hObject,handles)
Visibility(handles, 'off')
set(handles.pushbutton3,'Visible','off')
PictureTrialIndex = handles.PictureTrialIndex;
picture=handles.picture;

%
[w,fs_audio] = audioread('C:\Users\jingp\Desktop\Test\chirp.wav');
w = w/(20*rms(w));
c = audioplayer(w,fs_audio);
playblocking(c);
a = imread(['C:\Users\jingp\Desktop\Test\GrayscalePic\',picture{PictureTrialIndex}]);%IAPSImages\',picture{PictureTrialIndex}]);
axes(handles.axes1)
imshow(a)
pause(6)


% 
% respPicTimeStart.time=posixtime(datetime('now'));%GetTime(handles);
% handles.respPicTimeStart(handles.counter) = respPicTimeStart;
% respPicTimeStart = handles.respPicTimeStart;
% %format long
% %respPicTimeStart = posixtime(datetime('now'));
% a = get(handles.editText,'String');
% save (['.\Subject\' num2str(a) 'PictureTimestart'],'respPicTimeStart');

a = imread(['C:\Users\jingp\Desktop\Test\GrayscalePic\',picture{PictureTrialIndex+1}]);
axes(handles.axes1)
imshow(a)
pause(6)


% respPicTimeEnd.time=posixtime(datetime('now'));%GetTime(handles);
% handles.respPicTimeEnd(handles.counter) = respPicTimeEnd;
% respPicTimeEnd = handles.respPicTimeEnd;
% %format long
% %resp.time = posixtime(datetime('now'));
% a = get(handles.editText,'String');
% save (['.\Subject\' num2str(a) 'PictureTimeEnd'],'respPicTimeEnd');


a = imread(['C:\Users\jingp\Desktop\Test\GrayscalePic\',picture{PictureTrialIndex+2}]);
axes(handles.axes1)
imshow(a)
Visibility(handles, 'on')
set(handles.pushbutton3,'Visible','on')
guidata(hObject, handles);

% --- Executes on button press in pushbutton4.
function pushbutton3_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton4 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
respPic = GetResponse(handles);
if respPic.V1+respPic.V2+respPic.V3+respPic.V4+respPic.V5+respPic.V6+respPic.V7+respPic.V8+respPic.V9<1, msgbox('Choose one valence score','Choose one!','Warn');return;end;
if respPic.V10+respPic.V11+respPic.V12+respPic.V13+respPic.V14+respPic.V15+respPic.V16+respPic.V17+respPic.V18<1, msgbox('Choose one arousal score','Choose One!','Warn');return;end;
handles.respPic(handles.counter) = respPic;
respPic = handles.respPic;
%format long
a = get(handles.editText,'String');
save (['.\Subject\' num2str(a) 'Picture'],'respPic');

respPicTimeStart.time=posixtime(datetime('now'));%GetTime(handles);
handles.respPicTimeStart(handles.counter+1) = respPicTimeStart;
respPicTimeStart = handles.respPicTimeStart;
save (['.\Subject\' num2str(a) 'PictureTimestart'],'respPicTimeStart');


handles.counter = handles.counter+1;
ResetResponses(handles);
PictureTrialIndex = handles.PictureTrialIndex;
PictureTrialIndex = PictureTrialIndex + 3;
handles.PictureTrialIndex = PictureTrialIndex;
if handles.PictureTrialIndex < length(handles.picture)
    PlayPicture(hObject,handles);
else
    msgbox('Wait','Wait for Assistance!','Warn');
    set(handles.pushbutton2,'Visible','on');
    set(handles.pushbutton4,'Visible','on');
    set(handles.pushbutton1,'Visible','on');
    set(handles.pushbutton5,'Visible','on');
    set(handles.pushbutton6,'Visible','on');
end
%save ( 'Subject','resp');
guidata(hObject,handles);

% --- Executes during object creation, after setting all properties.
function axes1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to axes1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: place code in OpeningFcn to populate axes1


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Start
set(handles.editText,'enable','off');
set(handles.pushbutton1,'Visible','off');
set(handles.pushbutton3,'Visible','off');
set(handles.pushbutton5,'Visible','off');
set(handles.pushbutton6,'Visible','off');
set(handles.text6,'Visible','on');
set(handles.axes1,'Visible','off')
load('SoundStim.mat')
handles.StimOrder = StimOrder;
guidata(hObject,handles);
%----------------------
a = get(handles.editText,'String');
respSoundTimeStart.time=posixtime(datetime('now'));%GetTime(handles);
handles.respSoundTimeStart(handles.counter) = respSoundTimeStart;
respSoundTimeStart = handles.respSoundTimeStart;
save (['.\Subject\' num2str(a) 'SoundTimestart'],'respSoundTimeStart');
%----------------------
if handles.TrialIndex < length(handles.StimOrder)
    set(handles.pushbutton2,'Visible','off')
    posixtime(datetime('now'));
    PlaySound(hObject,handles);
else
    msgbox('Wait','Wait for Assistance!','Warn');
    set(handles.pushbutton1,'Visible','on');
    set(handles.pushbutton3,'Visible','on');
    set(handles.pushbutton5,'Visible','on');
    set(handles.pushbutton6,'Visible','on');
    set(handles.axes1,'Visible','on')
end


% --- Executes on button press in pushbutton3.
function pushbutton4_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
set(handles.axes1,'Visible','off')
resp = GetResponse(handles);
if resp.V1+resp.V2+resp.V3+resp.V4+resp.V5+resp.V6+resp.V7+resp.V8+resp.V9<1, msgbox('Choose one valence score','Choose One!','Warn');return;end;
if resp.V10+resp.V11+resp.V12+resp.V13+resp.V14+resp.V15+resp.V16+resp.V17+resp.V18>1, msgbox('Choose one arousal score','Choose One!','Warn');return;end;

handles.resp(handles.counter) = resp;
handles.counter = handles.counter+1;
resp = handles.resp;
%format long
%resp.time = posixtime(datetime('now'));
a = get(handles.editText,'String');
save (['.\Subject\' num2str(a) 'Sound'],'resp');

respSoundTimeStart.time=posixtime(datetime('now'));%GetTime(handles);
handles.respSoundTimeStart(handles.counter) = respSoundTimeStart;
respSoundTimeStart = handles.respSoundTimeStart;
save (['.\Subject\' num2str(a) 'SoundTimestart'],'respSoundTimeStart');

ResetResponses(handles);
TrialIndex = handles.TrialIndex;
TrialIndex = TrialIndex + 1 ;
handles.TrialIndex = TrialIndex;
if handles.TrialIndex < length(handles.StimOrder)
    set(handles.pushbutton3,'Visible','off');
    PlaySound(hObject,handles);
else
    msgbox('Wait','Wait for Assistance!','Warn');
    set(handles.pushbutton1,'Visible','on');
    set(handles.pushbutton2,'Visible','on');
    set(handles.pushbutton3,'Visible','on');
    set(handles.pushbutton5,'Visible','on');
    set(handles.pushbutton6,'Visible','on');
    set(handles.axes1,'Visible','on');
end
%save ( 'Subject','resp');
guidata(hObject,handles);


function PlaySound (hObject,handles)
set(handles.pushbutton4,'Visible','off')
set(handles.axes1,'Visible','off')
Visibility(handles, 'off')
TrialIndex = handles.TrialIndex; 
StimOrder=handles.StimOrder;
pause(6)


[w,fs_audio] = audioread(['C:\Users\jingp\Desktop\Test\IADSSounds\',StimOrder{TrialIndex }]);
w = w/(20*rms(w));
c = audioplayer(w,fs_audio);
playblocking(c);

Visibility(handles, 'on')
set(handles.pushbutton4,'Visible','on')
guidata(hObject, handles);


function editText_Callback(hObject, eventdata, handles)
% hObject    handle to editText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of editText as text
%        str2double(get(hObject,'String')) returns contents of editText as a double




% --- Executes during object creation, after setting all properties.
function editText_CreateFcn(hObject, eventdata, handles)
% hObject    handle to editText (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end

function respTime = GetTime(handles)
respTime=posixtime(datetime('now'));

function resp = GetResponse(handles)
%resp.time = posixtime(datetime('now'));
resp.V1 = get(handles.radiobutton10,'value');
resp.V2 = get(handles.radiobutton11,'value');
resp.V3 = get(handles.radiobutton12,'value');
resp.V4 = get(handles.radiobutton13,'value');
resp.V5 = get(handles.radiobutton14,'value');
resp.V6 = get(handles.radiobutton15,'value');
resp.V7 = get(handles.radiobutton16,'value');
resp.V8 = get(handles.radiobutton17,'value');
resp.V9 = get(handles.radiobutton18,'value'); 
resp.V10 = get(handles.radiobutton19,'value');
resp.V11 = get(handles.radiobutton20,'value');
resp.V12 = get(handles.radiobutton21,'value');
resp.V13 = get(handles.radiobutton22,'value');
resp.V14 = get(handles.radiobutton23,'value');
resp.V15 = get(handles.radiobutton24,'value');
resp.V16 = get(handles.radiobutton25,'value');
resp.V17 = get(handles.radiobutton26,'value');
resp.V18 = get(handles.radiobutton27,'value');
resp.V19 = get(handles.radiobutton28,'value');
resp.V20 = get(handles.radiobutton29,'value');



function ResetResponses(handles)
set(handles.radiobutton10,'value',0);
set(handles.radiobutton11,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton18,'value',0);
set(handles.radiobutton19,'value',0);
set(handles.radiobutton20,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton27,'value',0);
set(handles.radiobutton28,'value',0);
set(handles.radiobutton29,'value',0);
% if resp.MaleFemale==0
%     if get(handles.radiobutton2,'value')==0
%         resp.MaleFemale = -1;
%     end
% end


% if resp.MaleFemale==0
%     if get(handles.radiobutton2,'value')==0
%         resp.MaleFemale = -1;
%     end
% end


function Visibility(handles, s)
set(handles.uipanel1,'Visible',s);
set(handles.editText,'Visible',s);
set(handles.radiobutton10,'Visible',s);
set(handles.radiobutton11,'Visible',s);
set(handles.radiobutton12,'Visible',s);
set(handles.radiobutton13,'Visible',s);
set(handles.radiobutton14,'Visible',s);
set(handles.radiobutton15,'Visible',s);
set(handles.radiobutton16,'Visible',s);
set(handles.radiobutton17,'Visible',s);
set(handles.radiobutton18,'Visible',s);
set(handles.radiobutton19,'Visible',s);
set(handles.radiobutton20,'Visible',s);
set(handles.radiobutton21,'Visible',s);
set(handles.radiobutton22,'Visible',s);
set(handles.radiobutton23,'Visible',s);
set(handles.radiobutton24,'Visible',s);
set(handles.radiobutton25,'Visible',s);
set(handles.radiobutton26,'Visible',s);
set(handles.radiobutton27,'Visible',s);
set(handles.radiobutton28,'Visible',s);
set(handles.radiobutton29,'Visible',s);
set(handles.text2,'Visible',s);
set(handles.text3,'Visible',s);
set(handles.text4,'Visible',s);
set(handles.text5,'Visible',s);

function radiobutton28_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton10 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton10
set(handles.radiobutton29,'value',0);

function radiobutton29_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton10 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton10
set(handles.radiobutton28,'value',0);


% --- Executes on button press in radiobutton10.
function radiobutton10_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton10 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton10
set(handles.radiobutton11,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton18,'value',0);

% --- Executes on button press in radiobutton11.
function radiobutton11_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton11 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton11
set(handles.radiobutton10,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton18,'value',0);

% --- Executes on button press in radiobutton12.
function radiobutton12_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton12 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton12
set(handles.radiobutton11,'value',0);
set(handles.radiobutton10,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton18,'value',0);


% --- Executes on button press in radiobutton13.
function radiobutton13_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton13 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton13
set(handles.radiobutton11,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton10,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton18,'value',0);


% --- Executes on button press in radiobutton14.
function radiobutton14_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton14 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton14
set(handles.radiobutton11,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton10,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton18,'value',0);


% --- Executes on button press in radiobutton15.
function radiobutton15_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton15 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton15
set(handles.radiobutton11,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton10,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton18,'value',0);


% --- Executes on button press in radiobutton16.
function radiobutton16_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton16 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton16
set(handles.radiobutton11,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton10,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton18,'value',0);

% --- Executes on button press in radiobutton17.
function radiobutton17_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton17 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton17
set(handles.radiobutton11,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton10,'value',0);
set(handles.radiobutton18,'value',0);

% --- Executes on button press in radiobutton18.
function radiobutton18_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton18 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% Hint: get(hObject,'Value') returns toggle state of radiobutton18
set(handles.radiobutton11,'value',0);
set(handles.radiobutton12,'value',0);
set(handles.radiobutton13,'value',0);
set(handles.radiobutton14,'value',0);
set(handles.radiobutton15,'value',0);
set(handles.radiobutton16,'value',0);
set(handles.radiobutton17,'value',0);
set(handles.radiobutton10,'value',0);


% --- Executes on button press in radiobutton19.
function radiobutton19_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton19 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton19
set(handles.radiobutton20,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton27,'value',0);

% --- Executes on button press in radiobutton20.
function radiobutton20_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton20 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton20
set(handles.radiobutton19,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton27,'value',0);

% --- Executes on button press in radiobutton21.
function radiobutton21_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton21 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton21
set(handles.radiobutton20,'value',0);
set(handles.radiobutton19,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton27,'value',0);

% --- Executes on button press in radiobutton22.
function radiobutton22_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton22 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton22
set(handles.radiobutton20,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton19,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton27,'value',0);

% --- Executes on button press in radiobutton23.
function radiobutton23_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton23 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton23
set(handles.radiobutton20,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton19,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton27,'value',0);

% --- Executes on button press in radiobutton24.
function radiobutton24_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton24 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton24
set(handles.radiobutton20,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton19,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton27,'value',0);

% --- Executes on button press in radiobutton25.
function radiobutton25_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton25 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton25
set(handles.radiobutton20,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton19,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton27,'value',0);

% --- Executes on button press in radiobutton26.
function radiobutton26_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton26 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton26
set(handles.radiobutton20,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton19,'value',0);
set(handles.radiobutton27,'value',0);

% --- Executes on button press in radiobutton27.
function radiobutton27_Callback(hObject, eventdata, handles)
% hObject    handle to radiobutton27 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hint: get(hObject,'Value') returns toggle state of radiobutton27
set(handles.radiobutton20,'value',0);
set(handles.radiobutton21,'value',0);
set(handles.radiobutton22,'value',0);
set(handles.radiobutton23,'value',0);
set(handles.radiobutton24,'value',0);
set(handles.radiobutton25,'value',0);
set(handles.radiobutton26,'value',0);
set(handles.radiobutton19,'value',0);

% --- Executes during object creation, after setting all properties.
function text6_CreateFcn(hObject, eventdata, handles)
% hObject    handle to text6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

function pushbutton5_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton5 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% Start
set(handles.editText,'enable','off');
set(handles.text6,'Visible','off');
set(handles.text7,'Visible','off');
set(handles.pushbutton1,'Visible','off');
set(handles.pushbutton3,'Visible','off');
set(handles.pushbutton2,'Visible','off');
set(handles.pushbutton4,'Visible','off');
set(handles.pushbutton5,'Visible','off');
set(handles.axes1,'Visible','on');
load('VideoStim.mat')
handles.VideoStimOrder = VideoStimOrder;
guidata(hObject,handles);
%----------------------
a = get(handles.editText,'String');
respVideoTimeStart.time=posixtime(datetime('now'));%GetTime(handles);
handles.respVideoTimeStart(handles.counter) = respVideoTimeStart;
respVideoTimeStart = handles.respVideoTimeStart;
save (['.\Subject\' num2str(a) 'VideoTimestart'],'respVideoTimeStart');

%----------------------
if handles.VideoTrialIndex < length(handles.VideoStimOrder)
    set(handles.pushbutton2,'Visible','off')
    posixtime(datetime('now'));
    PlayVideo(hObject,handles);
else
    msgbox('Wait','Wait for Assistance!','Warn');
    set(handles.pushbutton1,'Visible','on');
    set(handles.pushbutton3,'Visible','on');
    set(handles.pushbutton2,'Visible','on');
    set(handles.pushbutton4,'Visible','on');
    set(handles.pushbutton5,'Visible','on');
end


% --- Executes on button press in pushbutton3.
function pushbutton6_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton6 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
respVideo = GetResponse(handles);
if respVideo.V1+respVideo.V2+respVideo.V3+respVideo.V4+respVideo.V5+respVideo.V6+respVideo.V7+respVideo.V8+respVideo.V9<1, msgbox('Choose one valence score','Choose One!','Warn');return;end;
if respVideo.V10+respVideo.V11+respVideo.V12+respVideo.V13+respVideo.V14+respVideo.V15+respVideo.V16+respVideo.V17+respVideo.V18>1, msgbox('Choose one arousal score','Choose One!','Warn');return;end;

handles.respVideo(handles.counter) = respVideo;
handles.counter = handles.counter+1;
respVideo = handles.respVideo;
%format long
%resp.time = posixtime(datetime('now'));
a = get(handles.editText,'String');
save (['.\Subject\' num2str(a) 'Video'],'respVideo');

respVideoTimeStart.time=posixtime(datetime('now'));%GetTime(handles);
handles.respVideoTimeStart(handles.counter) = respVideoTimeStart;
respVideoTimeStart = handles.respVideoTimeStart;
save (['.\Subject\' num2str(a) 'VideoTimestart'],'respVideoTimeStart');


ResetResponses(handles);
VideoTrialIndex = handles.VideoTrialIndex;
VideoTrialIndex = VideoTrialIndex + 2 ;
handles.VideoTrialIndex = VideoTrialIndex;
if handles.VideoTrialIndex < length(handles.VideoStimOrder)
    set(handles.pushbutton5,'Visible','off');
    PlayVideo(hObject,handles);
else
    msgbox('Wait','Wait for Assistance!','Warn');
    set(handles.pushbutton1,'Visible','on');
    set(handles.pushbutton2,'Visible','on');
    set(handles.pushbutton3,'Visible','on');
    set(handles.pushbutton5,'Visible','on');
    set(handles.pushbutton4,'Visible','on');
end
%save ( 'Subject','resp');
guidata(hObject,handles);


function PlayVideo (hObject,handles)
set(handles.pushbutton6,'Visible','off')
Visibility(handles, 'off')
VideoTrialIndex = handles.VideoTrialIndex; 
axes(handles.axes1);
VideoStimOrder=handles.VideoStimOrder;
[w,fs_audio] = audioread('C:\Users\jingp\Desktop\Test\chirp.wav');
w = w/(20*rms(w));
c = audioplayer(w,fs_audio);
playblocking(c);

a = imread('C:\Users\jingp\Desktop\Test\GrayscalePic\GRAY1.jpg');%IAPSImages\',picture{PictureTrialIndex}]);
axes(handles.axes1)
imshow(a)
pause(6)

% respVideoTimeStart=GetTime(handles);
% handles.respVideoTimeStart(handles.counter) = respVideoTimeStart;
% respVideoTimeStart = handles.respVideoTimeStart;
% %format long
% %resp.time = posixtime(datetime('now'));
% a = get(handles.editText,'String');
% save (['.\Subject\' num2str(a) 'VideoTimeStart'],'respVideoTimeStart');
% 
videoObject = VideoReader(['C:\Users\jingp\Desktop\Test\FunnyVideo\',VideoStimOrder{VideoTrialIndex+1}]);
for frameCount = 1:videoObject.NumberOfFrames
    % Display frames
    frame = read(videoObject,frameCount);
    imshow(frame);
    drawnow;
end

% respVideoTimeEnd=GetTime(handles);
% handles.respVideoTimeEnd(handles.counter) = respVideoTimeEnd;
% respVideoTimeEnd = handles.respVideoTimeEnd;
% %format long
% %resp.time = posixtime(datetime('now'));
% a = get(handles.editText,'String');
% save (['.\Subject\' num2str(a) 'VideoTimeEnd'],'respVideoTimeEnd');

[w,fs_audio] = audioread('C:\Users\jingp\Desktop\Test\chirp.wav');
w = w/(20*rms(w));
c = audioplayer(w,fs_audio);
playblocking(c);

Visibility(handles, 'on')
set(handles.pushbutton6,'Visible','on')
guidata(hObject, handles);
