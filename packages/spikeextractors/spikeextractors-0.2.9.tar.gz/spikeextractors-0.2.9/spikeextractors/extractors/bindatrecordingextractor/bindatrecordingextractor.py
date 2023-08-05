from spikeextractors import RecordingExtractor
import os
import numpy as np
from pathlib import Path


class BinDatRecordingExtractor(RecordingExtractor):
    def __init__(self, datfile, samplerate, numchan, frames_first=True, dtype=None, geom=None):
        RecordingExtractor.__init__(self)
        self._datfile = Path(datfile)
        if dtype == None:
            dtype = np.float32
        self._frame_first = frames_first
        self._timeseries = _read_binary(self._datfile, numchan, dtype, frames_first)
        self._samplerate = float(samplerate)
        self._geom = geom
        if geom is not None:
            for m in range(self._timeseries.shape[0]):
                self.setChannelProperty(m, 'location', self._geom[m, :])

    def getChannelIds(self):
        return list(range(self._timeseries.shape[0]))

    def getNumFrames(self):
        return self._timeseries.shape[1]

    def getSamplingFrequency(self):
        return self._samplerate

    def getTraces(self, channel_ids=None, start_frame=None, end_frame=None):
        if start_frame is None:
            start_frame = 0
        if end_frame is None:
            end_frame = self.getNumFrames()
        if channel_ids is None:
            channel_ids = self.getChannelIds()
        recordings = self._timeseries[:, start_frame:end_frame][channel_ids, :]
        return recordings

    @staticmethod
    def writeRecording(recording, save_path, dtype=None, transpose=False):
        save_path = Path(save_path)
        if dtype == None:
            dtype = np.float32
        if not transpose:
            with save_path.open('wb') as f:
                np.transpose(np.array(recording.getTraces(), dtype=dtype)).tofile(f)
        elif transpose:
            with save_path.open('wb') as f:
                np.array(recording.getTraces(), dtype=dtype).tofile(f)


def _read_binary(file, numchan, dtype, frames_first):
    numchan = int(numchan)
    with Path(file).open() as f:
        nsamples = os.fstat(f.fileno()).st_size // (numchan * np.dtype(dtype).itemsize)
        if frames_first:
            samples = np.memmap(f, np.dtype(dtype), mode='r',
                                shape=(nsamples, numchan))
            samples = np.transpose(samples)
        else:
            samples = np.memmap(f, np.dtype(dtype), mode='r',
                                shape=(numchan, nsamples))
    return samples
