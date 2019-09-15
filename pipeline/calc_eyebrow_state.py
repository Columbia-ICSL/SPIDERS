def calc_eyebrow_state(features, filenames, SMOOTH_WIN, PEAK_DIST = 30, PEAK_PROM = 100, WINDOW = 0.15, FS = 25, PEAK_STRENGTH_THRESH = 60):

    import numpy as np
    from scipy.signal import find_peaks

    def motion_tracking(features, filenames, PT_LENGTH = 54, ROW = 240, COL = 320,
                        MBSIZE = 10, P = 8, STRIDE = 5, STEP = 5, STOP_POINT = 0.6):
        """
        params include:
        MBSIZE: the size of the block of image at each search
        p: the size of the searching area at each search
        STRIDE: the distance each STEP takes
        STEP: the number of STEPs (which defines how many searches are done vertically for each horizontal location of the eyebrow)
        STOP_POINT: stop at this ratio of the length of the eyebrow (horizontally)
        """

        import numpy as np
        import matplotlib.pyplot as plt
        import math
        from exhaustive_search import find_vector

        integrals = np.zeros((2, len(list(features.keys()))))

        # processing each image
        for i in range(len(filenames) - 1):
            if (i % 10 == 0):
                print(i)
            img1 = plt.imread(filenames[i])
            img2 = plt.imread(filenames[i + 1])
            eyebrow = features[filenames[i]].pts[-PT_LENGTH // 3:]

            # fitting the eyebrow curve using a more granular x-axis
            x = eyebrow[0: PT_LENGTH // 3: 2]
            y = eyebrow[1: PT_LENGTH // 3: 2]
            xq = range(math.ceil(x[0]), math.floor(x[-1]))
            yq = np.interp(xq, x, y)
            vectors = np.zeros((2, STEP, int(len(xq) * STOP_POINT) // STRIDE + 1))

            # going along the eyebrow points, and for each point, find the
            # motion vector with respect to the next image in the image
            # sequence using an exhaustic search
            for col in range(0, int(len(xq) * STOP_POINT), STRIDE):
                for row in range(int(yq[col]), int(yq[col]) + (STEP - 1) * STRIDE, STRIDE):
                    dx, dy = find_vector(img1, img2, row, col, MBSIZE, P, ROW, COL)
                    # updating the motion vector map with the motion vector at
                    # the current position
                    vectors[0, (row - int(yq[col])) // STRIDE, col // STRIDE] = dy
                    vectors[1, (row - int(yq[col])) // STRIDE, col // STRIDE] = dx

            # take the sum of all the motion components in the searched area
            integrals[0, i] = np.sum(vectors[0, :, :])
            integrals[1, i] = np.sum(vectors[1, :, :])
            features[filenames[i]].set_integrals(np.sum(vectors[0, :, :]), np.sum(vectors[1, :, :]))

        return integrals

    def get_integral_state_map(peaks, peak_strengths, data_size):
        state_map = np.zeros(data_size)
        peak_counter = 0
        continuing = False
        for i in range(data_size):
            if peak_counter >= len(peaks_filtered) or i < peaks_filtered[peak_counter]:
                state_map[i] = state_map[i - 1]
                continue
            peak_val = peak_strengths[peak_counter, 0] if np.abs(peak_strengths[peak_counter, 0]) > np.abs(peak_strengths[peak_counter, 1])\
                                                        else peak_strengths[peak_counter, 1]
            if continuing and np.sign(peak_val) != np.sign(state_map[i - 1]):
                continuing = False
                state_map[i] = 0
                peak_counter += 1
                continue
            if continuing and np.sign(peak_val) == np.sign(state_map[i - 1]):
                peak_counter += 1
                state_map[i] = state_map[i - 1]
                continue
            if not continuing:
                continuing = True
                state_map[i] = np.sign(peak_val)
                peak_counter += 1
                continue

        # smoothing the state map
        for i in range(len(state_map)):
            for win in range(SMOOTH_WIN, 0):
                if state_map[i] != state_map[i - win] and state_map[i] != state_map[i + win]:
                    state_map[i] = state_map[i - win]
        return state_map

    integrals = motion_tracking(features, filenames)

    print("=======================starting to analyze motion integrals=======================")
    max_data = np.max(np.abs(integrals), axis = 0)
    peaks, __ = find_peaks(max_data, distance = PEAK_DIST, prominence = PEAK_PROM)
    peak_strengths = []
    peaks_filtered = []
    for idx, peak in enumerate(peaks):
        xrange = range(peak - int(WINDOW * FS), peak + int(WINDOW * FS) + 1)
        integ = (np.sum(integrals[:, xrange], axis = 0) * 1 / FS).reshape(-1)
        if np.max(np.abs(integ)) > PEAK_STRENGTH_THRESH1:
            peak_strengths.append(integ)
            peaks_filtered.append(peak)
    peak_strengths = np.array(peak_strengths)
    return get_integral_state_map(peaks_filtered, peak_strengths, integrals.shape[1])
