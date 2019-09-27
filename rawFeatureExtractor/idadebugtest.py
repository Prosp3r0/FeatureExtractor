#import pydevd
#import idaapi

RDEBUG_HOST = 'localhost'
RDEBUG_PORT = 12321


def debug():
    import sys
    import pydevd
    print('++ debug()')
    RDEBUG_EGG="/Applications/PyCharm.app/Contents/debug-eggs/pycharm-debug.egg"
    sys.path.append(RDEBUG_EGG)
    pydevd.settrace(RDEBUG_HOST, port=RDEBUG_PORT, stdoutToServer=True, stderrToServer=True)


class MyPlugin_t(idaapi.plugin_t):
    flags = idaapi.PLUGIN_HIDE
    comment = "Test"
    help = ""
    wanted_name = "Test"
    wanted_hotkey = ""

    def init(self):
        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        print('+ run()')
        debug()
        #print "hello,hit break"

    def term(self):
        pass

def PLUGIN_ENTRY():
    print('hello ')
    return MyPlugin_t()

if __name__ == '__main__':
    PLUGIN_ENTRY()
    debug()
    print("hello,hit break")