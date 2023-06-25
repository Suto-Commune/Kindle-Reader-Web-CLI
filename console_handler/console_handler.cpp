#include <windows.h>

BOOL WINAPI ConsoleHandler(DWORD dwCtrlType) {
    if (dwCtrlType == CTRL_CLOSE_EVENT) {
        // 在这里执行关闭事件的处理逻辑
        // 返回 FALSE 以继续默认的处理，返回 TRUE 则忽略默认处理
        system("taskkill /f /im nginx.exe");
		system("taskkill /f /im java.exe");
        return FALSE;
    }
    return FALSE;
}

extern "C" __declspec(dllexport) void RegisterConsoleHandler() {
    // 注册关闭事件处理函数
    SetConsoleCtrlHandler(ConsoleHandler, TRUE);
}
