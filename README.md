<p align="center" width="100%">
    <img width="33%" src="app/static/images/logo.png">
</p>

# Open source asynchronous video communication tool

Quickly create and share screen and camera recordings. 

The project comes in two parts: 

- The backend service to store, organize and share recordings (this project)
- [Client](https://github.com/sorbayhq/sorbay-client) for Windows, macOS and Linux(soon) to do the actual recordings

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
docker compose up
```

The backend service should now be running at 
[http://localhost:8000/](http://localhost:8000/). On your first visit, you should be 
redirected to a "Sign In" page. Click on "register" at the bottom to create an account. 
You can now download the [client](https://github.com/sorbayhq/sorbay-client). Make sure to
point it to your local backend service at `http://localhost:8000/` during setup.

## Leave a star
Consider leaving a star on this Github repository if you think what we are building is 
useful or might be useful at some point. We are in our very early stages and we don't
collect any telemetry. Getting a star is the only viable metric for us to gauge interest.

## Hosted Sorbay
We are currently working on a hosted backend service called 
[Sorbay Cloud](https://sorbay.io/), due to release in Q2 2023. Make sure to join the 
waitlist to get notified once we are ready.

Sorbay Cloud will allow you to get up and running in a couple of minutes. Instead of
deploying the backend service yourself, simply create an account, download the client and 
record your first video.

## State of the project

Sorbay is in its very early stages. Consider it an alpha that shouldn't be running in
production just yet. We are currently working on additional features and these will be influenced by feedback from the community.

## Help, bugs & discussion
If you encounter any bugs open up an issue in this repository. If you need help or want to chat about
the project, join our 
[Slack](https://join.slack.com/t/slack-oso6527/shared_invite/zt-1qd8gm543-KGdb5gD4WqikZEKEk8sSTA) channel.
