# Generate and plot EEG

import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from IPython.display import display, clear_output
import scipy
from scipy import stats
import pandas as pd
import mne

from eegsim import EEGGen

# from resample.bootstrap import bootstrap
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LinearRegression

cell_plot_width = 40
fig_height = 10

def generate_eeg_events(gen,
                        n_events=1,
                        duration=1,  # seconds
                        random_state=None,
                       ):
    eeg = list()
    for ev in range(n_events):
        rand_state = random_state if random_state is None else random_state + ev
        eeg.append(gen.Generate(duration, random_state=rand_state).reshape(1, 1, -1))
    return np.concatenate(eeg, axis=0)

# Plot the time-domain traces.
def plot_time(time, eeg, fig=None, display_notebook=False):
    n_events = eeg.shape[0]
    n_cols = min(n_events, 2)
    n_rows = n_events // n_cols + ((n_events % n_cols) == 1)
    if fig is None:
        fig = plt.figure(figsize=(cell_plot_width, fig_height*n_rows))
    plt.subplot(n_rows, n_cols, 1)
    plt.suptitle('EEG Traces over Time', fontsize=45)
    for ev in range(n_events):
        plt.subplot(n_rows, n_cols, ev + 1)
        plt.plot(time, eeg[ev, 0])
        plt.xticks(fontsize=35)
        plt.yticks(fontsize=35)
#         if ev % n_cols == 0:
        plt.ylabel('Voltage (uV)', fontsize=40)
#         if (np.ceil(ev / n_cols + 0.1) >= n_rows) or n_events <= n_cols:
        plt.xlabel('Time (s)', fontsize=40)
    if display_notebook:
#         import pdb; pdb.set_trace()
#         plt.plot()
        display(plt.gcf())
#         display(fig)

# Plot the PSD averaged across traces
def plot_psd(eeg, exclude_line_noise=True, fig=None):
    if mne.__version__ == '0.18.0':
        psd, freqs = mne.time_frequency.psd_multitaper(eeg, fmin=3, fmax=200, picks='all')
        psd_db = 10*np.log10(psd).mean(axis=0).reshape(-1)
    else:
        psd = eeg.compute_psd(fmin=3, fmax=200, picks='all')
        psd_db = 10*np.log10(psd._data).mean(axis=0).reshape(-1)
        freqs = psd._freqs
        
    if fig is None:
        fig = plt.figure(figsize=(cell_plot_width, fig_height*n_rows))
    plt.suptitle('Power Spectral Density', fontsize=45)
    plt.semilogx(freqs, psd_db, label='PSD')
    
    # plot linear fit in log-log space
    if exclude_line_noise:  # fit regression without common line noise bands to reduce bias
        mask = (freqs < 58) | (freqs > 62)
        mask = ((freqs < 118) | (freqs > 122)) & mask
        mask = ((freqs < 178) | (freqs > 182)) & mask
    else: mask = freqs > -1
    res = stats.linregress(np.log10(freqs[mask]), psd_db[mask])
    print(res)
    psd_fit = res.intercept + res.slope * np.log10(freqs)
    residuals = psd_db[mask] - psd_fit[mask]
    std = np.std(residuals, ddof=1)
    plt.plot(freqs, psd_fit, label=f'Reg: r={res.rvalue:0.2}, p={res.pvalue:0.3}', linewidth=3)
    df = pd.DataFrame({'freq': freqs[mask], 'psd': psd_db[mask]})
#     sns.regplot(data=df, x='freq', y='psd', logx=True, marker='')#, x_ci='sd')
#     A = np.concatenate([np.log10(freqs[mask]).reshape(-1, 1), psd_db[mask].reshape(-1, 1)], axis=1)
#     boot_coef = bootstrap(sample=A, fn=fitreg, size=50)
#     conf = 0.95
#     import pdb; pdb.set_trace()
    
    if exclude_line_noise:
        ax = fig.get_axes()[0]
        f = 60
        get_line_noise = lambda f: np.interp(f, freqs, psd_db) - (res.intercept + res.slope * np.log10(f))
        line_noise60 = get_line_noise(f)#np.linspace(f - 0.5, f + 0.5, 100)).mean()
        print('dB power at 60 Hz:', res.intercept + res.slope * np.log10(f))
        print('dB power at 120 Hz:', res.intercept + res.slope * np.log10(120))
        print('dB power at 180 Hz:', res.intercept + res.slope * np.log10(180))
        
        plt.text(0.1, 0.1, f'Line noise ({f} Hz): {line_noise60:0.3} dB', transform=ax.transAxes, fontsize=40)
    
    plt.legend(fontsize=30)
    plt.xticks(fontsize=35)
    plt.yticks(fontsize=35)
    plt.xlabel('Frequency (Hz)', fontsize=40)
    plt.ylabel('Power (dB)', fontsize=40)
    return fig


