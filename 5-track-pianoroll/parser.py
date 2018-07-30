import numpy as np
import os
from pypianoroll import Multitrack, Track
import json
import pickle

family_name=[
    'drum',
    'bass',
    'guitar',
    'string',
    'piano',
]

family_thres = [
    (2, 24), # drum
    (1, 96), # bass
    (2, 156), # guitar
    (2, 156), # string,
    (2, 156), # piano
]


def findall_endswith(root):
    """Traverse `root` recursively and yield all files ending with `postfix`"""
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if filename.endswith('.npz'):
                yield os.path.join(dirpath, filename)

def check_which_family(track):
    is_piano = lambda program, is_drum:  not is_drum and ((program >= 0 and program <= 7)
                                or (program >= 16 and program <= 23))
    is_guitar = lambda program: program >= 24 and program <= 31
    is_bass = lambda program: program >= 32 and program <= 39
    is_string = lambda program: program >=40  and program <= 51

    # drum, bass, guitar, string, piano
    is_instr_act = lambda program, is_drum: np.array([is_drum, is_bass(program), is_guitar(program),
                                          is_string(program), is_piano(program, is_drum)])

    instr_act = is_instr_act(track.program, track.is_drum)
    return instr_act

def check_instr_act(multitrack):
    instr_act_all = np.zeros(5)
    for track in multitrack.tracks:
        instr_act = check_which_family(track)
        instr_act_all += instr_act
    instr_act_cnt = sum(instr_act_all > 0)
    return  instr_act_all, instr_act_cnt

def segment_quality(pianoroll, thres_pitch, thres_beats):
    pitch_sum = sum(np.sum(pianoroll, axis=0) > 0)
    beat_sum = sum(np.sum(pianoroll, axis=1) > 0)
    score = pitch_sum + beat_sum
    return (pitch_sum >= thres_pitch) and (beat_sum >= thres_beats), (pitch_sum, beat_sum)

def proc_instr_intersection_list(npz_list):
    cnt_ok = 0
    list_ok = []
    thres_instr_num = 5
    for nidx in range(len(npz_list)): #len(npz_list)
        if nidx % 500 is 0:
            print(nidx, '-', cnt_ok)
        npz_file = npz_list[nidx]
        multitrack = Multitrack(npz_file)

        if len(multitrack.tracks) < 5:
            continue

        instr_act_all, instr_act_cnt = check_instr_act(multitrack)

        if instr_act_cnt != 5:
            continue

        list_ok.append(npz_file)
        cnt_ok += 1

    print(cnt_ok)
    return list_ok


if __name__ == '__main__':
    # root = 'lpd_cleansed'
    # npz_list = list(findall_endswith(root))

    # with open('npz_list.pickle', 'wb') as f:
    #     pickle.dump(npz_list, f, protocol=pickle.HIGHEST_PROTOCOL)
    # with open('npz_list.pickle', 'rb') as f:
    #     npz_list = pickle.load(f)

    # list_ok = proc_instr_intersection_list(npz_list)
    # with open('list_ok.pickle', 'wb') as f:
    #     pickle.dump(list_ok, f, protocol=pickle.HIGHEST_PROTOCOL)
    with open('list_ok.pickle', 'rb') as f:
        list_ok = pickle.load(f)



    num_consecutive_bar = 8
    resol = 96
    down_sample = 2
    cnt_totall_segments = 0
    cnt_augmented = 0
    ok_segment_list = []
    hop_size = (num_consecutive_bar / 4)

    num_list_ok = len(list_ok)
    for oid in range(len(list_ok)):
        print('==', oid, '/', num_list_ok,'===============')
        npz_ok = list_ok[oid]
        multitrack = Multitrack(npz_ok)
        downbeat = multitrack.downbeat

        num_bar = len(downbeat) // resol
        hop_iter = 0

        song_ok_segments = []
        for bidx in range(num_bar-num_consecutive_bar):
            if hop_iter > 0:
                hop_iter -= 1
                continue


            st = bidx * resol
            ed = st + num_consecutive_bar * resol

            best_instr = [None] * 5
            best_score = [-1] * 5
            second_act = [False] * 5
            second_instr = [None] * 5
            is_all_ok = [False] * 5
            for tidx, track in enumerate(multitrack.tracks):
            #     track[st:ed].plot()
                tmp_map = check_which_family(track)
                in_family = np.where(tmp_map)[0]

                if not len(in_family):
                    continue
                family = in_family[0]

                tmp_pianoroll = track[st:ed:down_sample].pianoroll
                is_ok, score = segment_quality(tmp_pianoroll, family_thres[family][0], family_thres[family][1])

                if is_ok and sum(score) > best_score[family]:
                    track.name = family_name[family]
                    best_instr[family] = track[st:ed:down_sample]
                    best_score[family] = sum(score)
                    is_all_ok[family] = True

            if sum(is_all_ok) == 5:
    #             print(bidx)
                hop_iter = np.random.randint(0, 1) + hop_size
                song_ok_segments.append(Multitrack(tracks=best_instr,
                                    downbeat=list(range(0, 383, 48)), beat_resolution=12))

        cnt_ok_segment = len(song_ok_segments)
        if cnt_ok_segment > 6:
            seed = (6, cnt_ok_segment//2)
            if cnt_ok_segment > 11:
                seed = (11, cnt_ok_segment//3)
            if cnt_ok_segment > 15:
                seed = (15, cnt_ok_segment//4)

            rand_idx = np.random.permutation(cnt_ok_segment)[:max(seed)]
            song_ok_segments = [song_ok_segments[ridx] for ridx in rand_idx]
            ok_segment_list.extend(song_ok_segments)
            cnt_ok_segment = len(rand_idx)
        else:
            ok_segment_list.extend(song_ok_segments)

        cnt_totall_segments += len(song_ok_segments)
        print('cur:%d | acc:%d'%(cnt_ok_segment, cnt_totall_segments))

    print('---')
    print(cnt_totall_segments)
    print(len(ok_segment_list))
    np.save('segments.npy', ok_segment_list)