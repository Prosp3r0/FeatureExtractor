import subprocess
import subprocess32
import os
import shutil

binary_dir_path = '/Users/Max/Documents/capstone/FeatureEngineering/FeatureResource/binary/'
ida64_path = '/Applications/IDA\ Pro\ 7.0/ida.app/Contents/MacOS/ida64'
ida32_path = r'/Applications/IDA\ Pro\ 7.0/ida.app/Contents/MacOS/idat'
ana_file = '/Users/Max/Documents/capstone/FeatureEngineering/FeatureExtractor/rawFeatureExtractor/preprocessing_ida.py'

rawFeatures_path = '/Users/Max/Documents/capstone/FeatureEngineering/FeatureResource/rawFeatures/'


def extractByIDAPro(binary_file_path):
    print('[+] Processing {0}'.format(binary_file_path))
    cmd = "{0} -L/Users/Max/Documents/capstone/FeatureExtractor/idalog/idalog.log -c -A -S{1} {2}".format(
        ida32_path, ana_file, binary_file_path)
    #p = subprocess.Popen(cmd, shell = True)
    try:
        stdout = subprocess32.check_output(cmd, stderr=subprocess32.STDOUT, shell = True, timeout=600)
    except Exception as e:
        print('  [-] Error Occur in IDA Pro')
        return False
    #p.wait()
    idb = os.path.splitext(binary_file_path)[0] + '.idb'
    if os.path.exists(idb):
        os.remove(idb)
    binary_relative_path = binary_file_path[len(binary_dir_path):]
    #rawFeature_platform_path = os.path.join(rawFeatures_path, os.path.basename(os.path.dirname(binary_file_path)))
    rawFeature_platform_path = os.path.join(rawFeatures_path, os.path.dirname(binary_relative_path) + '/')
    ida_file_path = os.path.join(rawFeatures_path, os.path.basename(binary_file_path) + '.ida')
    #if not os.path.exists()
    if not os.path.exists(rawFeature_platform_path):
        os.makedirs(rawFeature_platform_path, 0755)
    ida_file = os.path.join(rawFeature_platform_path, os.path.basename(ida_file_path))
    if os.path.exists(ida_file):
        os.remove(ida_file)
    shutil.move(ida_file_path, rawFeature_platform_path)
    #return os.basename(binary_file) + '.ida'
    return True

def MultiThreadingExtractByIDAPro(binary_file_path_list):
    for binary_file_path in binary_file_path_list:
        if not os.path.exists(binary_file_path):
            continue
        old_name = os.path.basename(binary_file_path)
        new_path = os.path.join(os.path.dirname(binary_file_path), binary_file_path[len(binary_dir_path):].replace('/', '_'))
        os.rename(binary_file_path, new_path)
        #binary_file_path = new_path
        print('[+] Processing {0}'.format(new_path))
        cmd = "{0} -L/Users/Max/Documents/capstone/FeatureExtractor/idalog/idalog.log -c -A -S{1} {2}".format(
            ida32_path, ana_file, new_path)
        #p = subprocess.Popen(cmd, shell = True)
        try:
            stdout = subprocess32.check_output(cmd, stderr=subprocess32.STDOUT, shell = True, timeout=1200)
        except Exception as e:
            print('  [-] Error Occur in IDA Pro')
            os.rename(new_path, binary_file_path)
            continue
        #p.wait()
        os.rename(new_path, binary_file_path)
        idb = os.path.splitext(new_path)[0] + '.idb'
        if os.path.exists(idb):
            os.remove(idb)
        binary_relative_path = new_path[len(binary_dir_path):]
        #rawFeature_platform_path = os.path.join(rawFeatures_path, os.path.basename(os.path.dirname(binary_file_path)))
        rawFeature_platform_path = os.path.join(rawFeatures_path, os.path.dirname(binary_relative_path) + '/')
        ida_file_path = os.path.join(rawFeatures_path, os.path.basename(new_path) + '.ida')
        #if not os.path.exists()
        if not os.path.exists(rawFeature_platform_path):
            os.makedirs(rawFeature_platform_path, 0755)
        ida_file = os.path.join(rawFeature_platform_path, os.path.basename(ida_file_path))
        if os.path.exists(ida_file):
            os.remove(ida_file)
        shutil.move(ida_file_path, rawFeature_platform_path)
        if os.path.exists(ida_file):
            os.rename(ida_file, os.path.join(os.path.dirname(ida_file), old_name + '.ida'))
        #return os.basename(binary_file) + '.ida'
        #return True

#if __name__ == "__main__":
#    extractByIDAPro()