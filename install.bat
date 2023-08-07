@echo off
setlocal
title Dependency Installer - DCS Server Toolkit

goto main

:main
    echo ###########################################
    echo # DCS Server Toolkit Dependency Installer #
    echo ###########################################
    echo.
    echo Warning: This tool will install Python packages through pip in order to allow
    echo DCS Server Toolkit to run properly. These packages can be uninstalled at any
    echo time if you choose to do so. This tool also uses/requires Python 3.10.8.
    echo.
    echo The following packages will be installed for the Python enviorment:
    echo colorama, dearpygui, requests, python-dotenv.
    echo.
    timeout /t 3 >nul
    echo Continue?
    echo.
    set /p "ch1=[Y/n]: "
    if /I "%ch1%"=="Y" (
        echo.
        goto check_python
    ) else (
        echo.
        echo OK! Terminating...
        echo.
        timeout /t 3 >nul
        exit
    )

:check_python
    set "PYTHON_VERSION="
    where python >nul 2>nul
    if %errorlevel% equ 0 (
        for /f "tokens=2 delims= " %%G in ('python --version 2^>^&1') do (
            set "PYTHON_VERSION=%%G"
        )
    )

    if "%PYTHON_VERSION%"=="3.10.8" (
        echo Python version 3.10.8 found!
        timeout /t 1 >nul
        goto install_libs
    ) else (
        title Dependency Installer - Incompatiable Python Version
        echo Python is not installed, or version 3.10.8 is not found. Please install it!
        echo.
        echo Override? You should not do this unless you know what you are doing! As any
        echo incompatiable version of Python will result in unstable code.
        echo.
        set /p "%ch2%=[Y/n]: "
        if /I "%ch2%" == "Y" (
            title Dependency Installer - DCS Server Toolkit - OVERRIDING
            goto install_libs
        ) else (
            echo.
            echo OK! Terminating...
            timeout /t 3 >nul
            exit
        )
    )

:install_libs
    echo Installing...
    timeout /t 2 >nul
    python -m pip install colorama
    python -m pip install dearpygui
    python -m pip install requests
    python -m pip install python-dotenv
    title Install Complete!
    echo.
    echo Complete. Press any key to close the window. IF ANY ERRORS HAVE OCCURED,
    echo PLEASE OPEN AN ISSUE ON THE GITHUB PAGE!
    pause >nul
    exit
endlocal