def plot_eeg_signal(gen, 
                    duration=1,  # seconds
                    n_events=1, 
                    sample_rate=1000,
                    include_time=True,
                    include_psd=True,
                    exclude_line_noise=False,
                    cell_plot_width=40, 
                    fig_height=10,
                    display_notebook=False
                   ):
    eeg = generate_eeg_events(gen, n_events=n_events, duration=duration)

    time = gen.time_coords - duration / 2.0
    if include_time:
        n_events = eeg.shape[0]
        n_cols = min(n_events, 2)
        n_rows = n_events // n_cols + ((n_events % n_cols) == 1)
        fig = plt.figure(figsize=(cell_plot_width, fig_height * n_rows))
        plot_time(time, eeg, fig=fig, 
                  display_notebook=display_notebook)

    if include_psd:
        chans = ['CH1']
        info = mne.create_info(ch_names=chans,
                               ch_types=['misc'] * len(chans), 
                               sfreq=sample_rate)
        eeg_mne = mne.EpochsArray(data=eeg, info=info)
        # eeg_mne.plot(picks='all', n_epochs=3)
        fig = plt.figure(figsize=(cell_plot_width, fig_height))
        _ = plot_psd(eeg_mne, exclude_line_noise=exclude_line_noise, fig=fig)

def display_quiz_eeg(high_line_noise=False, sample_rate=1000, eeg_scale=7, duration=4):
    gen = EEGGen(sampling_rate=sample_rate)

    pink_scale = 0.5
    pink_exponent = 0.51  # 0.51 from Linkenkaer-Hansen et al. 2001, J. Neurosci.
    gen.EnablePinkNoise(amp=pink_scale * eeg_scale, exponent=pink_exponent)

    # calibration of dB power for pink noise amplitude of 0.5, pink noise 
    # exponent of 0.51 without line noise components 
    pow_dB60 = 14.838
    pow_dB120 = 13.2890
    pow_dB180 = 12.383

    # line noise components
    if high_line_noise:  # 5 to 15 dB of line noise
        noise_db = np.random.rand() * 10 + 15
    else:  # 0 to 2 dB of line noise
        noise_db = np.random.rand() * 1.5
    osc_freq = 60  # Hz
    # find oscillatory amplitude of 1 corresponds to 40 dB on PSD...
    osc_amplitude_scale = (10**(noise_db / 20) - 1) * (10**(pow_dB60 / 20)) / 100
#     osc_amplitude_scale = 0.07
    osc_offset = 0.0
    cycles = osc_freq * duration
    gen.AddWave(freq=osc_freq, amp=osc_amplitude_scale * eeg_scale, start=osc_offset, reps=cycles)

#     osc_freq = 120  # Hz
#     osc_amplitude_scale = 0.05
#     osc_offset = 0.0
#     cycles = osc_freq * duration
#     gen.AddWave(freq=osc_freq, amp=osc_amplitude_scale * eeg_scale, start=osc_offset, reps=cycles)

    plot_eeg_signal(gen, duration=duration, n_events=1, exclude_line_noise=False, include_psd=False, display_notebook=True)

def discrimination_quiz(func1, func2, prompt, num_questions=40, answer_delay=1, min_score=0.8, display_question_number=True):
    '''
    boolean_quiz
    Quiz a user with 2 stimuli to discriminate.
    Functions func1() or func2() generate and display stimuli.
    Returns quiz proportion correct, responses, and answers.
    '''
    answers = list()
    responses = list()
    for i in range(num_questions):
        if display_question_number:
            print(f'Question {i+1}:')
        answers.append(np.random.rand() > 0.5)
        
        if answers[-1]: func1()
        else: func2()
        
        # get response
        resp = input(prompt)
        while resp not in ['y', 'Y', 'n', 'N']:
            print('Invalid choice')
            resp = input(prompt)
        resp = resp in ['y', 'Y']
        responses.append(resp)
        if resp == answers[-1]: print('Correct!')
        else: print('Incorrect.')
        sleep(answer_delay)
        clear_output()

    results = np.array(responses) == np.array(answers)
    score = results.mean()
    print(f'You got {score * 100:0.1f}% ({results.sum()} / {len(results)}) correct.')
    if score < min_score:
        print(f'Please take the test again until you achieve at least {100*min_score:0.1f}% correct.')
    else:
        print("Congratulations! You've passed the discrimination quiz!")
    return score, responses, answers