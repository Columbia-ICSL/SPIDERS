"""
parameters:

SQUINT_THRESH = -24.76 # might want to change later
PT_LENGTH = 54 # 27 landmark points used
ROW = 240 # img size
COL = 320
EYE_SIZE_RANGE = 2000 # used to calculate eye size baseline
PEAK_DIST = 30 # used to find motion acceleration peaks
PEAK_PROM = 100
FS = 25
WINDOW = 0.15 # time range over which the peak strength is integrated
SMOOTH_WIN = 3 # for smoothing state maps
"""

def fe_state_map(EXPORT_DIR, PIC_DIR, SQUINT_THRESH = -24.76, PT_LENGTH = 54, \
                 ROW = 240, COL = 320, EYE_SIZE_RANGE = 2000, PEAK_DIST = 30, \
                 PEAK_PROM = 100, FS = 25, WINDOW = 0.15, SMOOTH_WIN = 3):
    from tensorflow.contrib import predictor
    from pathlib import Path
    from PIL import Image
    import numpy as np
    import tensorflow as tf
    import matplotlib.pyplot as plt
    from calc_eye_size_state import calc_eye_size_state
    from calc_eyebrow_state import calc_eyebrow_state
    from plot_confusion_matrix import plot_confusion_matrix as plt_cm
    import io, os

    # holds the state information for each time point
    class time_pt_info:

        def __init__(self, filename, pts):
            self.filename = filename
            self.time = float(filename.split(os.path.sep)[-1].strip()[:-4])
            self.pts = pts
        def __repr__(self):
            return str(self.time) + " " + str(self.pts) + "\n"
        def set_area(self, area):
            self.area = area
        def set_eye_size_state(self, state):
            self.eye_size_state = state
        def set_integrals(self, x_integrals, y_integrals):
            self.x_integrals = x_integrals
            self.y_integrals = y_integrals

    def encode_img (filename):
        pil_im = Image.fromarray(plt.imread(filename))
        b = io.BytesIO()
        pil_im.save(b, 'jpeg')
        return b.getvalue()

    def vanilla_get_class(area_state, eyebrow_state):
        ans = []
        for i in range(len(area_state)):
            if area_state[i] == 0:
                if eyebrow_state[i] == 0:
                    ans.append('neutral/sad')
                elif eyebrow_state[i] == 1:
                    ans.append('surprised')
                else:
                    ans.append('angry/fearful')
            else:
                if eyebrow_state[i] == -1:
                    ans.append('disgusted')
                else:
                    ans.append('happy')
        return ans


    # landmark generation ---------------------------
    print("=======================starting landmark generation=======================")
    # finding latest trained model and generating prediction for imgs in filenames
    filenames = [str(x) for x in Path(PIC_DIR).iterdir() if 'jpg' in str(x)]
    subdirs = [x for x in Path(EXPORT_DIR).iterdir() if x.is_dir() and 'temp' not in str(x)]
    latest = str(sorted(subdirs)[-1])
    predictor_fn = predictor.from_saved_model(latest)
    features = {}
    for filename in filenames:
        img_string = encode_img(filename)
        pred = predictor_fn({'image_bytes': [img_string]})['output']
        features[filename] = time_pt_info(filename, pred[0])

    # eye size calculation & state management --------------------------
    # this functions changes the /area/ and /eye_size_state/ attributes of the time_pt_info objects
    # and also sorts the filenames by time
    print("=======================starting eye size state map generation=======================")
    sort_time_fn = lambda filename : features[filename].time
    eye_size_state = calc_eye_size_state(features, filenames, sort_time_fn, SQUINT_THRESH, SMOOTH_WIN, EYE_SIZE_RANGE, PT_LENGTH)
    # motion detection --------------------------
    # this function changes the /integrals/ attribut of the time_pt_info objects,
    # getting state map of eyebrow
    print("=======================starting eyebrow state map generation=======================")
    eyebrow_state = calc_eyebrow_state(features, filenames, SMOOTH_WIN, PEAK_DIST = PEAK_DIST, PEAK_PROM = PEAK_PROM,
                                                  WINDOW = WINDOW, FS = FS)
    print(eyebrow_state, len(eyebrow_state))

    print("=======================starting classifying state maps=======================")
    # getting time-state map
    predictions = vanilla_get_class(eye_size_state, eyebrow_state)
    prediction_time_map = np.concatenate((np.array([features[filename].time for filename in filenames]).reshape(1, -1), \
                                          np.array(predictions).reshape(1, -1)), axis = 0)
    print(predictions)
    return prediction_time_map
