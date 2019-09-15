def pupil_processing(PUPIL_FILE, FS = 10, WINDOW_SIZE = 12, HAMPEL_PASSES = 3, MAD_MULTIPLIER = 12):
    import numpy as np
    import matplotlib.pyplot as plt

    def diff(first, second):
            second = set(second)
            return [item for item in first if item not in second]

    def hampel(data, window = 7, mad_multiplier = 4):
        length = len(list(data))
        half_window = int((window - 1) / 2)
        ans = []
        for i in range(half_window, length - half_window):
            median = np.median(data[i - half_window : i + half_window + 1])
            mad = np.median(abs(data[i - half_window : i + half_window + 1] - median))
            if data[i] > median + mad_multiplier * mad or data[i] < median - mad_multiplier * mad:
                ans.append(i)
        return ans

    def nan_helper(y):
        """Helper to handle indices and logical indices of NaNs.
        Input:
            - y, 1d numpy array with possible NaNs
        Output:
            - nans, logical indices of NaNs
            - index, a function, with signature indices= index(logical_indices),
              to convert logical indices of NaNs to 'equivalent' indices
        """
        nans = np.isnan(y)
        x = lambda z : z.nonzero()[0]
        y[nans] = np.interp(x(nans), x(~nans), y[~nans])
        return y

    # constants
    LEFT = 3
    RIGHT = 4

    # loading data
    dataset = np.loadtxt(PUPIL_FILE)

    data = [];
    loc_data = []
    for i in range(len(dataset)):
        data.append(max(dataset[i, LEFT] / 10, dataset[i, RIGHT] / 10));
        loc_data.append(dataset[i, 1:3]) # ********DEPENDS ON DATA FORMAT***********

    # ----------------------------------------preprocessing-----------------------------------------
    data_time = dataset[:, 0];
    data = np.array(data)
    loc_data = np.array(loc_data)

    for i in range(len(data)):
        if data[i] < 0 or np.isnan(data[i]):
            data[i] = np.nan;
            loc_data[i, :] = np.nan
            data_time[i] = np.nan;

    # hampel filtering
    for iter in range(HAMPEL_PASSES):
        data = nan_helper(data)
        data_time = nan_helper(data_time)
        loc_data[:, 0] = nan_helper(loc_data[:, 0])
        loc_data[:, 1] = nan_helper(loc_data[:, 1])

        outliers = hampel(data, mad_multiplier = MAD_MULTIPLIER)
        print("Hampel filter iteration " + str(iter) + ": detected " + str(len(outliers)) + " outliers.")
        for i in outliers:
            data[i] = np.nan
            loc_data[i, :] = np.nan
            data_time[i] = np.nan

    data = nan_helper(data)
    data_time = nan_helper(data_time)
    loc_data[:, 0] = nan_helper(loc_data[:, 0])
    loc_data[:, 1] = nan_helper(loc_data[:, 1])

    # upsampling to 10Hz
    timestamp = np.arange(data_time[0], data_time[-1], 1 / FS);
    timestep = timestamp - data_time[0];

    interpFunc = interp.interp1d(data_time, data, kind = 'linear');
    interp_data = interpFunc(timestamp);

    interp_loc_data = np.zeros((2, len(timestamp)))
    for i in range(loc_data.shape[1]):
        interpFunc = interp.interp1d(data_time, loc_data[:, i], kind = 'linear')
        interp_loc_data[i, :] = interpFunc(timestamp)

    valid = ~np.isnan(interp_data)
    interp_data = interp_data[valid]
    interp_loc_data = interp_loc_data[:, valid]
    timestamp = timestamp[valid]

    return np.concatenate((timestamp.reshape(1, -1), interp_data.reshape(1, -1), \
                           interp_loc_data), axis = 0)
