from pyAudioAnalysis import audioFeatureExtraction as aF
from pyAudioAnalysis import audioBasicIO as aIO
from Tyiannak.video_features import VideoFeatureExtractor

class BaseExtractor:
    def __init__(self, file):
        self._file = file


class VideoExtractor(BaseExtractor):
    _features = ['Color-R0', 'Color-R1', 'Color-R2', 'Color-R3', 'Color-R4', 'Color-R5', 'Color-R6', 'Color-R7', 'Color-R8', 'Color-R9', 'Color-R10', 'Color-R11', 'Color-R12', 'Color-R13', 'Color-R14', 'Color-R15', 'Color-G0', 'Color-G1', 'Color-G2', 'Color-G3', 'Color-G4', 'Color-G5', 'Color-G6', 'Color-G7', 'Color-G8', 'Color-G9', 'Color-G10', 'Color-G11', 'Color-G12', 'Color-G13', 'Color-G14', 'Color-G15', 'Color-B0', 'Color-B1', 'Color-B2', 'Color-B3', 'Color-B4', 'Color-B5', 'Color-B6', 'Color-B7', 'Color-B8', 'Color-B9', 'Color-B10', 'Color-B11', 'Color-B12', 'Color-B13', 'Color-B14', 'Color-B15', 'Color-Gray0', 'Color-Gray1', 'Color-Gray2', 'Color-Gray3', 'Color-Gray4', 'Color-Gray5', 'Color-Gray6', 'Color-Gray7', 'Color-Gray8', 'Color-Gray9', 'Color-Gray10', 'Color-Gray11', 'Color-Gray12', 'Color-Gray13', 'Color-Gray14', 'Color-Gray15', 'Color-GraySobel0', 'Color-GraySobel1', 'Color-GraySobel2', 'Color-GraySobel3', 'Color-GraySobel4', 'Color-GraySobel5', 'Color-GraySobel6', 'Color-GraySobel7', 'Color-GraySobel8', 'Color-GraySobel9', 'Color-GraySobel10', 'Color-GraySobel11', 'Color-GraySobel12', 'Color-GraySobel13', 'Color-GraySobel14', 'Color-GraySobel15', 'Color-Satur0', 'Color-Satur1', 'Color-Satur2', 'Color-Satur3', 'Color-Satur4', 'Color-Satur5', 'Color-Satur6', 'Color-Satur7', 'Color-Satur8', 'Color-Satur9', 'Color-Satur10', 'Color-Satur11', 'Color-Satur12', 'Color-Satur13', 'Color-Satur14', 'Color-Satur15', 'LBP00', 'LBP01', 'LBP02', 'LBP03', 'LBP04', 'LBP05', 'LBP06', 'LBP07', 'LBP08', 'LBP09', 'LBP10', 'LBP11', 'LBP12', 'LBP13', 'LBP14', 'LBP15', 'LBP16', 'LBP17', 'LBP18', 'LBP19', 'LBP20', 'LBP21', 'LBP22', 'LBP23', 'LBP24', 'LBP25', 'LBP26', 'LBP27', 'LBP28', 'LBP29', 'LBP30', 'LBP31', 'LBP32', 'LBP33', 'LBP34', 'LBP35', 'LBP36', 'LBP37', 'LBP38', 'LBP39', 'LBP40', 'LBP41', 'LBP42', 'LBP43', 'LBP44', 'LBP45', 'LBP46', 'LBP47', 'LBP48', 'LBP49', 'LBP50', 'LBP51', 'LBP52', 'LBP53', 'LBP54', 'LBP55', 'LBP56', 'LBP57', 'LBP58', 'LBP59', 'LBP60', 'LBP61', 'LBP62', 'LBP63', 'LBP64', 'LBP65', 'LBP66', 'LBP67', 'LBP68', 'LBP69', 'LBP70', 'LBP71', 'LBP72', 'LBP73', 'LBP74', 'LBP75', 'LBP76', 'LBP77', 'LBP78', 'LBP79', 'LBP80', 'LBP81', 'LBP82', 'LBP83', 'LBP84', 'LBP85', 'LBP86', 'LBP87', 'LBP88', 'LBP89', 'LBP90', 'LBP91', 'LBP92', 'LBP93', 'LBP94', 'LBP95', 'LBP96', 'LBP97', 'LBP98', 'LBP99', 'LBP100', 'LBP101', 'LBP102', 'LBP103', 'LBP104', 'LBP105', 'LBP106', 'LBP107', 'LBP108', 'LBP109', 'LBP110', 'LBP111', 'LBP112', 'LBP113', 'LBP114', 'LBP115', 'LBP116', 'LBP117', 'LBP118', 'LBP119', 'LBP120', 'LBP121', 'LBP122', 'LBP123', 'LBP124', 'LBP125', 'LBP126', 'LBP127', 'HOG00', 'HOG01', 'HOG02', 'HOG03', 'HOG04', 'HOG05', 'HOG06', 'HOG07', 'HOG08', 'HOG09', 'HOG10', 'HOG11', 'HOG12', 'HOG13', 'HOG14', 'HOG15', 'HOG16', 'HOG17', 'HOG18', 'HOG19', 'HOG20', 'HOG21', 'HOG22', 'HOG23', 'HOG24', 'HOG25', 'HOG26', 'HOG27', 'HOG28', 'HOG29', 'HOG30', 'HOG31', 'HOG32', 'HOG33', 'HOG34', 'HOG35', 'HOG36', 'HOG37', 'HOG38', 'HOG39', 'HOG40', 'HOG41', 'HOG42', 'HOG43', 'HOG44', 'HOG45', 'HOG46', 'HOG47', 'HOG48', 'HOG49', 'HOG50', 'HOG51', 'HOG52', 'HOG53', 'HOG54', 'HOG55', 'HOG56', 'HOG57', 'HOG58', 'HOG59', 'HOG60', 'HOG61', 'HOG62', 'HOG63', 'HOG64', 'HOG65', 'HOG66', 'HOG67', 'HOG68', 'HOG69', 'HOG70', 'HOG71', 'HOG72', 'HOG73', 'HOG74', 'HOG75', 'HOG76', 'HOG77', 'HOG78', 'HOG79', 'HOG80', 'HOG81', 'HOG82', 'HOG83', 'HOG84', 'HOG85', 'HOG86', 'HOG87', 'HOG88', 'HOG89', 'HOG90', 'HOG91', 'HOG92', 'HOG93', 'HOG94', 'HOG95', 'HOG96', 'HOG97', 'HOG98', 'HOG99', 'HOG100', 'HOG101', 'HOG102', 'HOG103', 'HOG104', 'HOG105', 'HOG106', 'HOG107', 'HOG108', 'HOG109', 'HOG110', 'HOG111', 'HOG112', 'HOG113', 'HOG114', 'HOG115', 'HOG116', 'HOG117', 'HOG118', 'HOG119', 'HOG120', 'HOG121', 'HOG122', 'HOG123', 'HOG124', 'HOG125', 'HOG126', 'HOG127', 'm', 's']


class SoundExtractor(BaseExtractor):
    _features = ['zcr', 'energy', 'energy_entropy', 'spectral_centroid', 'spectral_spread', 'spectral_entropy', 'spectral_flux', 'spectral_rolloff', 'mfcc_1', 'mfcc_2', 'mfcc_3', 'mfcc_4', 'mfcc_5', 'mfcc_6', 'mfcc_7', 'mfcc_8', 'mfcc_9', 'mfcc_10', 'mfcc_11', 'mfcc_12', 'mfcc_13', 'chroma_1', 'chroma_2', 'chroma_3', 'chroma_4', 'chroma_5', 'chroma_6', 'chroma_7', 'chroma_8', 'chroma_9', 'chroma_10', 'chroma_11', 'chroma_12', 'chroma_std']


class FeatureExtractor(SoundExtractor, VideoExtractor):
    pass


if __name__ == '__main__':
    # read machine sound
    fs, s = aIO.readAudioFile("juan_atkins_urban_tropics.wav")
    duration = len(s) / float(fs)
    # extract short term features
    [f, fn] = aF.stFeatureExtraction(s, fs, int(fs * 0.050), int(fs * 0.050))
    print(duration)
    print(f.T[0].shape)
    print(fn)
