import numpy as np
import pandas as pd
import AudioProcess
import PyOctaveBand
import librosa


# Function to export audio data
def export_data(signal, sr, url, path):
    if (len(signal.shape) > 1):  # Stereo audio format
        # Full spectrum

        f_source, p_source, f_receiver, p_receiver = AudioProcess.stereo_spectrum(
            signal, sr)

        # One third octave
        # Source
        spl_source, freq_source = PyOctaveBand.octavefilter(signal[1],
                                                            sr,
                                                            fraction=3,
                                                            limits=[20, 25000],
                                                            show=False,
                                                            sigbands=False)
        spl_source = np.asanyarray(spl_source) + 48
        freq_source = PyOctaveBand.normalizedfreq(
            fraction=3)[2:len(spl_source) + 2]

        # Receiver
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

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(path + "/" + url.fileName() + '_result.xlsx',
                                engine='xlsxwriter')

        # Export data as csv
        data_source = {
            "Full Spectrum Frequency [Hz]": f_source[0:8001],
            "Full Spectrum Magnitude [dB/20u]": p_source[0:8001],
            "": "",
            "1/3 Octave Frequency [Hz]": freq_source,
            "1/3 Octave Magnitude [dB/20u]": spl_source
        }

        data_receiver = {
            "Full Spectrum Frequency [Hz]": f_receiver[0:8001],
            "Full Spectrum Magnitude [dB/20u]": p_receiver[0:8001],
            "": "",
            "1/3 Octave Frequency [Hz]": freq_receiver,
            "1/3 Octave Magnitude [dB/20u]": spl_receiver
        }

        df_source = pd.DataFrame(
            {key: pd.Series(value)
             for key, value in data_source.items()})

        df_receiver = pd.DataFrame(
            {key: pd.Series(value)
             for key, value in data_receiver.items()})

        # Write to csv
        df_source.to_excel(writer, sheet_name='Source', index=False)
        df_receiver.to_excel(writer, sheet_name='Receiver', index=False)

        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 35)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 26)
            worksheet.set_column('E:E', 30)
        writer.save()

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

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(path + "/" + url.fileName() + '_result.xlsx',
                                engine='xlsxwriter')

        # Export data as csv
        data_dict = {
            "Full Spectrum Frequency [Hz]": f[0:8001],
            "Full Spectrum Magnitude [dB/20u]": p[0:8001],
            "": "",
            "1/3 Octave Frequency [Hz]": freq,
            "1/3 Octave Magnitude [dB/20u]": spl
        }

        df_data = pd.DataFrame.from_dict(
            {key: pd.Series(value)
             for key, value in data_dict.items()})

        # Write to csv
        df_data.to_excel(writer, sheet_name='Data', index=False)

        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 35)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 26)
            worksheet.set_column('E:E', 30)
        writer.save()


def export_average(pathList, exportPath, filename):
    mono_count, stero_count, total_spl_source, total_spl_receiver, total_p_source, total_p_receiver, total_spl, total_p = 0, 0, 0, 0, 0, 0, 0, 0
    global f_source, f_receiver, freq_source, freq_receiver, f, freq
    global mono_status, stereo_status

    mono_status, stereo_status = False, False
    mono_list, stereo_list, sd_source_array, sd_receiver_array, sd_array = [], [], [], [], []

    for path in pathList:
        signal, sr = librosa.load(path, sr=None, mono=False)  #Load audio file

        if (len(signal.shape) > 1):  # Stereo audio format
            stereo_status = True
            stereo_list.append(path)
            # Full spectrum
            f_source, p_source, f_receiver, p_receiver = AudioProcess.stereo_spectrum(
                signal, sr)

            # One third octave
            # Source
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

            # Receiver
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

            # Total
            total_spl_source += spl_source
            total_spl_receiver += spl_receiver
            total_p_source += p_source
            total_p_receiver += p_receiver
            stero_count += 1

        else:  # Mono audio format
            mono_status = True
            mono_list.append(path)
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

    # Export
    if stereo_status:
        writer = pd.ExcelWriter(exportPath + "/" + filename + ".xlsx",
                                engine='xlsxwriter')

        df_stereo_list = pd.DataFrame({"Audio Paths": stereo_list},
                                      columns=["Audio Paths"])

        data_source = {
            "Full Spectrum Frequency [Hz]": f_source[0:8001],
            "Full Spectrum Magnitude [dB/20u]":
            total_p_source[0:8001] / stero_count,
            "": "",
            "1/3 Octave Frequency [Hz]": freq_source,
            "1/3 Octave Magnitude [dB/20u]": total_spl_source / stero_count,
            "Standard Deviation": np.std(sd_source_array, axis=0).tolist()
        }

        data_receiver = {
            "Full Spectrum Frequency [Hz]": f_receiver[0:8001],
            "Full Spectrum Magnitude [dB/20u]":
            total_p_receiver[0:8001] / stero_count,
            "": "",
            "1/3 Octave Frequency [Hz]": freq_receiver,
            "1/3 Octave Magnitude [dB/20u]": total_spl_receiver / stero_count,
            "Standard Deviation": np.std(sd_receiver_array, axis=0).tolist()
        }

        df_source = pd.DataFrame(
            {key: pd.Series(value)
             for key, value in data_source.items()})

        df_receiver = pd.DataFrame(
            {key: pd.Series(value)
             for key, value in data_receiver.items()})

        # Write to csv
        df_stereo_list.to_excel(writer, sheet_name='Audio Files', index=False)

        df_source.to_excel(writer, sheet_name='Avg Source', index=False)
        df_receiver.to_excel(writer, sheet_name='Avg Receiver', index=False)

        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 35)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 26)
            worksheet.set_column('E:E', 30)
            worksheet.set_column('F:F', 30)
        writer.save()
    else:
        pass

    if mono_status:
        writer = pd.ExcelWriter(exportPath + "/" + filename + ".xlsx",
                                engine='xlsxwriter')

        df_mono_list = pd.DataFrame({"Audio Paths": mono_list},
                                    columns=["Audio Paths"])

        data_dict = {
            "Full Spectrum Frequency [Hz]": f[0:8001],
            "Full Spectrum Magnitude [dB/20u]": total_p[0:8001] / mono_count,
            "": "",
            "1/3 Octave Frequency [Hz]": freq,
            "Magnitude [dB/20u]": total_spl / mono_count,
            "Standard Deviation": np.std(sd_array, axis=0).tolist()
        }

        df_data = pd.DataFrame.from_dict(
            {key: pd.Series(value)
             for key, value in data_dict.items()})

        # Write to csv
        df_mono_list.to_excel(writer, sheet_name='Audio Files', index=False)
        df_data.to_excel(writer, sheet_name="Avg Data", index=False)

        for sheet in writer.sheets:
            worksheet = writer.sheets[sheet]
            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 35)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 26)
            worksheet.set_column('E:E', 30)
            worksheet.set_column('F:F', 30)
        writer.save()

    else:
        pass


