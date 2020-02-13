from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.tools import subprocess_call
from moviepy.config import get_setting
from pyAudioAnalysis import audioFeatureExtraction as aF
from pyAudioAnalysis import audioBasicIO as aIO
from Tyiannak.video_features import VideoFeatureExtractor
import cv2
import os
import os.path
from app import db
from app.models import Segment, SegmentFeatures, Feature, Video
import numpy as np
import multiprocessing as mp


class VideoSplitter:
    _segment_duration = 10
    _file = None
    _duration = 0
    _r = []

    def set_file(self, file):
        self._file = file
        self._duration = int(self.get_duration())
        # step = int(self._segment_duration // 2)
        step = self._segment_duration  # no overlap
        self._r = range(0, self._duration-self._segment_duration, step)

    def split(self):
        for t in self._r:
            video_file = "vid.part"+str(t)+"."+self._file
            audio_file = "aud.part"+str(t)+"."+self._file+".wav"
            ffmpeg_extract_subclip(self._file, t, t+self._segment_duration, targetname=video_file)

            # pyAudioAnalysis accepts mono -> refactor ffmpeg_extract_audio #
            bitrate = 3000
            fps = 44100
            cmd = [get_setting("FFMPEG_BINARY"), "-y", "-i", video_file, "-ac", "1", "-ab", "%dk"%bitrate, "-ar", "%d"%fps, audio_file]
            subprocess_call(cmd)

        return self._r

    def delete_parts(self):
        for t in self._r:
            os.remove("vid.part"+str(t)+"."+self._file)
            os.remove("aud.part"+str(t)+"."+self._file+".wav")

    def get_duration(self):
        capture = cv2.VideoCapture(self._file)
        n_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = capture.get(cv2.CAP_PROP_FPS)
        return n_frames / fps

    def get_segment_end(self, start):
        return min(self._duration, start + self._segment_duration)


