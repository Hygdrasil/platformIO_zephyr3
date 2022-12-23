## Zephyr 3.1 for Platformio 

This is based on "https://github.com/maxgerhardt/zephyr/tree/3.1.0_pio".
There are some tweeks to build a stm32 board in with Platformio

# Instructions 

 - delete <UserDirectory>/.platformio/packages/framework-zephyr
 - create new zephyr project with PlatformIO
 - append in plaformio.ini ```
platform_packages =
    framework-zephyr @ file:///run/media/kappy/d/programms/zephyr/zephyrPioBackup/framework-zephyr ```

# Further TODOS

- Test other Platforms than stm32
- fix main is build in ./src
- create better workaround to include the Library-Directories determined by PlatformIO
- 

