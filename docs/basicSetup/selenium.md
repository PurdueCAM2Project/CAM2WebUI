# Selenium Test Environment

Selenium automates browsers. It is for automating web applications for testing purposes. More details of selenium web driver can be found at [Selenium HQ](http://www.seleniumhq.org/)

## Download Python Selenium

If you have pip on your system, you can simply install or upgrade the Python bindings:

```
pip install -U selenium
```

Alternately, you can download the source distribution from PyPI [Selenium PYPI](https://pypi.python.org/pypi/selenium), unarchive it, and run:

```
python setup.py install
```

Note: both of the methods described above install selenium as a system-wide package That will require administrative/root access to their machine. 


## Download Firefox/Chrome driver

Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the selenium can run.

Failure to observe this step will give you an error selenium.common.exceptions.WebDriverException: Message: ‘xxxdriver’ executable needs to be in PATH.

Here I will use the Chrome driver as the example. The installation of the Firefox or Safari driver is similar to the ones of Chrome driver.

1. Visit [Selenium PYPI](https://pypi.python.org/pypi/selenium) and scroll down to the driver part. You can see the url links to those common web browsers. Click on the link of Chrome and link to the Chrome driver page.


2. Choose the latest version of Chrome driver in the page and download the zip file of the driver depending on your system. Remember the folder where you download the zip file. 

3. Open the terminal and change directory to the one which you download the driver zip file. Unzip chrome driver using the following command. Here I am using linux 64 bit system. If you are using some other systems, you will unzip a different zip file. 

```
unzip chromedriver_linux64.zip
```

4. Use sudo command to move your unzipped chromedriver to the usr/bin/ directory. Change the mode of chromedriver to make it executable.

```
sudo mv chromedriver /usr/bin
sudo chmod a+x /usr/bin/chromedriver
```

## Install X virtual framebuffer(xvfb)

Xvfb (short for X virtual framebuffer) is an in-memory display server for UNIX-like operating system (e.g., Linux). It enables you to run graphical applications without a display (e.g., browser tests on a CI server) while also having the ability to take screenshots.

You can simply install xvfb using command

```
sudo apt-get install xvfb
```

## Ready to Write Selenium Test

Congratulations, you have successfully built the selenium test environment. In this [guide](https://purduecam2project.github.io/CAM2WebUI/test/test.html), you will learn about how to create selenium tests and what are the test files. 
