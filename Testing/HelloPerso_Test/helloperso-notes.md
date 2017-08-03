# Notes on Hello Perso sample app.

Hello Perso is a sample app from the LedgerHQ repository
[blue-sample-apps](https://github.com/LedgerHQ/blue-sample-apps). It's
stated purpose is to be a "a simple application showing the UI and master
seed derivation."

### Compiling:

Compiles fine inside Docker image, as in the process described in the
[Getting Started](http://ledger.readthedocs.io/en/latest/nanos/setup.html)
tutorial (which takes you through the Hello World tutorial).

In extracting the hex-encoded compiled app from the docker container to my
local machine, I changed the app name as follows:

``` bash
sudo docker cp [container_id]:/home/blue-sample-apps/blue-app-helloperso/bin/app.hex perso-app.hex
```

I then loaded the app onto the Nano S using the following, and then
discovered a problem:

``` bash
python -m ledgerblue.loadApp --targetId 0x31100002 --apdu --fileName perso-app.hex --appName HelloPerso --appFlags 0x00 --icon ""
```

The problem: Hello Perso app requires the `APPLICATION_FLAG_GLOBAL_PIN`
permission flag. I had just copied and pasted my loadApp command line for
HelloWorld and changed the app name and image name.  But the `--appFlags`
argument needed to be changed to `--appFlags 0x40`.

Symptoms: With the wrong permissions set, even though the app was
successfuly loaded onto the device, it would freeze the Nano every
time I started the app, requiring a power-cycle to get back to the
dashboard.

The correct load command was:

``` bash
python -m ledgerblue.loadApp --targetId 0x31100002 --apdu --fileName perso-app.hex --appName HelloPerso --appFlags 0x40 --icon ""
```

### How to remove apps:

Problem Two: Repeating the loadApp() command with the correct flags failed
because the app already existed on the device.  It apparently won't
overwrite.  Thus I had to find a delete command, which fortunately is
referenced in the Makefile.  To manually delete the app, this is the
command:

``` bash
python -m ledgerblue.deleteApp --targetId 0x31100002 --appName HelloPerso
```

### Permission flags defined:

The `0x40` permission flag that was needed is defined by macro constant
`APPLICATION_FLAG_GLOBAL_PIN` in
[nanos-secure-sdk/include/os.h](https://github.com/LedgerHQ/nanos-secure-sdk/blob/master/include/os.h),
along with many other application flags.
