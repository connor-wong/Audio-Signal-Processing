import librosa
import numpy as np
import scipy as sp


# Fulll Spectrum Function
def stereo_spectrum(signal, sr):
    segment_size = sr
    noverlap = segment_size / 2
    ref = 2e-5  # 20 uPa

    # Source
    x_source = signal[1] * (2**15)  # scale signal to [-1.0 .. 1.0]
    f_source, Pxx_source = sp.signal.welch(
        x_source,  # signal
        fs=sr,  # sample rate
        nperseg=segment_size,  # segment size
        window='hann',  # window type to use
        nfft=segment_size,  # num. of samples in FFT
        detrend=False,  # remove DC part
        scaling='spectrum',  # return power spectrum [V^2]
        noverlap=noverlap)  # overlap between segments
    p_source = librosa.power_to_db(Pxx_source, ref=ref) + 4.5

    # Receiver
    x_receiver = signal[0] * (2**15)  # scale signal to [-1.0 .. 1.0]
    f_receiver, Pxx_receiver = sp.signal.welch(
        x_receiver,  # signal
        fs=sr,  # sample rate
        nperseg=segment_size,  # segment size
        window='hann',  # window type to use
        nfft=segment_size,  # num. of samples in FFT
        detrend=False,  # remove DC part
        scaling='spectrum',  # return power spectrum [V^2]
        noverlap=noverlap)  # overlap between segments
    p_receiver = librosa.power_to_db(Pxx_receiver, ref=ref) + 4.5

    return f_source, p_source, f_receiver, p_receiver


def mono_spectrum(signal, sr):
    segment_size = sr
    noverlap = segment_size / 2
    ref = 2e-5  # 20 uPa

    x = signal * (2**15)  # scale signal to [-1.0 .. 1.0]
    f, Pxx = sp.signal.welch(
        x,  # signal
        fs=sr,  # sample rate
        nperseg=segment_size,  # segment size
        window='hann',  # window type to use
        nfft=segment_size,  # num. of samples in FFT
        detrend=False,  # remove DC part
        scaling='spectrum',  # return power spectrum [V^2]
        noverlap=noverlap)  # overlap between segments
    p = librosa.power_to_db(Pxx, ref=ref) - 50.0

    return f, p


# Spectrogram
def stereo_spectrogram(signal, sr):
    # Source
    stft_source = librosa.stft(signal[1])
    spectrogram_source = librosa.amplitude_to_db(np.abs(stft_source))

    # Receiver
    stft_receiver = librosa.stft(signal[0])
    spectrogram_receiver = librosa.amplitude_to_db(np.abs(stft_receiver))

    return spectrogram_source, spectrogram_receiver


def mono_spectrogram(signal, sr):
    stft = librosa.stft(signal)
    spectrogram = librosa.amplitude_to_db(np.abs(stft))

    return spectrogram
