import traceback


class Log:
    __MAX_LEVEL = 4
    __MIN_LEVEL = 0
    __LOG_LEVEL = __MIN_LEVEL
    
    __TRACEBACK_ENABLED = False

    @staticmethod
    def log_trace_back():
        format_stack = traceback.format_stack()
        for i in range(0,len(format_stack)-3):
            print('\t'*i,format_stack[i].strip())

    @staticmethod
    def log_info(message : str):
        if Log.__TRACEBACK_ENABLED:
            Log.log_trace_back()
        if Log.__LOG_LEVEL < 1:
            print("INFO:[", message,"]")

    @staticmethod
    def log_warning(message : str ):
        if Log.__TRACEBACK_ENABLED:
            Log.log_trace_back()
        if Log.__LOG_LEVEL < 2:
            print("WARN:[", message,"]")

    @staticmethod
    def log_warning_2(message : str ):
        if Log.__TRACEBACK_ENABLED:
            Log.log_trace_back()
        if Log.__LOG_LEVEL < 3:
            print("*WARN:[", message,"]")

    @staticmethod
    def log_warning_3(message : str ):
        if Log.__TRACEBACK_ENABLED:
            Log.log_trace_back()
        if Log.__LOG_LEVEL < 4:
            print("**WARN:[", message,"]")

    @staticmethod
    def log_error(message : str):
        if Log.__TRACEBACK_ENABLED:
            Log.log_trace_back()
        if Log.__LOG_LEVEL < 5:
            print("\n***\nERROR:[", message, ']\n***\n')
            
    @staticmethod
    def set_log_level(level :int):
        Log.__LOG_LEVEL = max(Log.__MIN_LEVEL, min(level, Log.__MAX_LEVEL))

    @staticmethod
    def enable_trace_back(self):
        Log.__TRACEBACK_ENABLED = True

    @staticmethod
    def disable_trace_back(self):
        Log.__TRACEBACK_ENABLED = False