import numpy as np
import os
import random
import cv2
import torch
import cv2
import urllib.request
import numpy as np
import time
import cv2
import torch

#!/usr/bin/env python

import torch
import time
import getopt
import math
import numpy
import os
import PIL
import PIL.Image
import sys


from correlation import correlation # the custom cost volume layer
# end

##########################################################

#assert(int(str('').join(torch.__version__.split('.')[0:3])) >= 41) # requires at least pytorch version 0.4.1

torch.set_grad_enabled(False) # make sure to not compute gradients for computational performance

torch.backends.cudnn.enabled = True # make sure to use cudnn for computational performance

##########################################################
'''
arguments_strModel = 'default'
arguments_strFirst = './images/first.png'
arguments_strSecond = './images/second.png'
arguments_strOut = './out.flo'


for strOption, strArgument in getopt.getopt(sys.argv[1:], '', [ strParameter[2:] + '=' for strParameter in sys.argv[1::2] ])[0]:
	if strOption == '--model' and strArgument != '': arguments_strModel = strArgument # which model to use
	if strOption == '--first' and strArgument != '': arguments_strFirst = strArgument # path to the first frame
	if strOption == '--second' and strArgument != '': arguments_strSecond = strArgument # path to the second frame
	if strOption == '--out' and strArgument != '': arguments_strOut = strArgument # path to where the output should be stored
# end
'''
arguments_strModel = 'default'
'''
arguments_strFirst = '/content/0.jpg'
arguments_strSecond = '/content/75.jpg'
arguments_strOut = '/content/out.flo'
'''
##########################################################

Backward_tensorGrid = {}
Backward_tensorPartial = {}

def Backward(tensorInput, tensorFlow):
	if str(tensorFlow.size()) not in Backward_tensorGrid:
		tensorHorizontal = torch.linspace(-1.0, 1.0, tensorFlow.size(3)).view(1, 1, 1, tensorFlow.size(3)).expand(tensorFlow.size(0), -1, tensorFlow.size(2), -1)
		tensorVertical = torch.linspace(-1.0, 1.0, tensorFlow.size(2)).view(1, 1, tensorFlow.size(2), 1).expand(tensorFlow.size(0), -1, -1, tensorFlow.size(3))

		Backward_tensorGrid[str(tensorFlow.size())] = torch.cat([ tensorHorizontal, tensorVertical ], 1).cuda()
	# end

	if str(tensorFlow.size()) not in Backward_tensorPartial:
		Backward_tensorPartial[str(tensorFlow.size())] = tensorFlow.new_ones([ tensorFlow.size(0), 1, tensorFlow.size(2), tensorFlow.size(3) ])
	# end

	tensorFlow = torch.cat([ tensorFlow[:, 0:1, :, :] / ((tensorInput.size(3) - 1.0) / 2.0), tensorFlow[:, 1:2, :, :] / ((tensorInput.size(2) - 1.0) / 2.0) ], 1)
	tensorInput = torch.cat([ tensorInput, Backward_tensorPartial[str(tensorFlow.size())] ], 1)

	tensorOutput = torch.nn.functional.grid_sample(input=tensorInput, grid=(Backward_tensorGrid[str(tensorFlow.size())] + tensorFlow).permute(0, 2, 3, 1), mode='bilinear', padding_mode='zeros')

	tensorMask = tensorOutput[:, -1:, :, :]; tensorMask[tensorMask > 0.999] = 1.0; tensorMask[tensorMask < 1.0] = 0.0

	return tensorOutput[:, :-1, :, :] * tensorMask
# end

##########################################################

