# Eclipse Settings

## Setting Up An Eclipse Workspace

See TODO on how to setup an Eclipse workspace to work with foxBMS.

## Settings

### C/C++ Build
    Enviroment
        FOXCONDA:   ${HOMEDRIVE}\foxconda;
                    ${HOMEDRIVE}\foxconda\Lib;
                    ${HOMEDRIVE}\foxconda\Library\bin;
                    ${HOMEDRIVE}\foxconda\Scripts;
        PATH:       ${FOXCONDA};{path automatically set by eclipse}

### C/C++ General
    Paths and Symbols
        Includes:   ${HOMEDRIVE}\foxconda\Library\arm-none-eabi\include
                    ${HOMEDRIVE}\foxconda\Library\lib\gcc\arm-none-eabi\4.9.3\include
