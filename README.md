## Zephyr 3.1 for Platformio 

This is based on "https://github.com/maxgerhardt/zephyr/tree/3.1.0_pio".
There are some tweeks to build a stm32 board in with Platformio

# Instructions 

 - delete <UserDirectory>/.platformio/packages/framework-zephyr
 - create new zephyr project with PlatformIO
 - append in plaformio.ini ```
platform_packages =
    framework-zephyr @ https://github.com/Hygdrasil/platformIO_zephyr3.git ```
 - build the project
  PlatformIO should download this repo. 
  It will clone the other dependencies in a subdirectory. 
  This process may take a while.

# get Rasperry PI PICO running
- run a build
- in `framework-zephyr/modules/hal` add this patch (https://github.com/zephyrproject-rtos/zephyr/pull/46616/commits/30736644c61ff9a6a52ea052f453da58bbda8f33#diff-f3ebf5014b5186f321b405640bb799a6fa92e57b79439deb24d730c3fedcd58c)
- clean your project
- build your project again
- press `BOOTSEL` on the pico and plug it in
- on the flash drive copy the `.pio/build/pico/firmware.uf2` 
Disclamer serial output is not working at the moment. 
TODO auto generate the needet file and update to a later version
# Further TODOS

- Test other Platforms than stm32
- fix main is build in ./src
- create better workaround to include the Library-Directories determined by PlatformIO
- 

