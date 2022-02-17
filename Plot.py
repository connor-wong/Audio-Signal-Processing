import io
import pickle
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import AudioProcess
import PyOctaveBand
from PyQt5 import QtCore


# Function to plot audio waveform
def plot_waveform(signal, sr, audioName, minFreq, maxFreq, source, receiver):
    def onclick_select(event):
        if not event.inaxes: return
        inx = list(fig.axes).index(event.inaxes)
        buf = io.BytesIO()
        pickle.dump(fig, buf)
        buf.seek(0)

        newFig = pickle.load(buf)

        for i, ax in enumerate(newFig.axes):
            if i != inx:
                newFig.delaxes(ax)
            else:
                axes = ax

        axes.change_geometry(1, 1, 1)
        newFig.tight_layout(rect=[0.1, 0.1, 0.9, 0.95])
        newFig.show()

    if (len(signal.shape) > 1):  # Stereo audio format
        # Full spectrum
        f_source, p_source, f_receiver, p_receiver = AudioProcess.stereo_spectrum(
            signal, sr)

        # One third octave
        # Source
        if source:
            spl_source, freq_source = PyOctaveBand.octavefilter(
                signal[1],
                sr,
                fraction=3,
                limits=[20, 25000],
                show=False,
                sigbands=False)
            spl_source = np.asanyarray(spl_source) + 48
            freq_source = PyOctaveBand.normalizedfreq(
                fraction=3)[2:len(spl_source) + 2]

        # Receiver
        if receiver:
            spl_receiver, freq_receiver = PyOctaveBand.octavefilter(
                signal[0],
                sr,
                fraction=3,
                limits=[20, 25000],
                show=False,
                sigbands=False)
            spl_receiver = np.asanyarray(spl_receiver) + 48
            freq_receiver = PyOctaveBand.normalizedfreq(
                fraction=3)[2:len(spl_receiver) + 2]

        # Plot figure
        fig = plt.figure(audioName, figsize=(18, 10))
        plt.suptitle(audioName, fontsize=16)

        if source and not receiver:
            # Raw Waveform
            ax1 = plt.subplot(3, 1, 1)
            librosa.display.waveplot(signal[1], sr=sr, alpha=0.5)
            plt.title("Source [Raw Waveform]")
            plt.xlabel("Time")
            plt.ylabel("Sound Amplitude")

            # Full Spectrum
            ax2 = plt.subplot(3, 1, 2)
            plt.title("Source [Full Spectrum]")
            plt.semilogx(f_source, p_source, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # One Third Octave
            ax3 = plt.subplot(3, 1, 3)
            plt.title("Source [1/3 Octave]")
            plt.semilogx(freq_source, spl_source, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

        if receiver and not source:
            # Raw Waveform
            ax1 = plt.subplot(3, 1, 1)
            librosa.display.waveplot(signal[0], sr=sr, alpha=0.5)
            plt.title("Receiver [Raw Waveform]")
            plt.xlabel("Time")
            plt.ylabel("Sound Amplitude")

            # Full Spectrum
            ax2 = plt.subplot(3, 1, 2)
            plt.title("Receiver [Full Spectrum]")
            plt.semilogx(f_receiver, p_receiver, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # One Third Octave
            ax3 = plt.subplot(3, 1, 3)
            plt.title("Receiver [1/3 Octave]")
            plt.semilogx(freq_receiver, spl_receiver, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

        if source and receiver:
            # Raw Waveform
            ax1 = plt.subplot(3, 2, 1)
            librosa.display.waveplot(signal[1], sr=sr, alpha=0.5)
            plt.title("Source [Raw Waveform]")
            plt.xlabel("Time")
            plt.ylabel("Sound Amplitude")

            ax2 = plt.subplot(3, 2, 2)
            librosa.display.waveplot(signal[0], sr=sr, alpha=0.5)
            plt.title("Receiver [Raw Waveform]")
            plt.xlabel("Time")
            plt.ylabel("Sound Amplitude")

            # Full Spectrum
            ax3 = plt.subplot(3, 2, 3)
            plt.title("Source [Full Spectrum]")
            plt.semilogx(f_source, p_source, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            ax4 = plt.subplot(3, 2, 4)
            plt.title("Receiver [Full Spectrum]")
            plt.semilogx(f_receiver, p_receiver, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # One Third Octave
            ax5 = plt.subplot(3, 2, 5)
            plt.title("Source [1/3 Octave]")
            plt.semilogx(freq_source, spl_source, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            ax6 = plt.subplot(3, 2, 6)
            plt.title("Receiver [1/3 Octave]")
            plt.semilogx(freq_receiver, spl_receiver, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

    else:  # Mono audio format
        # Full spectrum
        f, p = AudioProcess.mono_spectrum(signal, sr)

        # One third octave
        spl, freq = PyOctaveBand.octavefilter(signal,
                                              sr,
                                              fraction=3,
                                              limits=[20, 25000],
                                              show=False,
                                              sigbands=False)

        spl = np.asanyarray(spl) + 48
        freq = PyOctaveBand.normalizedfreq(fraction=3)[2:len(spl) + 2]

        # Plot figure
        fig = plt.figure(audioName, figsize=(18, 10))
        plt.suptitle(audioName, fontsize=16)
        # Raw Waveform
        ax1 = plt.subplot(3, 1, 1)
        librosa.display.waveplot(signal, sr=sr, alpha=0.5)
        plt.title("Raw Waveform")
        plt.xlabel("Time")
        plt.ylabel("Sound Amplitude")

        # Full Spectrum
        ax2 = plt.subplot(3, 1, 2)
        plt.title("Full Spectrum")
        plt.semilogx(f, p, 'b')
        plt.grid(which='major')
        plt.grid(which='minor', linestyle=':')
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("SPL [dB/20u]")
        if maxFreq != "":
            plt.xlim([int(minFreq), int(maxFreq)])

        # One Third Octave
        ax3 = plt.subplot(3, 1, 3)
        plt.title("1/3 Octave")
        plt.semilogx(freq, spl, 'b')
        plt.grid(which='major')
        plt.grid(which='minor', linestyle=':')
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("SPL [dB/20u]")
        if maxFreq != "":
            plt.xlim([int(minFreq), int(maxFreq)])

    plt.tight_layout()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    fig.canvas.mpl_connect("button_press_event", onclick_select)
    plt.show()


def plot_compare(pathList, minFreq, maxFreq, source, receiver):
    def onclick_select(event):
        if not event.inaxes: return
        inx = list(fig.axes).index(event.inaxes)
        buf = io.BytesIO()
        pickle.dump(fig, buf)
        buf.seek(0)

        newFig = pickle.load(buf)

        for i, ax in enumerate(newFig.axes):
            if i != inx:
                newFig.delaxes(ax)
            else:
                axes = ax

        axes.change_geometry(1, 1, 1)
        newFig.tight_layout(rect=[0.1, 0.1, 0.9, 0.95])
        newFig.show()

    fig = plt.figure(figsize=(18, 10))

    for path in pathList:
        url = QtCore.QUrl.fromLocalFile(path)
        signal, sr = librosa.load(path, sr=None, mono=False)  #Load audio file

        if (len(signal.shape) > 1):  # Stereo audio format
            # Full spectrum
            f_source, p_source, f_receiver, p_receiver = AudioProcess.stereo_spectrum(
                signal, sr)

            # One third octave
            # Source
            if source:
                spl_source, freq_source = PyOctaveBand.octavefilter(
                    signal[1],
                    sr,
                    fraction=3,
                    limits=[20, 25000],
                    show=False,
                    sigbands=False)
                spl_source = np.asanyarray(spl_source) + 48
                freq_source = PyOctaveBand.normalizedfreq(
                    fraction=3)[2:len(spl_source) + 2]

            # Receiver
            if receiver:
                spl_receiver, freq_receiver = PyOctaveBand.octavefilter(
                    signal[0],
                    sr,
                    fraction=3,
                    limits=[20, 25000],
                    show=False,
                    sigbands=False)
                spl_receiver = np.asanyarray(spl_receiver) + 48
                freq_receiver = PyOctaveBand.normalizedfreq(
                    fraction=3)[2:len(spl_receiver) + 2]

            # Plot
            if receiver and not source:
                # Full Spectrum
                ax1 = plt.subplot(2, 1, 1)
                plt.title("Receiver [Full Spectrum]")
                plt.semilogx(f_receiver, p_receiver, label=url.fileName())
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                # One Third Octave
                ax2 = plt.subplot(2, 1, 2)
                plt.title("Receiver [1/3 Octave]")
                plt.semilogx(freq_receiver, spl_receiver, label=url.fileName())
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

            if source and not receiver:
                # Full Spectrum
                ax1 = plt.subplot(2, 1, 1)
                plt.title("Source [Full Spectrum]")
                plt.semilogx(f_source, p_source, label=url.fileName())
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                # One Third Octave
                ax2 = plt.subplot(2, 1, 2)
                plt.title("Source [1/3 Octave]")
                plt.semilogx(freq_source, spl_source, label=url.fileName())
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

            if source and receiver:
                # Full Spectrum
                ax1 = plt.subplot(2, 2, 1)
                plt.title("Source [Full Spectrum]")
                plt.semilogx(f_source, p_source, label=url.fileName())
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                ax2 = plt.subplot(2, 2, 2)
                plt.title("Receiver [Full Spectrum]")
                plt.semilogx(f_receiver, p_receiver, label=url.fileName())
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                # One Third Octave
                ax3 = plt.subplot(2, 2, 3)
                plt.title("Source [1/3 Octave]")
                plt.semilogx(freq_source, spl_source, label=url.fileName())
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                ax4 = plt.subplot(2, 2, 4)
                plt.title("Receiver [1/3 Octave]")
                plt.semilogx(freq_receiver, spl_receiver, label=url.fileName())
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

        else:  # Mono audio format
            # Full spectrum
            f, p = AudioProcess.mono_spectrum(signal, sr)

            # One third octave
            spl, freq = PyOctaveBand.octavefilter(signal,
                                                  sr,
                                                  fraction=3,
                                                  limits=[20, 25000],
                                                  show=False,
                                                  sigbands=False)

            spl = np.asanyarray(spl) + 48
            freq = PyOctaveBand.normalizedfreq(fraction=3)[2:len(spl) + 2]

            # Plot
            # Full Spectrum
            ax1 = plt.subplot(2, 1, 1)
            plt.title("Full Spectrum")
            plt.semilogx(f, p, label=url.fileName())
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            plt.legend(loc='best')
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # One Third Octave
            ax2 = plt.subplot(2, 1, 2)
            plt.title("1/3 Octave")
            plt.semilogx(freq, spl, label=url.fileName())
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            plt.legend(loc='best')
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

    plt.tight_layout()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    fig.canvas.mpl_connect("button_press_event", onclick_select)

    plt.show()


def plot_average(pathList, minFreq, maxFreq, source, receiver, sd):
    def onclick_select(event):
        if not event.inaxes: return
        inx = list(fig.axes).index(event.inaxes)
        buf = io.BytesIO()
        pickle.dump(fig, buf)
        buf.seek(0)

        newFig = pickle.load(buf)

        for i, ax in enumerate(newFig.axes):
            if i != inx:
                newFig.delaxes(ax)
            else:
                axes = ax

        axes.change_geometry(1, 1, 1)
        newFig.tight_layout(rect=[0.1, 0.1, 0.9, 0.95])
        newFig.show()

    mono_count, stero_count, total_spl_source, total_spl_receiver, total_p_source, total_p_receiver, total_spl, total_p = 0, 0, 0, 0, 0, 0, 0, 0
    num_figure = 3
    global f_source, f_receiver, freq_source, freq_receiver, f, freq
    global mono_status, stereo_status

    mono_status, stereo_status = False, False
    sd_source_array, sd_receiver_array, sd_array = [], [], []

    if sd:
        num_figure = 3
    else:
        num_figure = 2

    for path in pathList:
        signal, sr = librosa.load(path, sr=None, mono=False)  #Load audio file

        if (len(signal.shape) > 1):  # Stereo audio format
            stereo_status = True
            # Full spectrum
            f_source, p_source, f_receiver, p_receiver = AudioProcess.stereo_spectrum(
                signal, sr)

            # One third octave
            # Source
            if source:
                spl_source, freq_source = PyOctaveBand.octavefilter(
                    signal[1],
                    sr,
                    fraction=3,
                    limits=[20, 25000],
                    show=False,
                    sigbands=False)
                spl_source = np.asanyarray(spl_source) + 48
                freq_source = PyOctaveBand.normalizedfreq(
                    fraction=3)[2:len(spl_source) + 2]
                sd_source_array.append(spl_source)

                total_spl_source += spl_source
                total_p_source += p_source

            # Receiver
            if receiver:
                spl_receiver, freq_receiver = PyOctaveBand.octavefilter(
                    signal[0],
                    sr,
                    fraction=3,
                    limits=[20, 25000],
                    show=False,
                    sigbands=False)
                spl_receiver = np.asanyarray(spl_receiver) + 48
                freq_receiver = PyOctaveBand.normalizedfreq(
                    fraction=3)[2:len(spl_receiver) + 2]
                sd_receiver_array.append(spl_receiver)

                total_spl_receiver += spl_receiver
                total_p_receiver += p_receiver

            # Total
            stero_count += 1

        else:  # Mono audio format
            mono_status = True
            # Full spectrum
            f, p = AudioProcess.mono_spectrum(signal, sr)

            # One third octave
            spl, freq = PyOctaveBand.octavefilter(signal,
                                                  sr,
                                                  fraction=3,
                                                  limits=[20, 25000],
                                                  show=False,
                                                  sigbands=False)

            spl = np.asanyarray(spl) + 48
            freq = PyOctaveBand.normalizedfreq(fraction=3)[2:len(spl) + 2]
            sd_array.append(spl)

            # Total
            total_spl += spl
            total_p += p
            mono_count += 1

    if stereo_status:
        # Plot figure
        fig = plt.figure("Average Stereo Plot", figsize=(18, 10))
        plt.suptitle("Average Stereo Plot", fontsize=16)

        if receiver and not source:
            # Full Spectrum
            ax1 = plt.subplot(num_figure, 1, 1)
            plt.title("Receiver [Average Full Spectrum]")
            plt.semilogx(f_receiver, total_p_receiver / stero_count, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # One Third Octave
            ax2 = plt.subplot(num_figure, 1, 2)
            plt.title("Receiver [Average 1/3 Octave]")
            plt.semilogx(freq_receiver, total_spl_receiver / stero_count, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # Standard Deviation
            if sd:
                ax3 = plt.subplot(num_figure, 1, 3)
                plt.title("Receiver [Standard Deviation]")
                plt.errorbar(freq_receiver,
                             total_spl_receiver / stero_count,
                             yerr=np.std(sd_receiver_array, axis=0).tolist(),
                             capsize=5,
                             color='b')
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xscale("log")
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

        if source and not receiver:
            # Full Spectrum
            ax1 = plt.subplot(num_figure, 1, 1)
            plt.title("Source [Average Full Spectrum]")
            plt.semilogx(f_source, total_p_source / stero_count, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # One Third Octave
            ax2 = plt.subplot(num_figure, 1, 2)
            plt.title("Source [Average 1/3 Octave]")
            plt.semilogx(freq_source, total_spl_source / stero_count, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # Standard Deviation
            if sd:
                ax3 = plt.subplot(num_figure, 1, 3)
                plt.title("Source [Standard Deviation]")
                plt.errorbar(freq_source,
                             total_spl_source / stero_count,
                             yerr=np.std(sd_source_array, axis=0).tolist(),
                             capsize=5,
                             color='b')
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xscale("log")
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

        if source and receiver:
            # Full Spectrum
            ax1 = plt.subplot(num_figure, 2, 1)
            plt.title("Source [Average Full Spectrum]")
            plt.semilogx(f_source, total_p_source / stero_count, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            ax2 = plt.subplot(num_figure, 2, 2)
            plt.title("Receiver [Average Full Spectrum]")
            plt.semilogx(f_receiver, total_p_receiver / stero_count, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # One Third Octave
            ax3 = plt.subplot(num_figure, 2, 3)
            plt.title("Source [Average 1/3 Octave]")
            plt.semilogx(freq_source, total_spl_source / stero_count, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            ax4 = plt.subplot(num_figure, 2, 4)
            plt.title("Receiver [Average 1/3 Octave]")
            plt.semilogx(freq_receiver, total_spl_receiver / stero_count, 'b')
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            if sd:
                # Standard Deviation
                ax5 = plt.subplot(num_figure, 2, 5)
                plt.title("Source [Standard Deviation]")
                plt.errorbar(freq_source,
                             total_spl_source / stero_count,
                             yerr=np.std(sd_source_array, axis=0).tolist(),
                             capsize=5,
                             color='b')
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xscale("log")
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                ax6 = plt.subplot(num_figure, 2, 6)
                plt.title("Receiver [Standard Deviation]")
                plt.errorbar(freq_receiver,
                             total_spl_receiver / stero_count,
                             yerr=np.std(sd_receiver_array, axis=0).tolist(),
                             capsize=5,
                             color='b')
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xscale("log")
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

    else:
        pass

    if mono_status:
        # Plot figure
        fig = plt.figure("Average Mono Plot", figsize=(18, 10))
        plt.suptitle("Average Mono Plot", fontsize=16)

        # Full Spectrum
        ax1 = plt.subplot(num_figure, 1, 1)
        plt.title("Average Full Spectrum")
        plt.semilogx(f, total_p / mono_count, 'b')
        plt.grid(which='major')
        plt.grid(which='minor', linestyle=':')
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("SPL [dB/20u]")
        if maxFreq != "":
            plt.xlim([int(minFreq), int(maxFreq)])

        # One Third Octave
        ax2 = plt.subplot(num_figure, 1, 2)
        plt.title("Average 1/3 Octave")
        plt.semilogx(freq, total_spl / mono_count, 'b')
        plt.grid(which='major')
        plt.grid(which='minor', linestyle=':')
        plt.xlabel("Frequency [Hz]")
        plt.ylabel("SPL [dB/20u]")
        if maxFreq != "":
            plt.xlim([int(minFreq), int(maxFreq)])

        # Standard Deviation
        if sd:
            ax3 = plt.subplot(num_figure, 1, 3)
            plt.title("Receiver [Standard Deviation]")
            plt.errorbar(
                freq,
                total_spl / mono_count,
                yerr=np.std(sd_receiver_array, axis=0).tolist(),
                capsize=5,
                color='b',
            )
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xscale("log")
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

    plt.tight_layout()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    fig.canvas.mpl_connect("button_press_event", onclick_select)
    plt.show()


def plot_compare_average(pathListArray, minFreq, maxFreq, colourList,
                         legendList, source, receiver, sd):
    def onclick_select(event):
        if not event.inaxes: return
        inx = list(fig.axes).index(event.inaxes)
        buf = io.BytesIO()
        pickle.dump(fig, buf)
        buf.seek(0)

        newFig = pickle.load(buf)

        for i, ax in enumerate(newFig.axes):
            if i != inx:
                newFig.delaxes(ax)
            else:
                axes = ax

        axes.change_geometry(1, 1, 1)
        newFig.tight_layout(rect=[0.1, 0.1, 0.9, 0.95])
        newFig.show()

    num_figure = 3

    if sd:
        num_figure = 3
    else:
        num_figure = 2

    for i, pathList in enumerate(pathListArray):
        mono_count, stero_count, total_spl_source, total_spl_receiver, total_p_source, total_p_receiver, total_spl, total_p = 0, 0, 0, 0, 0, 0, 0, 0
        global f_source, f_receiver, freq_source, freq_receiver, f, freq
        global mono_status, stereo_status

        mono_status, stereo_status = False, False
        sd_source_array, sd_receiver_array, sd_array = [], [], []

        for path in pathList:
            signal, sr = librosa.load(path, sr=None,
                                      mono=False)  #Load audio file

            if (len(signal.shape) > 1):  # Stereo audio format
                stereo_status = True
                # Full spectrum
                f_source, p_source, f_receiver, p_receiver = AudioProcess.stereo_spectrum(
                    signal, sr)

                # One third octave
                # Source
                if source:
                    spl_source, freq_source = PyOctaveBand.octavefilter(
                        signal[1],
                        sr,
                        fraction=3,
                        limits=[20, 25000],
                        show=False,
                        sigbands=False)
                    spl_source = np.asanyarray(spl_source) + 48
                    freq_source = PyOctaveBand.normalizedfreq(
                        fraction=3)[2:len(spl_source) + 2]

                    total_spl_source += spl_source
                    total_p_source += p_source
                    sd_source_array.append(spl_source)

                # Receiver
                if receiver:
                    spl_receiver, freq_receiver = PyOctaveBand.octavefilter(
                        signal[0],
                        sr,
                        fraction=3,
                        limits=[20, 25000],
                        show=False,
                        sigbands=False)
                    spl_receiver = np.asanyarray(spl_receiver) + 48
                    freq_receiver = PyOctaveBand.normalizedfreq(
                        fraction=3)[2:len(spl_receiver) + 2]

                    total_spl_receiver += spl_receiver
                    total_p_receiver += p_receiver
                    sd_receiver_array.append(spl_receiver)

                # Total
                stero_count += 1

            else:  # Mono audio format
                mono_status = True
                # Full spectrum
                f, p = AudioProcess.mono_spectrum(signal, sr)

                # One third octave
                spl, freq = PyOctaveBand.octavefilter(signal,
                                                      sr,
                                                      fraction=3,
                                                      limits=[20, 25000],
                                                      show=False,
                                                      sigbands=False)

                spl = np.asanyarray(spl) + 48
                freq = PyOctaveBand.normalizedfreq(fraction=3)[2:len(spl) + 2]
                sd_array.append(spl)

                # Total
                total_spl += spl
                total_p += p
                mono_count += 1

        if stereo_status:
            # Plot figure
            fig = plt.figure("Average Stereo Plot", figsize=(18, 10))
            plt.suptitle("Average Stereo Plot", fontsize=16)

            if receiver and not source:
                # Full Spectrum
                ax1 = plt.subplot(num_figure, 1, 1)
                plt.title("Receiver [Average Full Spectrum]")
                plt.semilogx(f_receiver,
                             total_p_receiver / stero_count,
                             colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                # One Third Octave
                ax2 = plt.subplot(num_figure, 1, 2)
                plt.title("Receiver [Average 1/3 Octave]")
                plt.semilogx(freq_receiver,
                             total_spl_receiver / stero_count,
                             colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                if sd:
                    # Standard Deviation
                    ax3 = plt.subplot(num_figure, 1, 3)
                    plt.title("Receiver [Standard Deviation]")
                    plt.errorbar(freq_receiver,
                                 total_spl_receiver / stero_count,
                                 yerr=np.std(sd_receiver_array,
                                             axis=0).tolist(),
                                 capsize=5,
                                 color=colourList[i],
                                 label=legendList[i])
                    plt.grid(which='major')
                    plt.grid(which='minor', linestyle=':')
                    plt.xscale("log")
                    plt.xlabel("Frequency [Hz]")
                    plt.ylabel("SPL [dB/20u]")
                    if maxFreq != "":
                        plt.xlim([int(minFreq), int(maxFreq)])

            if source and not receiver:
                # Full Spectrum
                ax1 = plt.subplot(num_figure, 1, 1)
                plt.title("Source [Average Full Spectrum]")
                plt.semilogx(f_source,
                             total_p_source / stero_count,
                             colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                # One Third Octave
                ax2 = plt.subplot(num_figure, 1, 2)
                plt.title("Source [Average 1/3 Octave]")
                plt.semilogx(freq_source,
                             total_spl_source / stero_count,
                             colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                if sd:
                    # Standard Deviation
                    ax3 = plt.subplot(num_figure, 1, 3)
                    plt.title("Source [Standard Deviation]")
                    plt.errorbar(freq_source,
                                 total_spl_source / stero_count,
                                 yerr=np.std(sd_source_array, axis=0).tolist(),
                                 capsize=5,
                                 color=colourList[i],
                                 label=legendList[i])
                    plt.grid(which='major')
                    plt.grid(which='minor', linestyle=':')
                    plt.xscale("log")
                    plt.xlabel("Frequency [Hz]")
                    plt.ylabel("SPL [dB/20u]")
                    if maxFreq != "":
                        plt.xlim([int(minFreq), int(maxFreq)])

            if source and receiver:
                # Full Spectrum
                ax1 = plt.subplot(num_figure, 2, 1)
                plt.title("Source [Average Full Spectrum]")
                plt.semilogx(f_source,
                             total_p_source / stero_count,
                             colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                ax2 = plt.subplot(num_figure, 2, 2)
                plt.title("Receiver [Average Full Spectrum]")
                plt.semilogx(f_receiver,
                             total_p_receiver / stero_count,
                             colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                # One Third Octave
                ax3 = plt.subplot(num_figure, 2, 3)
                plt.title("Source [Average 1/3 Octave]")
                plt.semilogx(freq_source,
                             total_spl_source / stero_count,
                             colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                ax4 = plt.subplot(num_figure, 2, 4)
                plt.title("Receiver [Average 1/3 Octave]")
                plt.semilogx(freq_receiver,
                             total_spl_receiver / stero_count,
                             colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                plt.legend(loc='best')
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

                if sd:
                    # Standard Deviation
                    ax5 = plt.subplot(num_figure, 2, 5)
                    plt.title("Source [Standard Deviation]")
                    plt.errorbar(freq_source,
                                 total_spl_source / stero_count,
                                 yerr=np.std(sd_source_array, axis=0).tolist(),
                                 capsize=5,
                                 color=colourList[i],
                                 label=legendList[i])
                    plt.grid(which='major')
                    plt.grid(which='minor', linestyle=':')
                    plt.xscale("log")
                    plt.xlabel("Frequency [Hz]")
                    plt.ylabel("SPL [dB/20u]")
                    if maxFreq != "":
                        plt.xlim([int(minFreq), int(maxFreq)])

                    ax6 = plt.subplot(num_figure, 2, 6)
                    plt.title("Receiver [Standard Deviation]")
                    plt.errorbar(freq_receiver,
                                 total_spl_receiver / stero_count,
                                 yerr=np.std(sd_receiver_array,
                                             axis=0).tolist(),
                                 capsize=5,
                                 color=colourList[i],
                                 label=legendList[i])
                    plt.grid(which='major')
                    plt.grid(which='minor', linestyle=':')
                    plt.xscale("log")
                    plt.xlabel("Frequency [Hz]")
                    plt.ylabel("SPL [dB/20u]")
                    if maxFreq != "":
                        plt.xlim([int(minFreq), int(maxFreq)])

        else:
            pass

        if mono_status:
            # Plot figure
            fig = plt.figure("Average Mono Plot", figsize=(18, 10))
            plt.suptitle("Average Mono Plot", fontsize=16)

            # Full Spectrum
            ax1 = plt.subplot(num_figure, 1, 1)
            plt.title("Average Full Spectrum")
            plt.semilogx(f,
                         total_p / mono_count,
                         colourList[i],
                         label=legendList[i])
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            plt.legend(loc='best')
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            # One Third Octave
            ax2 = plt.subplot(num_figure, 1, 2)
            plt.title("Average 1/3 Octave")
            plt.semilogx(freq,
                         total_spl / mono_count,
                         colourList[i],
                         label=legendList[i])
            plt.grid(which='major')
            plt.grid(which='minor', linestyle=':')
            plt.xlabel("Frequency [Hz]")
            plt.ylabel("SPL [dB/20u]")
            plt.legend(loc='best')
            if maxFreq != "":
                plt.xlim([int(minFreq), int(maxFreq)])

            if sd:
                # Standard Deviation
                ax5 = plt.subplot(num_figure, 1, 3)
                plt.title("Standard Deviation")
                plt.errorbar(freq_receiver,
                             total_spl / mono_count,
                             yerr=np.std(sd_array, axis=0).tolist(),
                             capsize=5,
                             color=colourList[i],
                             label=legendList[i])
                plt.grid(which='major')
                plt.grid(which='minor', linestyle=':')
                plt.xscale("log")
                plt.xlabel("Frequency [Hz]")
                plt.ylabel("SPL [dB/20u]")
                if maxFreq != "":
                    plt.xlim([int(minFreq), int(maxFreq)])

    plt.tight_layout()
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    fig.canvas.mpl_connect("button_press_event", onclick_select)
    plt.show()