class Network(torch.nn.Module):
	def __init__(self):
		super(Network, self).__init__()

		class Extractor(torch.nn.Module):
			def __init__(self):
				super(Extractor, self).__init__()

				self.moduleOne = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, stride=2, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=16, out_channels=16, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleTwo = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=2, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleThr = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=2, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleFou = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=64, out_channels=96, kernel_size=3, stride=2, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=96, out_channels=96, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=96, out_channels=96, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleFiv = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=96, out_channels=128, kernel_size=3, stride=2, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleSix = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=128, out_channels=196, kernel_size=3, stride=2, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=196, out_channels=196, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=196, out_channels=196, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)
			# end

			def forward(self, tensorInput):
				tensorOne = self.moduleOne(tensorInput)
				tensorTwo = self.moduleTwo(tensorOne)
				tensorThr = self.moduleThr(tensorTwo)
				tensorFou = self.moduleFou(tensorThr)
				tensorFiv = self.moduleFiv(tensorFou)
				tensorSix = self.moduleSix(tensorFiv)

				return [ tensorOne, tensorTwo, tensorThr, tensorFou, tensorFiv, tensorSix ]
			# end
		# end

		class Decoder(torch.nn.Module):
			def __init__(self, intLevel):
				super(Decoder, self).__init__()

				intPrevious = [ None, None, 81 + 32 + 2 + 2, 81 + 64 + 2 + 2, 81 + 96 + 2 + 2, 81 + 128 + 2 + 2, 81, None ][intLevel + 1]
				intCurrent = [ None, None, 81 + 32 + 2 + 2, 81 + 64 + 2 + 2, 81 + 96 + 2 + 2, 81 + 128 + 2 + 2, 81, None ][intLevel + 0]

				if intLevel < 6: self.moduleUpflow = torch.nn.ConvTranspose2d(in_channels=2, out_channels=2, kernel_size=4, stride=2, padding=1)
				if intLevel < 6: self.moduleUpfeat = torch.nn.ConvTranspose2d(in_channels=intPrevious + 128 + 128 + 96 + 64 + 32, out_channels=2, kernel_size=4, stride=2, padding=1)
				if intLevel < 6: self.dblBackward = [ None, None, None, 5.0, 2.5, 1.25, 0.625, None ][intLevel + 1]

				self.moduleOne = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=intCurrent, out_channels=128, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleTwo = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=intCurrent + 128, out_channels=128, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleThr = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=intCurrent + 128 + 128, out_channels=96, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleFou = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=intCurrent + 128 + 128 + 96, out_channels=64, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleFiv = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=intCurrent + 128 + 128 + 96 + 64, out_channels=32, kernel_size=3, stride=1, padding=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1)
				)

				self.moduleSix = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=intCurrent + 128 + 128 + 96 + 64 + 32, out_channels=2, kernel_size=3, stride=1, padding=1)
				)
			# end

			def forward(self, tensorFirst, tensorSecond, objectPrevious):
				tensorFlow = None
				tensorFeat = None

				if objectPrevious is None:
					tensorFlow = None
					tensorFeat = None

					tensorVolume = torch.nn.functional.leaky_relu(input=correlation.FunctionCorrelation(tensorFirst=tensorFirst, tensorSecond=tensorSecond), negative_slope=0.1, inplace=False)

					tensorFeat = torch.cat([ tensorVolume ], 1)

				elif objectPrevious is not None:
					tensorFlow = self.moduleUpflow(objectPrevious['tensorFlow'])
					tensorFeat = self.moduleUpfeat(objectPrevious['tensorFeat'])

					tensorVolume = torch.nn.functional.leaky_relu(input=correlation.FunctionCorrelation(tensorFirst=tensorFirst, tensorSecond=Backward(tensorInput=tensorSecond, tensorFlow=tensorFlow * self.dblBackward)), negative_slope=0.1, inplace=False)

					tensorFeat = torch.cat([ tensorVolume, tensorFirst, tensorFlow, tensorFeat ], 1)

				# end

				tensorFeat = torch.cat([ self.moduleOne(tensorFeat), tensorFeat ], 1)
				tensorFeat = torch.cat([ self.moduleTwo(tensorFeat), tensorFeat ], 1)
				tensorFeat = torch.cat([ self.moduleThr(tensorFeat), tensorFeat ], 1)
				tensorFeat = torch.cat([ self.moduleFou(tensorFeat), tensorFeat ], 1)
				tensorFeat = torch.cat([ self.moduleFiv(tensorFeat), tensorFeat ], 1)

				tensorFlow = self.moduleSix(tensorFeat)

				return {
					'tensorFlow': tensorFlow,
					'tensorFeat': tensorFeat
				}
			# end
		# end

		class Refiner(torch.nn.Module):
			def __init__(self):
				super(Refiner, self).__init__()

				self.moduleMain = torch.nn.Sequential(
					torch.nn.Conv2d(in_channels=81 + 32 + 2 + 2 + 128 + 128 + 96 + 64 + 32, out_channels=128, kernel_size=3, stride=1, padding=1, dilation=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=2, dilation=2),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=4, dilation=4),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=128, out_channels=96, kernel_size=3, stride=1, padding=8, dilation=8),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=96, out_channels=64, kernel_size=3, stride=1, padding=16, dilation=16),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=64, out_channels=32, kernel_size=3, stride=1, padding=1, dilation=1),
					torch.nn.LeakyReLU(inplace=False, negative_slope=0.1),
					torch.nn.Conv2d(in_channels=32, out_channels=2, kernel_size=3, stride=1, padding=1, dilation=1)
				)
			# end

			def forward(self, tensorInput):
				return self.moduleMain(tensorInput)
			# end
		# end

		self.moduleExtractor = Extractor()

		self.moduleTwo = Decoder(2)
		self.moduleThr = Decoder(3)
		self.moduleFou = Decoder(4)
		self.moduleFiv = Decoder(5)
		self.moduleSix = Decoder(6)

		self.moduleRefiner = Refiner()

		self.load_state_dict(torch.load('./network-' + arguments_strModel + '.pytorch'))
	# end

	def forward(self, tensorFirst, tensorSecond):
		tensorFirst = self.moduleExtractor(tensorFirst)
		tensorSecond = self.moduleExtractor(tensorSecond)

		objectEstimate = self.moduleSix(tensorFirst[-1], tensorSecond[-1], None)
		objectEstimate = self.moduleFiv(tensorFirst[-2], tensorSecond[-2], objectEstimate)
		objectEstimate = self.moduleFou(tensorFirst[-3], tensorSecond[-3], objectEstimate)
		objectEstimate = self.moduleThr(tensorFirst[-4], tensorSecond[-4], objectEstimate)
		objectEstimate = self.moduleTwo(tensorFirst[-5], tensorSecond[-5], objectEstimate)

		return objectEstimate['tensorFlow'] + self.moduleRefiner(objectEstimate['tensorFeat'])
	# end
