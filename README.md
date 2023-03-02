<p align="center" width="100%">
    <img width="33%" src="app/static/images/logo.png">
</p>

# Open Source Loom alternative

## About

Quickly create and share screen and camera recordings. The project comes in two parts: The backend service to store, organize and share recordings (this project) and a [client](https://github.com/sorbayhq/sorbay-client) for Windows, macOS and Linux to do the actual recordings.

## Setup

First, clone the repository to your local machine.
```shell
git clone https://github.com/sorbayhq/sorbay
cd sorbay
```

Next, run the following to set the project up for local development.

On macOS/Linux, make sure to have Docker and Docker-Compose installed.
And run:
```shell
sh setup/setup.sh
```

on Windows, make sure to have Docker Desktop installed.
And run
```batch
setup\setup.cmd
```

## Deployment

Once everything is set up, run the stack.
```shell
docker-compose up
```

The backend service should now be running at 
[http://localhost:8000/](http://localhost:8000/). On your first visit, you should be 
redirected to a "Sign In" page. Click on "register" at the bottom to create an account. 
You can now download the [client](https://github.com/sorbayhq/sorbay-client). Make sure to
point it to your local backend service at `http://localhost:8000/` during setup.

## Hosted Sorbay
We are currently working on a hosted backend service called 
[Sorbay Cloud](https://sorbay.io/), due to release in Q1 2023. Make sure to join the 
waitlist to get notified once we are ready.

Sorbay Cloud will allow you to get up and running in a couple of minutes. Instead of
deploying the backend service yourself, simply create an account, download the client and 
record your first video.

## State of the project

Sorbay is in its very early stages. Consider it an alpha that shouldn't be running in
production just yet. Our goal was to release Sorbay with a working minimalized featureset
and then add more and more features later on.

## Help, bugs & discussion
If you encounter any bugs up an issue in this repository. If you need help or want to chat about
the project, join our 
[Slack](https://join.slack.com/t/sorbay/shared_invite/zt-1m3nio46o-ERrjXDNgSLr_ToklzUfFtw) channel.
