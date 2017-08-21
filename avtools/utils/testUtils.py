from processInfo import ProcessInfo

def test_process_info():
    pi = ProcessInfo()
    while pi.get_process_status("vlc.exe"):
        print "got it"
        continue

def get_multiple_pids():
    pi = ProcessInfo()
    print pi.get_multiple_process_id("svchost.exe")


if __name__ == '__main__':
    # test_process_info()
    get_multiple_pids()