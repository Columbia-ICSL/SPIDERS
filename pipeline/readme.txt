Description (from abstract):
SPIDERS, short for System for Processing In-situ Bio-signal Data for Emotion Recognition and Sensing, is a bio-signal acquisition and processing system that is wireless, low-cost, user-friendly, and comfortable to wear. SPIDERS provides robust data collection and analysis pipelines for 6 sensing modalities included in our core function library, and enables advanced functionalities including emotion classification and affective state monitoring. Utilizing the suite of eye landmark localization and eyebrow motion tracking algorithms provided by the SPIDERS platform, we propose a 5-class facial expression classification model solely dependent on raw, gray-scale eye image inputs, which achieves a 79.62% average prediction accuracy.
The current program serves as the back-end pipeline that processes data wirelessly streamed from the wearable device. Eventually, it is expected to output time-series affective state predictions and pre-processed bio-signal data in a cleaner and more accessible form for the user's purposes.

Starting the project: 
1. Stream .jpg eye images into the subdirectory named "pictures" that is located within the main directory
2. Check file paths for inputting eye images and saved CNN model in pipeline.py
3. run $ python3 pipeline.py

Note: right now, only the first part of the data processing pipeline (namely, the facial expression classification pipeline) is fully tested and ready for use.