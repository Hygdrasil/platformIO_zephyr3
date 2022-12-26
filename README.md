## Zephyr 3.2 for Platformio 

This is based on "https://github.com/maxgerhardt/zephyr/tree/3.1.0_pio".
There are some tweeks to build a stm32 board in with Platformio

# Instructions 

 - delete <UserDirectory>/.platformio/packages/framework-zephyr
 - create new zephyr project with PlatformIO
 - append in plaformio.ini ```
platform_packages =
    framework-zephyr @ https://github.com/Hygdrasil/platformIO_zephyr3.git#piosupport32 ```
 - build the project
  PlatformIO should download this repo. 
  It will clone the other dependencies in a subdirectory. 
  This process may take a while.
# Further TODOS

- Test other Platforms than stm32
- Create usable version for raspberry pico
- fix main is build in ./src
- create better workaround to include the Library-Directories determined by PlatformIO
- 

