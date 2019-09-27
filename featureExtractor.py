from rawFeatureHandler.rawFeatureHandler import rawHandler
from rawFeatureExtractor.runIDAPro import extractByIDAPro, MultiThreadingExtractByIDAPro
import threading

import os, shutil


binary_dir_path = '/Users/Max/Documents/capstone/FeatureEngineering/FeatureResource/binary/'
rawFeatures_path = '/Users/Max/Documents/capstone/FeatureEngineering/FeatureResource/rawFeatures/'
final_feature_path = '/Users/Max/Documents/capstone/FeatureEngineering/FeatureResource/features/'

class featureGenerator():
    def __init__(self, binary_dir, rawFeatures_dir):
        self.binary_dir = binary_dir
        self.rawFeature_dir = rawFeatures_dir

    def extractIDAFilefromBinary(self):
        print('[INFO] Generating IDA File for Binary by IDA Pro')
        for root, dirs, files in os.walk(self.binary_dir):
            for file_name in files:
                if file_name.startswith('.') or (not file_name.endswith('.o') and not file_name.endswith('.so')):
                    continue
                binary_file_path = os.path.join(root, file_name)
                bin_file_relative_path = binary_file_path[len(binary_dir_path):]
                ida_file_relative_path = bin_file_relative_path + '.ida'
                if os.path.exists(os.path.join(rawFeatures_path, ida_file_relative_path)):
                    print("[INFO] Skiping {0}. Found {1}".format(bin_file_relative_path, ida_file_relative_path))
                    continue
                if not extractByIDAPro(binary_file_path):
                    continue

    def collectBinary(self):
        print('[INFO] Generating IDA File for Binary by IDA Pro')
        bin_to_extract = []
        for root, dirs, files in os.walk(self.binary_dir):
            for file_name in files:
                if file_name.startswith('.') or (not file_name.endswith('.o') and not file_name.endswith('.so')):
                    continue
                binary_file_path = os.path.join(root, file_name)
                bin_file_relative_path = binary_file_path[len(binary_dir_path):]
                ida_file_relative_path = bin_file_relative_path + '.ida'
                if os.path.exists(os.path.join(rawFeatures_path, ida_file_relative_path)):
                    print("[INFO] Skiping {0}. Found {1}".format(bin_file_relative_path, ida_file_relative_path))
                    continue
                bin_to_extract.append(binary_file_path)
                #if not extractByIDAPro(binary_file_path):
                #    continue
        return bin_to_extract

    def multithreadingIDA(self):
        bin_files = self.collectBinary()
        if len(bin_files) > 11:
            block_len = len(bin_files)/6
            bin_files_1 = bin_files[0:block_len]
            bin_files_2 = bin_files[block_len:block_len*2]
            bin_files_3 = bin_files[block_len*2:block_len*3]
            bin_files_4 = bin_files[block_len*3:block_len*4]
            bin_files_5 = bin_files[block_len*4:block_len*5]
            bin_files_6 = bin_files[block_len*5:]
            th = [
                threading.Thread(target=MultiThreadingExtractByIDAPro, args=(bin_files_1,)),
                threading.Thread(target=MultiThreadingExtractByIDAPro, args=(bin_files_2,)),
                threading.Thread(target=MultiThreadingExtractByIDAPro, args=(bin_files_3,)),
                threading.Thread(target=MultiThreadingExtractByIDAPro, args=(bin_files_4,)),
                threading.Thread(target=MultiThreadingExtractByIDAPro, args=(bin_files_5,)),
                threading.Thread(target=MultiThreadingExtractByIDAPro, args=(bin_files_6,))
            ]
            for t in th:
                t.start()
            for t in th:
                t.join()
        else:
            MultiThreadingExtractByIDAPro(bin_files)

    def idaFileAnalyzer(self):
        print('[INFO] Extracting Features from IDA File')
        errorlog = []
        for root, dirs, files in os.walk(self.rawFeature_dir):
            for file_name in files:
                if file_name == '.DS_Store' or file_name.startswith('.'):
                    continue
                ida_file_path = os.path.join(root, file_name)
                feature_results = rawHandler(ida_file=ida_file_path, error=errorlog).extractFromGraphs()
                if feature_results == None:
                    continue
                #feature_file_path = os.path.join(final_feature_path, os.path.basename(root)) + '.json'
                feature_file_path = os.path.join(final_feature_path, root[len(rawFeatures_path):].split('/')[0] + '.json')
                #if not os.path.exists(feature_file_path):
                #    os
                print('    Writing Features into {}'.format(feature_file_path))
                with open(feature_file_path, 'a+') as f:
                    for func in feature_results:
                        f.write(func)
                        f.write('\n')
        if len(errorlog) > 0:
            print('[INFO] Error When Extracting: ')
            for error in errorlog:
                print('[-] ' + error)








if __name__ == '__main__':

    #featureGenerator(binary_dir_path, rawFeatures_path).extractIDAFilefromBinary()

    featureGenerator(binary_dir_path, rawFeatures_path).multithreadingIDA()
    featureGenerator(binary_dir_path, rawFeatures_path).idaFileAnalyzer()