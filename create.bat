@ECHO off

@REM Dont call without at least a project name
IF "%1" == "" ( 
    ECHO Error, missing project information
    PAUSE
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

@REM the path you set in windows environment variables must be same with
@REM the path you set to the python file
@REM make sure to add white space inside quotes
python "C:\Users\YONI\Documents\Projects\My Projects\project-init\create.py" %projectName% %template%