import numpy as np

def test_glitch(tod, detail=False):
    found_glitches = flags.get_glitch_flags(tod, signal=signal_name, overwrite=True).ranges
    true_glitches = tod.flags.true_glitches

    found_glitches_ranges2D = np.vstack([r.mask() for r in found_glitches])
    true_glitches_ranges2D = np.vstack(r.mask() for r in true_glitches)

    result = found_glitches_ranges2D*true_glitches_ranges2D

    false_sum = 0
    for det in range(tod.dets.count):
        false_count = 0
        r = found_glitches[det].ranges()

        for index in r:
            s = np.sum(found_glitches[det].mask()[index[0]:index[1]] * true_glitches[det].mask()[index[0]:index[1]])
            if s == 0:
                false_count = false_count + 1
                false_sum = false_sum + 1

        if detail == True:
            true = tod.flags.true_glitches[det]


            found = flags.get_glitch_flags(tod, signal=signal_name, overwrite=True).ranges[det]

            results = true.mask()*found.mask()
            print('det:', det)
            print('true glitches:%s %s' %(np.sum(true.mask()),true.ranges()))
            #print('\n')
            print('found ranges:%s %s' %(int(found.ranges().size/2),found.ranges()))
            #print('\n')
            print('found true glitches:', np.sum(results))
            print('found false ranges:', false_count)
            print('detection rate:', np.sum(results)/np.sum(true.mask()))
            print('true positive rate:', (int(found.ranges().size/2)-false_count)/int(found.ranges().size/2))
            print('\n')

    #print('false sum:', false_sum)
    #print('\n')

    true_sum = true_glitches_ranges2D.sum()
    found_sum = sum([mr.ranges().size/2 for mr in found_glitches])
    found_true_sum = result.sum()

    detection_rate = found_true_sum/true_sum

    if found_sum == 0:
        true_positive_rate = 0
    else:
        true_positive_rate = (found_sum - false_sum)/found_sum
    false_positive_rate = 1 - true_positive_rate

    return detection_rate, true_positive_rate, false_positive_rate


def get_noise(tod):
    if 'turnarounds' in tod.flags:
        tod.flags.move('turnarounds', None)

    flags.get_turnaround_flags(tod, merge=True, name='turnarounds');
    print( tod.flags.turnarounds )

    tmsk = tod.flags.turnarounds.mask()

    scan_rate = np.median( np.abs(np.diff(tod.boresight.az[~tmsk]))) / np.median(np.diff(tod.timestamps))
    print( 'The scan rate is {} deg / s'.format(round(np.degrees(scan_rate),3) ))

    turn = np.where( np.diff(tod.timestamps[tmsk]) > 0.005 )[0]
    turn_time = np.median( np.diff(tod.timestamps[tmsk][turn]))

    ffts, freqs = rfft(tod)
    tsamp = np.median(np.diff(tod.timestamps))
    norm_fact = (1.0/tsamp)*np.sum(np.abs(np.hanning(tod.samps.count))**2)
    fmsk = freqs > 10
    det_white_noise = 1e6*np.median(np.sqrt(np.abs(ffts[:,fmsk])**2/norm_fact),axis=1)

    return np.median(det_white_noise)


# def in_range(Points, Ranges):
#     results = np.zeros_like(Ranges[:,0])
#     for i, Range in enumerate(Ranges):
#         count = 0
#         for j, Point in enumerate(Points[count:]):
#             if Point in range(Range[0], Range[-1]):
#                 results[i] = 1
#                 count = count+1
#                 break
#             if j == len(Points) - 1:
#                 results[i] = 0
#     return results

# def true_positive_rate(results):
#     return (np.sum(results)/np.size(results))*100

# def false_positive_rate(results):
#     return (1-np.sum(results)/np.size(results))*100
