def calc_eye_size_state (features, filenames, sort_time_fn, SQUINT_THRESH, SMOOTH_WIN, EYE_SIZE_RANGE = 2000, PT_LENGTH = 54, ROW = 240, COL = 320, FS = 10):

    import numpy as np
    from scipy import io, optimize, integrate

    def curve_function(x, a, b, c, d, e, f):
        return a * x ** 5 + b * x ** 4 + c * x ** 3 + d * x ** 2 + e * x + f

    def find_zero_1der(x, find_peak = False):
        ans = []
        gradient = np.gradient(x)
        for i in range(len(x) - 1):
            if find_peak:
                if np.sign(gradient[i + 1]) < 0 and np.sign(gradient[i]) > 0:
                    ans.append(i)
            else:
                if np.sign(gradient[i + 1]) > 0 and np.sign(gradient[i]) < 0:
                    ans.append(i)
        return ans

    # sorting the images based on time
    filenames.sort(key = sort_time_fn)

    for i in range(len(filenames)):
        if i % 100 == 0:
            print('current subject: ' + str(i))

        # fitting the curves for eyelids
        upper_eye = np.array(features[filenames[i]].pts[:PT_LENGTH // 3]).reshape(-1, 2)
        lower_eye = np.array(features[filenames[i]].pts[PT_LENGTH // 3:PT_LENGTH // 3 * 2]).reshape(-1, 2)
        upper_popt, upper_pcov = optimize.curve_fit(curve_function, upper_eye[:, 0], upper_eye[:, 1])
        lower_popt, lower_pcov = optimize.curve_fit(curve_function, lower_eye[:, 0], lower_eye[:, 1])

        xaxes = np.arange(0, COL, 1/FS)
        upper = curve_function(xaxes, *upper_popt)
        lower = curve_function(xaxes, *lower_popt)

        valid = [ind for ind, x in enumerate(upper) if upper[ind] <= lower[ind]]
        xaxes = xaxes[valid]
        upper = upper[valid]
        lower = lower[valid]

        # finding the two eye corners (either points of intersection or points of 0 first derivatives)
        lower_zeros = find_zero_1der(lower)
        if lower_zeros:
            start, end = 0, len(xaxes)
            for zero in lower_zeros:
                if zero < len(xaxes) / 2: start = zero
                if zero > len(xaxes) / 2: end = zero
            xaxes = xaxes[start : end]
            upper = upper[start : end]
            lower = lower[start : end]

        # calculating area
        area = 0
        for j in range(len(xaxes) - 1):
            area += ((lower[j] + lower[j + 1]) / 2 - (upper[j] + upper[j + 1]) / 2) * (xaxes[j + 1] - xaxes[j])
        features[filenames[i]].set_area(area)

    # determine eye size state for each time point
    areas = np.array([time_pt.area for time_pt in list(features.values())])
    baseline = np.average(areas[areas > np.max(areas) - EYE_SIZE_RANGE])

    for filename in filenames:
        features[filename].set_eye_size_state(((features[filename].area - baseline) / baseline * 100) < SQUINT_THRESH)

    state_map = np.array([features[filename].eye_size_state for filename in filenames])

    # smoothing the state map
    for i in range(len(state_map)):
        for win in range(SMOOTH_WIN, 0):
            if state_map[i] != state_map[i - win] and state_map[i] != state_map[i + win]:
                state_map[i] = state_map[i - win]

    return state_map
