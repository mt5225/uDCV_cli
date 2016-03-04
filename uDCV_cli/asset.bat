@ECHO OFF
SETLOCAL ENABLEDELAYEDEXPANSION
SET classpath=.
FOR %%i IN (lib/*.jar) DO (
    SET classpath=!classpath!;lib/%%i
)
SET jvmargs=-Xms256M -Xmx512M -XX:+UseParallelGC -XX:ParallelGCThreads=%NUMBER_OF_PROCESSORS%
SET mainClass=com.uinv.simple.AssetSender %1 %2 %3 %4 %5
echo %mainClass%
java %jvmargs% -classpath %classpath% %mainClass%
endlocal