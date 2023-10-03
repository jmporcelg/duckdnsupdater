## DuckDNS IP Updater

This is a simple Python tool based on Tkinter, designed to periodically update the DNS for a dynamic IP address using the www.duckdns.org API. It is user-friendly and aimed at Windows users seeking a GUI to do that.

For the same result, the easiest method is to use a cron job that merely calls duckdns.org. This tool avoids having to create tasks in Windows and is appropriate for inexperienced users.

You need Python ~3.11, the code should be portable. However, some Linux distributions may require that you install a separate package for python3-Tkinter (even though it is part of the standard library).

When you utilize this tool, you have the ability to refresh a DuckDNS domain at your own discretion, or it will happen automatically every thirty minutes.

### Why?

I stumbled upon several websites with Java or C# tools, some of which did not even possess a valid SSL certificate, and thus I elected to release this straightforward solution instead of having to rely on random code I have no intention of reading.

### How to install?

You have several options, assuming you are on Windows but the same goes for Linux or any other OS that supports Python:

First option, run

`python3 setup.py install`.

Second alternative, install the tarball from GitHub i.e.

 `pip install https://github.com/jmporcelg/duckdnsupdater/raw/main/dist/duckdns-updater-1.0.0.tar.gz`.

You may opt to create a virtual environment first. After installation, you will have access to the `duckdns-updater.exe` and `duckdns-updater-script.pyw` binaries. You can add them to your PATH to make them accessible from any location.

### Screenshot

It could be worse, if you don't care for it, don't hesitate to simply access duckdns.org via curl ;-)

![Screenshot](/duckdnsupdater_example.png?raw=true "Screenshot")