def export_multiple_average(pathListArray, legendList, exportPath, filename):
    mono_list, stereo_list, sd_source_array, sd_receiver_array, sd_array = [], [], [], [], []
    writer = pd.ExcelWriter(exportPath + "/" + filename + ".xlsx",
                            engine='xlsxwriter')

    for i, pathList in enumerate(pathListArray):
        mono_count, stero_count, total_spl_source, total_spl_receiver, total_p_source, total_p_receiver, total_spl, total_p = 0, 0, 0, 0, 0, 0, 0, 0
        global f_source, f_receiver, freq_source, freq_receiver, f, freq
        global mono_status, stereo_status
        mono_status, stereo_status = False, False
        mono_list.append(legendList[i])
        stereo_list.append(legendList[i])

        for path in pathList:
            signal, sr = librosa.load(path, sr=None,
                                      mono=False)  #Load audio file

            if (len(signal.shape) > 1):  # Stereo audio format
                stereo_status = True
                stereo_list.append(path)
                # Full spectrum
                f_source, p_source, f_receiver, p_receiver = AudioProcess.stereo_spectrum(
                    signal, sr)

                # One third octave
                # Source
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

                # Receiver
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

                # Total
                total_spl_source += spl_source
                total_spl_receiver += spl_receiver
                total_p_source += p_source
                total_p_receiver += p_receiver
                stero_count += 1

            else:  # Mono audio format
                mono_status = True
                mono_list.append(path)
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

        # Export
        if stereo_status:
            df_stereo_list = pd.DataFrame({"Audio Lists": stereo_list},
                                          columns=["Audio Lists"])

            data_source = {
                "Full Spectrum Frequency [Hz]": f_source[0:8001],
                "Full Spectrum Magnitude [dB/20u]":
                total_p_source[0:8001] / stero_count,
                "": "",
                "1/3 Octave Frequency [Hz]": freq_source,
                "1/3 Octave Magnitude [dB/20u]":
                total_spl_source / stero_count,
                "Standard Deviation": np.std(sd_source_array, axis=0).tolist()
            }

            data_receiver = {
                "Full Spectrum Frequency [Hz]": f_receiver[0:8001],
                "Full Spectrum Magnitude [dB/20u]":
                total_p_receiver[0:8001] / stero_count,
                "": "",
                "1/3 Octave Frequency [Hz]": freq_receiver,
                "1/3 Octave Magnitude [dB/20u]":
                total_spl_receiver / stero_count,
                "Standard Deviation": np.std(sd_receiver_array,
                                             axis=0).tolist()
            }

            df_source = pd.DataFrame(
                {key: pd.Series(value)
                 for key, value in data_source.items()})

            df_receiver = pd.DataFrame({
                key: pd.Series(value)
                for key, value in data_receiver.items()
            })

            # Write to csv
            df_stereo_list.to_excel(writer,
                                    sheet_name='Audio Lists',
                                    index=False)

            df_source.to_excel(writer,
                               sheet_name=legendList[i] + ' Source',
                               index=False)
            df_receiver.to_excel(writer,
                                 sheet_name=legendList[i] + ' Receiver',
                                 index=False)

        else:
            pass

        if mono_status:
            df_mono_list = pd.DataFrame({"Audio Lists": mono_list},
                                        columns=["Audio Lists"])

            data_dict = {
                "Full Spectrum Frequency [Hz]": f[0:8001],
                "Full Spectrum Magnitude [dB/20u]":
                total_p[0:8001] / mono_count,
                "": "",
                "1/3 Octave Frequency [Hz]": freq,
                "Magnitude [dB/20u]": total_spl / mono_count,
                "Standard Deviation": np.std(sd_array, axis=0).tolist()
            }

            df_data = pd.DataFrame.from_dict(
                {key: pd.Series(value)
                 for key, value in data_dict.items()})

            # Write to csv
            df_mono_list.to_excel(writer,
                                  sheet_name='Audio Lists',
                                  index=False)

            df_data.to_excel(writer, sheet_name=legendList[i], index=False)

        else:
            pass

    for sheet in writer.sheets:
        worksheet = writer.sheets[sheet]
        worksheet.set_column('A:A', 30)
        worksheet.set_column('B:B', 35)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 26)
        worksheet.set_column('E:E', 30)
        worksheet.set_column('F:F', 30)
    writer.save()