# end

moduleNetwork = Network().cuda().eval()


import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.conv3 = nn.Conv2d(64, 64, 3, 1)
        self.conv4 = nn.Conv2d(64, 128, 3, 1)
        self.conv5 = nn.Conv2d(128, 128, 3, 1)
        self.conv6 = nn.Conv2d(128, 256, 3, 1)
        self.fc1 = nn.Linear(32256, 1024)
        self.fc2 = nn.Linear(1024, 54)

    def forward(self, x):
        batch_size = x.size(0)
        img_H = x.size(1)
        img_W = x.size(2)
        x = x.unsqueeze(1)
        x = F.relu(self.conv1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv3(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv6(x))
        x = x.view(-1, 32256)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
        
save_model=Net()
save_model=save_model.cuda()
save_model.load_state_dict(torch.load('model_04112020.pt'))
save_model = save_model.eval()  

tr_img_mean = np.array(124.063805, dtype = np.float32)
tr_img_std = np.array(65.97971, dtype = np.float32)

tr_points_mean = np.array([ 83.708336,  59.916668, 265.98334 ,  48.958332, 179.74167 ,
        57.616665, 134.425   ,  60.041668, 226.86667 ,  52.591667,
       110.041664,  60.75    , 157.38333 ,  59.883335, 204.04167 ,
        55.366665, 248.05833 ,  50.666668,  97.99167 ,  70.433334,
       256.2     ,  60.708332, 184.275   , 105.683334, 136.61667 ,
        98.40833 , 231.01666 ,  88.066666, 116.5     ,  87.075   ,
       160.3     , 105.8     , 210.375   ,  99.958336, 245.49167 ,
        75.34167 ,  27.1     , 143.625   , 306.675   , 160.475   ,
       169.41667 , 186.95833 ,  96.041664, 175.075   , 247.675   ,
       180.825   ,  61.816666, 161.98334 , 132.85834 , 184.15834 ,
       210.575   , 186.225   , 280.85834 , 171.48334 ], dtype = np.float32)

tr_points_std = np.array([22.97232  , 18.773466 , 17.912277 , 17.107819 , 11.454072 ,
       20.301554 , 16.011148 , 20.068277 , 13.016294 , 19.4783   ,
       19.072514 , 19.572195 , 12.921676 , 20.501295 , 10.903856 ,
       20.271255 , 15.386978 , 18.40237  , 25.578554 , 17.38641  ,
       19.22156  , 16.603033 , 13.67797  , 18.017113 , 21.160175 ,
       16.366758 , 15.731329 , 15.275926 , 23.69353  , 15.900688 ,
       16.994165 , 17.637836 , 13.37243  , 16.367472 , 17.77463  ,
       15.0741205,  8.620132 ,  9.716663 ,  4.4420576,  6.8169065,
        8.883584 ,  8.164094 ,  8.662318 ,  7.5767326,  5.7262735,
        7.3732767,  8.518591 ,  8.187372 ,  8.1675625,  8.261604 ,
        7.0909715,  8.325375 ,  4.358987 ,  6.985083 ], dtype = np.float32)

#Calculate eye size
from scipy import optimize

def curve_function(x, a, b, c, d, e, f):
  return a * x ** 5 + b * x ** 4 + c * x ** 3 + d * x ** 2 + e * x + f
'''
def curve_function(x, b, c, d, e, f):
  return b * x ** 4 + c * x ** 3 + d * x ** 2 + e * x + f
'''
def cal_eye_size(img_cords):
  upper_eye = img_cords[:9]
  lower_eye = img_cords[9:18]
  upper_popt, upper_pcov = optimize.curve_fit(curve_function, upper_eye[:, 0], upper_eye[:, 1])
  lower_popt, lower_pcov = optimize.curve_fit(curve_function, lower_eye[:, 0], lower_eye[:, 1])
  xaxes = np.arange(img_cords[0][0],img_cords[1][0],1)
  upper = curve_function(xaxes, *upper_popt)
  lower = curve_function(xaxes, *lower_popt)
  size = np.sum(((lower-upper)>0).astype(int)*(lower-upper))
  return size  

#Calculate eyebrow state
def cal_eyebrow_state(optical_flow,img_cords):
    eyebrow_points = np.array((img_cords[19],img_cords[26],img_cords[22],img_cords[25],img_cords[20],img_cords[24]))
    #eyebrow_points = np.array((img_cords[26],img_cords[22],img_cords[25],img_cords[20],img_cords[24],img_cords[21]))
    #eyebrow_points = np.array((img_cords[22],img_cords[25],img_cords[20],img_cords[24],img_cords[21],img_cords[23]))
    eyebrow_popt, eyebrow_pcov = optimize.curve_fit(curve_function, eyebrow_points[:, 0], eyebrow_points[:, 1])
    xaxes = np.arange(int(eyebrow_points[5][0]),int(eyebrow_points[0][0]),1)
    #eyebrow = curve_function(xaxes, *eyebrow_popt))
    eyebrow_flow = np.array([0,0],dtype='f')
    eyebrow_flow_true = np.array([0,0],dtype='f')
    for x in xaxes:
        x = int(max(0,min(x, 319)))
        eyebrow_flow[0] += np.mean(optical_flow[0,int(max(0,min(curve_function(x, *eyebrow_popt), 319))):int(max(0,min((curve_function(x, *eyebrow_popt)+30),319))),x])
        eyebrow_flow[1] += np.mean(optical_flow[1,int(max(0,min(curve_function(x, *eyebrow_popt), 319))):int(max(0,min((curve_function(x, *eyebrow_popt)+40),319))),x])
    eyebrow_flow[0] /= len(xaxes)
    eyebrow_flow[1] /= len(xaxes)
    #eyebrow_flow_true[0] = eyebrow_flow[0] + eyebrow_flow[1]
    #eyebrow_flow_true[1] = 0.2*eyebrow_flow[0] + eyebrow_flow[1]
    return eyebrow_flow#_true


##########################################################

def estimate(tensorFirst, tensorSecond):
	assert(tensorFirst.size(1) == tensorSecond.size(1))
	assert(tensorFirst.size(2) == tensorSecond.size(2))

	intWidth = tensorFirst.size(2)
	intHeight = tensorFirst.size(1)

	#assert(intWidth == 1024) # remember that there is no guarantee for correctness, comment this line out if you acknowledge this and want to continue
	#assert(intHeight == 436) # remember that there is no guarantee for correctness, comment this line out if you acknowledge this and want to continue

	tensorPreprocessedFirst = tensorFirst.cuda().view(1, 3, intHeight, intWidth)
	tensorPreprocessedSecond = tensorSecond.cuda().view(1, 3, intHeight, intWidth)

	intPreprocessedWidth = int(math.floor(math.ceil(intWidth / 64.0) * 64.0))
	intPreprocessedHeight = int(math.floor(math.ceil(intHeight / 64.0) * 64.0))

	tensorPreprocessedFirst = torch.nn.functional.interpolate(input=tensorPreprocessedFirst, size=(intPreprocessedHeight, intPreprocessedWidth), mode='bilinear', align_corners=False)
	tensorPreprocessedSecond = torch.nn.functional.interpolate(input=tensorPreprocessedSecond, size=(intPreprocessedHeight, intPreprocessedWidth), mode='bilinear', align_corners=False)

	tensorFlow = 20.0 * torch.nn.functional.interpolate(input=moduleNetwork(tensorPreprocessedFirst, tensorPreprocessedSecond), size=(intHeight, intWidth), mode='bilinear', align_corners=False)

	tensorFlow[:, 0, :, :] *= float(intWidth) / float(intPreprocessedWidth)
	tensorFlow[:, 1, :, :] *= float(intHeight) / float(intPreprocessedHeight)

	return tensorFlow[0, :, :, :].clone().cpu().detach().numpy()
# end
##########################################################
# end

#stream = urllib.request.urlopen('http://160.39.225.43:81/stream')
stream = urllib.request.urlopen('http://192.168.137.90:81/stream')
bytes = bytes()
eyebrow_state = np.array([0,0])
init_flag = False
frame = 255*np.ones((480, 970, 3), dtype=np.uint8)
size_buff = 8000*np.ones(100)
smooth_size_buff = 8000*np.ones(100)
move_buff = np.ones((2,100))
smooth_move_buff = np.ones((2,100))
pupil_buff = np.ones(100)
smooth_pupil_buff = np.ones(100)
plots = np.ones((100,2),np.int32)
plots[:,0] = np.arange(330,630,3)
valence = 0
pupil_size = 0
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'datastart')
    b = bytes.find(b'dataend')
    #c = bytes.find(b'accgyrostart')
    #d = bytes.find(b'accgyroend')
    if a != -1 and b != -1:# and c != -1 and d != -1:
        T=time.time()
        jpg = bytes[a+9:b]
        #accgyro = bytes[b:b+100]
        bytes = bytes[b+7:]
        #print(accgyro)
        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        
        
        gray=img[:,:,0]
        sketch=cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,5)
        threshold_value=65
        rat,binary=cv2.threshold(gray,threshold_value,255,cv2.THRESH_BINARY_INV)
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        opening=cv2.morphologyEx(binary,cv2.MORPH_OPEN,kernel)
        kernel=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        closing=cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel)
        contours, _ = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if  area > 10000 or area < 400:
                continue
            #convex=cv2.convexHull(cnt)
            ellipse_fit = cv2.fitEllipse(cnt)
            pupil_size = max(ellipse_fit[1])
            #print(pupil_size)
            cv2.ellipse(img,ellipse_fit,(0,255,0),2)
        
        #Landmarks of the emotional image
        img_ = img[:,:,0]
        img_ = (img_-tr_img_mean)/tr_img_std
        img_points = save_model(torch.unsqueeze(torch.from_numpy(img_).cuda(),0)).clone().cpu().detach().numpy()*tr_points_std+tr_points_mean
        img_cords = np.zeros((27,2))
        img_cords[:,0] = img_points[0][::2]
        img_cords[:,1] = img_points[0][1::2]
        #eye_brow_center_cord = np.mean(img_cords[18:26],axis=0)
        #Eye size of the emotional image
        eye_size = cal_eye_size(img_cords)
        #Calculate optical flow
        if init_flag:
            tensorFirst = torch.FloatTensor(old_img[:, :, ::-1].transpose(2, 0, 1).astype(numpy.float32) * (1.0 / 255.0))
            tensorSecond = torch.FloatTensor(img[:, :, ::-1].transpose(2, 0, 1).astype(numpy.float32) * (1.0 / 255.0))
            optical_flow = estimate(tensorFirst, tensorSecond)
            eyebrow_state = cal_eyebrow_state(optical_flow, img_cords)
        old_img = img
        init_flag = True
        #print(T, eye_size, eyebrow_state)
        size_buff[:-1] = size_buff[1:]
        size_buff[-1] = eye_size
        smooth_size_buff[:-1] = smooth_size_buff[1:]
        smooth_size_buff[-1] = np.mean(size_buff[-4:])
        move_buff[:,:-1] = move_buff[:,1:]
        move_buff[:,-1] = eyebrow_state
        smooth_move_buff[:,:-1] = smooth_move_buff[:,1:]
        smooth_move_buff[:,-1] = np.mean(move_buff[:,-3:],axis=1)
        pupil_buff[:-1] = pupil_buff[1:]
        pupil_buff[-1] = pupil_size
        smooth_pupil_buff[:-1] = smooth_pupil_buff[1:]
        smooth_pupil_buff[-1] = np.mean(pupil_buff[-4:])
        for i in range(27):
          cv2.circle(img, (int(img_cords[i,0]),int(img_cords[i,1])), 4, (255,0,0), -1)
        frame = 255*np.ones((480, 970, 3), dtype=np.uint8)
        #frame[0:240, 0:320,:] = img[::-1,:,:]
        frame[0:240, 650:970,:] = img[::-1,:,:]
        if smooth_move_buff[0,-1]>1:
            valence = 1
        if (smooth_move_buff[0,-1]<-1.5):
            valence = 0
        if smooth_size_buff[-1]<6000:
            eye = 0
        else:
            eye = 1
        #print(valence)
        frame=cv2.line(frame, (330,0), (330,480), (0,0,0))
        frame=cv2.line(frame, (330,165), (640,165), (0,0,0))
        frame=cv2.line(frame, (330,325), (640,325), (0,0,0))
        
        frame=cv2.line(frame, (640,0), (640,650), (0,0,0))
        
        frame=cv2.line(frame, (650,250), (650,480), (0,0,0))
        frame=cv2.line(frame, (650,250), (970,250), (0,0,0))  

        plots[:,0] = np.arange(330,630,3)
        
        plots[:,1] = np.clip((160-smooth_size_buff/120),10,160)
        plots.astype(int)
        frame=cv2.polylines(frame, [plots], False, (0,0,0), 1)
        
        plots[:,1] = np.clip((245+smooth_move_buff[0,:]*14),170,320)
        plots.astype(int)
        frame=cv2.polylines(frame, [plots], False, (0,0,0), 1)
        
        plots[:,1] =np.clip((400+smooth_move_buff[1,:]*14),330,470)
        plots.astype(int)
        frame=cv2.polylines(frame, [plots], False, (0,0,0), 1)
        
        plots[:,1] = np.clip((480-3*smooth_pupil_buff),250,480)
        plots[:,0] = np.arange(660,960,3)
        plots.astype(int)
        frame=cv2.polylines(frame, [plots], False, (0,0,0), 1)
        
        if valence == 0 and eye == 0:
            cv2.putText(frame, "Happy", (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)
        elif valence == 0 and eye == 1:
            cv2.putText(frame, "Neutral", (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)
        elif valence == 1 and eye == 0:
            cv2.putText(frame, "Disgusted", (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)
        elif valence == 1 and eye == 1:
            cv2.putText(frame, "Angry", (100, 350), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), lineType=cv2.LINE_AA)
        
        cv2.putText(frame, "Eye size", (450, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), lineType=cv2.LINE_AA)
        cv2.putText(frame, "Horizontal Movement", (415, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), lineType=cv2.LINE_AA)
        cv2.putText(frame, "Vertical Movement", (425, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), lineType=cv2.LINE_AA)
        cv2.putText(frame, "Pupil Size", (770, 270), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), lineType=cv2.LINE_AA)
        
        
        cv2.imshow('blink',frame)
        if cv2.waitKey(1) == ord('q'):
            exit(0)