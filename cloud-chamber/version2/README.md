# Activate Virtual Environment 
- Activating a Python virtual environment is a common practice in Python development. Make sure to run the scripts with python3.9 or more.

```shell
source env/bin/activate
```

# Execute in headless server
- Make sure to add the that the DISPLAY environment variable is set correctly. It should point to the display where the X Server is running. You can set it explicitly before running your application:
  ```shell
  export DISPLAY=:0
  ```

Error Message:
![Error Message](/images/error_display.png) 