class Processor:
    _video_features = ['Color-R0', 'Color-R1', 'Color-R2', 'Color-R3', 'Color-R4', 'Color-R5', 'Color-R6', 'Color-R7', 'Color-R8', 'Color-R9', 'Color-R10', 'Color-R11', 'Color-R12', 'Color-R13', 'Color-R14', 'Color-R15', 'Color-G0', 'Color-G1', 'Color-G2', 'Color-G3', 'Color-G4', 'Color-G5', 'Color-G6', 'Color-G7', 'Color-G8', 'Color-G9', 'Color-G10', 'Color-G11', 'Color-G12', 'Color-G13', 'Color-G14', 'Color-G15', 'Color-B0', 'Color-B1', 'Color-B2', 'Color-B3', 'Color-B4', 'Color-B5', 'Color-B6', 'Color-B7', 'Color-B8', 'Color-B9', 'Color-B10', 'Color-B11', 'Color-B12', 'Color-B13', 'Color-B14', 'Color-B15', 'Color-Gray0', 'Color-Gray1', 'Color-Gray2', 'Color-Gray3', 'Color-Gray4', 'Color-Gray5', 'Color-Gray6', 'Color-Gray7', 'Color-Gray8', 'Color-Gray9', 'Color-Gray10', 'Color-Gray11', 'Color-Gray12', 'Color-Gray13', 'Color-Gray14', 'Color-Gray15', 'Color-GraySobel0', 'Color-GraySobel1', 'Color-GraySobel2', 'Color-GraySobel3', 'Color-GraySobel4', 'Color-GraySobel5', 'Color-GraySobel6', 'Color-GraySobel7', 'Color-GraySobel8', 'Color-GraySobel9', 'Color-GraySobel10', 'Color-GraySobel11', 'Color-GraySobel12', 'Color-GraySobel13', 'Color-GraySobel14', 'Color-GraySobel15', 'Color-Satur0', 'Color-Satur1', 'Color-Satur2', 'Color-Satur3', 'Color-Satur4', 'Color-Satur5', 'Color-Satur6', 'Color-Satur7', 'Color-Satur8', 'Color-Satur9', 'Color-Satur10', 'Color-Satur11', 'Color-Satur12', 'Color-Satur13', 'Color-Satur14', 'Color-Satur15', 'LBP00', 'LBP01', 'LBP02', 'LBP03', 'LBP04', 'LBP05', 'LBP06', 'LBP07', 'LBP08', 'LBP09', 'LBP10', 'LBP11', 'LBP12', 'LBP13', 'LBP14', 'LBP15', 'LBP16', 'LBP17', 'LBP18', 'LBP19', 'LBP20', 'LBP21', 'LBP22', 'LBP23', 'LBP24', 'LBP25', 'LBP26', 'LBP27', 'LBP28', 'LBP29', 'LBP30', 'LBP31', 'LBP32', 'LBP33', 'LBP34', 'LBP35', 'LBP36', 'LBP37', 'LBP38', 'LBP39', 'LBP40', 'LBP41', 'LBP42', 'LBP43', 'LBP44', 'LBP45', 'LBP46', 'LBP47', 'LBP48', 'LBP49', 'LBP50', 'LBP51', 'LBP52', 'LBP53', 'LBP54', 'LBP55', 'LBP56', 'LBP57', 'LBP58', 'LBP59', 'LBP60', 'LBP61', 'LBP62', 'LBP63', 'LBP64', 'LBP65', 'LBP66', 'LBP67', 'LBP68', 'LBP69', 'LBP70', 'LBP71', 'LBP72', 'LBP73', 'LBP74', 'LBP75', 'LBP76', 'LBP77', 'LBP78', 'LBP79', 'LBP80', 'LBP81', 'LBP82', 'LBP83', 'LBP84', 'LBP85', 'LBP86', 'LBP87', 'LBP88', 'LBP89', 'LBP90', 'LBP91', 'LBP92', 'LBP93', 'LBP94', 'LBP95', 'LBP96', 'LBP97', 'LBP98', 'LBP99', 'LBP100', 'LBP101', 'LBP102', 'LBP103', 'LBP104', 'LBP105', 'LBP106', 'LBP107', 'LBP108', 'LBP109', 'LBP110', 'LBP111', 'LBP112', 'LBP113', 'LBP114', 'LBP115', 'LBP116', 'LBP117', 'LBP118', 'LBP119', 'LBP120', 'LBP121', 'LBP122', 'LBP123', 'LBP124', 'LBP125', 'LBP126', 'LBP127', 'HOG00', 'HOG01', 'HOG02', 'HOG03', 'HOG04', 'HOG05', 'HOG06', 'HOG07', 'HOG08', 'HOG09', 'HOG10', 'HOG11', 'HOG12', 'HOG13', 'HOG14', 'HOG15', 'HOG16', 'HOG17', 'HOG18', 'HOG19', 'HOG20', 'HOG21', 'HOG22', 'HOG23', 'HOG24', 'HOG25', 'HOG26', 'HOG27', 'HOG28', 'HOG29', 'HOG30', 'HOG31', 'HOG32', 'HOG33', 'HOG34', 'HOG35', 'HOG36', 'HOG37', 'HOG38', 'HOG39', 'HOG40', 'HOG41', 'HOG42', 'HOG43', 'HOG44', 'HOG45', 'HOG46', 'HOG47', 'HOG48', 'HOG49', 'HOG50', 'HOG51', 'HOG52', 'HOG53', 'HOG54', 'HOG55', 'HOG56', 'HOG57', 'HOG58', 'HOG59', 'HOG60', 'HOG61', 'HOG62', 'HOG63', 'HOG64', 'HOG65', 'HOG66', 'HOG67', 'HOG68', 'HOG69', 'HOG70', 'HOG71', 'HOG72', 'HOG73', 'HOG74', 'HOG75', 'HOG76', 'HOG77', 'HOG78', 'HOG79', 'HOG80', 'HOG81', 'HOG82', 'HOG83', 'HOG84', 'HOG85', 'HOG86', 'HOG87', 'HOG88', 'HOG89', 'HOG90', 'HOG91', 'HOG92', 'HOG93', 'HOG94', 'HOG95', 'HOG96', 'HOG97', 'HOG98', 'HOG99', 'HOG100', 'HOG101', 'HOG102', 'HOG103', 'HOG104', 'HOG105', 'HOG106', 'HOG107', 'HOG108', 'HOG109', 'HOG110', 'HOG111', 'HOG112', 'HOG113', 'HOG114', 'HOG115', 'HOG116', 'HOG117', 'HOG118', 'HOG119', 'HOG120', 'HOG121', 'HOG122', 'HOG123', 'HOG124', 'HOG125', 'HOG126', 'HOG127', 'm', 's']
    # _audio_features = ['zcr', 'energy', 'energy_entropy', 'spectral_centroid', 'spectral_spread', 'spectral_entropy', 'spectral_flux', 'spectral_rolloff', 'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11', 'mfcc_12', 'mfcc_13', 'chroma_1', 'chroma_2', 'chroma_3', 'chroma_4', 'chroma_5', 'chroma_6', 'chroma_7', 'chroma_8', 'chroma_9', 'chroma_10', 'chroma_11', 'chroma_12', 'chroma_std']
    _audio_features = ['zcr_mean', 'energy_mean', 'energy_entropy_mean', 'spectral_centroid_mean', 'spectral_spread_mean', 'spectral_entropy_mean', 'spectral_flux_mean', 'spectral_rolloff_mean', 'mfcc_1_mean', 'mfcc_2_mean', 'mfcc_3_mean', 'mfcc_4_mean', 'mfcc_5_mean', 'mfcc_6_mean', 'mfcc_7_mean', 'mfcc_8_mean', 'mfcc_9_mean', 'mfcc_10_mean', 'mfcc_11_mean', 'mfcc_12_mean', 'mfcc_13_mean', 'chroma_1_mean', 'chroma_2_mean', 'chroma_3_mean', 'chroma_4_mean', 'chroma_5_mean', 'chroma_6_mean', 'chroma_7_mean', 'chroma_8_mean', 'chroma_9_mean', 'chroma_10_mean', 'chroma_11_mean', 'chroma_12_mean', 'chroma_std_mean', 'zcr_std', 'energy_std', 'energy_entropy_std', 'spectral_centroid_std', 'spectral_spread_std', 'spectral_entropy_std', 'spectral_flux_std', 'spectral_rolloff_std', 'mfcc_1_std', 'mfcc_2_std', 'mfcc_3_std', 'mfcc_4_std', 'mfcc_5_std', 'mfcc_6_std', 'mfcc_7_std', 'mfcc_8_std', 'mfcc_9_std', 'mfcc_10_std', 'mfcc_11_std', 'mfcc_12_std', 'mfcc_13_std', 'chroma_1_std', 'chroma_2_std', 'chroma_3_std', 'chroma_4_std', 'chroma_5_std', 'chroma_6_std', 'chroma_7_std', 'chroma_8_std', 'chroma_9_std', 'chroma_10_std', 'chroma_11_std', 'chroma_12_std', 'chroma_std_std']

    def __init__(self):
        self._file = None
        self._splitter = VideoSplitter()
        self._video_extractor = VideoFeatureExtractor(resize_width=256, step=0.51)
        self._features = []

        # get a map connecting feature names to db ids
        db_video_features = Feature.query.filter(Feature.description.in_(self._video_features)).all()
        video_feature_map = {dvf.description: dvf.id for dvf in db_video_features}

        db_audio_features = Feature.query.filter(Feature.description.in_(self._audio_features)).all()
        audio_feature_map = {daf.description: daf.id for daf in db_audio_features}
        # merge into one map
        self._feature_map = {**video_feature_map, **audio_feature_map}

    def process_file(self, file, video_id):
        if not os.path.isfile(file):
            print('Could not locate file: ' + file)
            return

        # 1. split file
        self._splitter.set_file(file)
        parts = self._splitter.split()

        # all part features per part as row

        # 2. extract features
        pool = mp.Pool(int(mp.cpu_count()/2))
        segments = pool.starmap_async(self.get_segments, [(file, part, video_id) for part in parts]).get()
        pool.close()
        pool.join()

        # 3. save to database
        for segment in filter(None, segments):
            db.session.add(segment)
        db.session.commit()
        self._splitter.delete_parts()

    def get_segments(self, file, part, video_id):

        try:
            audio_file = "aud.part"+str(part)+"."+file+".wav"
            fs, s = aIO.readAudioFile(audio_file)
            af, _, afn = aF.mtFeatureExtraction(s, fs, int(0.5*fs), int(0.5*fs), int(0.1*fs), int(0.1*fs))

            video_file = "vid.part"+str(part)+"."+file
            vf, t, vfn = self._video_extractor.extract_features(video_file)

        except Exception as e:
            print(e)
            return None
        else:
            segment_features = []
            # construct segmentfeature

            vmean = vf.T.mean(axis=1)
            for i, val in enumerate(vmean):
                if isinstance(val, np.ndarray):
                    val = val[0]

                feature = SegmentFeatures(value=val, seq_no=1, feature_id=self._feature_map[vfn[i]])
                segment_features.append(feature)

            amean = af.mean(axis=1)
            for i, val in enumerate(amean):
                feature = SegmentFeatures(value=val, seq_no=1, feature_id=self._feature_map[afn[i]])
                segment_features.append(feature)

            # construct segment with its segmentfeatures
            segment = Segment(video_id=video_id, start_sec=part, end_sec=self._splitter.get_segment_end(part), features=segment_features)

            return segment


if __name__ == '__main__':
    """Extract features for downloaded videos in database with no segments"""
    p = Processor()

    cwd = os.getcwd()
    videos = Video.query.outerjoin(Segment).filter(Video.search == False, Segment.video_id.is_(None)).all()
    for video in videos:
        os.chdir(video.directory)
        p.process_file(video.file, video.id)
        os.chdir(cwd)


