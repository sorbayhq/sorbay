# Troubleshooting

## Installing Docker on MacOS.

**Q:** Where can I download Docker on MacOS?

**A:** You can download Docker Desktop on MacOS
[here](https://docs.docker.com/desktop/install/mac-install/).
But keep in mind that you need to download the correct `.dmg` file:

There are two:
* Docker Desktop for Mac with **Intel chip**.
* Docker Desktop for Mac with **Apple silicon**.

Choose the correct one according to your CPU on your Mac.

**Q:** I can't install Docker Desktop on MacOS Catalina (10.15),
what do I do?

**A:** Docker Desktop does not support MacOS Catalina (10.15) since
the version 4.16, however you can install 4.15 with [Homebrew](https://brew.sh/):

```bash
# Download Cask code for Docker Desktop 4.15.0,93002
curl https://raw.githubusercontent.com/Homebrew/homebrew-cask/1a83f3469ab57b01c0312aa70503058f7a27bd1d/Casks/docker.rb -O

# Install Docker Desktop from Cask Code
brew install --cask docker.rb

# OR

# if Docker Desktop is already installed then reinstall from Cask Code
brew reinstall --cask docker.rb 
```
(source: [StackOverflow, User:PJT](https://stackoverflow.com/a/75132333).)


## Errors when running the setup.

**Q:** When I run the `setup`-script, I get the following error:

```
debconf: delaying package configuration, since apt-utils is not installed
```

**A:** It's not really an error, and it's okay to ignore it.

**Q:** I am on Windows, and when I run the `setup`-script, I get the following error:

```
failed to get console mode for stdin: The handle is invalid.
```

**A:** It does not really cause any problem, you can ignore it.

**Q:** I get a lot python Traceback errors, and the last line of those Tracebacks look like this:

```
Failed to establish a new connection: [Errno -3] Temporary failure in name resolution
FATAL:  password authentication failed for user "sorbay"
```

**A:** You need to delete the old containers and their volumes on docker first before relaunching the setup.
When you delete the sorbay docker containrs and their volumes, then relaunching the setup, then it should work fine.