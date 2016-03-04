set arg1=%1
set arg2=%2
set arg3=%3
set arg4=%4
set arg5=%5
set arg6=%6
set arg7=%7
set arg8=%8
set arg9=%9
shift
set arg10=%9

@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
SET classpath=.
FOR %%i IN (lib/*.jar) DO (
    SET classpath=!classpath!;lib/%%i
)
SET jvmargs=-Xms256M -Xmx512M -XX:+UseParallelGC -XX:ParallelGCThreads=%NUMBER_OF_PROCESSORS%
SET mainClass=com.uinv.simple.PerfSender %arg1% %arg2% %arg3% %arg4% %arg5% %arg6% %arg7% %arg8% %arg9% %arg10%
java %jvmargs% -classpath %classpath% %mainClass%
echo %mainClass%
endlocal
