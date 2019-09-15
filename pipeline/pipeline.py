from fe_state_map import fe_state_map
from pupil_processing import pupil_processing

# defining file paths
EXPORT_DIR = 'saved_model' # dir for trained models
PIC_DIR = 'pictures' # dir for eye images

# getting facial expression predictions based on cnn model and eye images:
state_map = fe_state_map(EXPORT_DIR, PIC_DIR)

# # pupillometry pre-processing:
# pupil_data = pupil_processing(PUPIL_FILE)
