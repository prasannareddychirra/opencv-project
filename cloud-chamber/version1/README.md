# Execute in headless server
- Make sure to add the that the DISPLAY environment variable is set correctly. It should point to the display where the X Server is running. You can set it explicitly before running your application:
  ```shell
  export DISPLAY=:0
