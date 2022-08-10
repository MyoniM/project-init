@ECHO off

@REM Dont call without at least a project name
IF "%1" == "" ( 
    ECHO Error, missing project information
    EXIT
)

@REM Set projectName and change the position back to 1
SET projectName=%1
SHIFT

@REM Give arguments a default value
SET template=none

@REM Get passed arguments
:getArguments
IF NOT "%1" == "" ( 
    IF "%1" == "-t" (
        SET template=%2
        SHIFT
    )
    SHIFT
    @REM Loop until all arguments are parsed
    GOTO :getArguments
)

ECHO Creating project %projectName% { options: -t %template% }
python create.py %projectName% %template%