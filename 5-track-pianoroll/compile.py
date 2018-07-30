import numpy as np

print('[*] loading...')
proc_list = np.load('segments.npy')
print('[*] processing...')
num_item = len(proc_list)
print(num_item)
compiled_list = []
for lidx in range(num_item):
    multi_track = proc_list[lidx]
    pianorolls = []

    for tracks in multi_track.tracks:
        pianorolls.append(tracks.pianoroll[:, :, np.newaxis])

    pianoroll_compiled = np.reshape(np.concatenate(pianorolls, axis=2)[:, 24:108, :], (8, 48, 84, 5))
    pianoroll_compiled  = pianoroll_compiled[np.newaxis, :] > 0
    compiled_list.append(pianoroll_compiled.astype(bool))

final = np.concatenate(compiled_list, axis=0)
print(final.shape)
print('[*] saving...')
np.save('x_lpd_5_phr.npy', final)
print('Done!!')