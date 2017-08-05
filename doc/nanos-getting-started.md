# Some Background for getting started developing for Nano S

### Relevent Repositories

**The development SDK:** contains header and library files for compiling
Nano S applications.  Located at:
[LedgerHQ/nanos-secure-sdk](https://github.com/LedgerHQ/nanos-secure-sdk).

**Python Tools for Ledger Blue and Nano S:** These contain tools for loading
apps onto the Nano S, and basic communication between Nano S and a python
interface on the computer.  Located at:
[LedgerHQ/blue-loader-python](https://github.com/LedgerHQ/blue-loader-python).

* The various python scripts are documented reasonably well at:
[Script Reference](https://ledger.readthedocs.io/projects/blue-loader-python/en/0.1.15/script_reference.html)

**Sample Apps:** These provide examples of basic operations on the Nano S
device. Located at:
[LedgerHQ/blue-sample-apps](https://github.com/LedgerHQ/blue-sample-apps).

### Documentation

Comprehensive developer documentation does not seem to be available yet (but
is expected).  Some very good general overview information for developers on
the way the BOLOS operating system and apps work and interact is located
here, however:
[Ledger Documentation Hub](http://ledger.readthedocs.io/en/latest/index.html).

A tutorial for building, installing, and running the Hello World sample app
is located here: (part of the docs mentioned above)
[Getting started](http://ledger.readthedocs.io/en/latest/nanos/setup.html).
It may be slightly out of date.

## Notes and tidbits

### Hardware memory and executable formats

Some basic info about the Nano S execution environment memory specs and
layout can be divined by looking at the linker scripts `script.ld` and
`script.ux.ld` in the SDK at
[LedgerHQ/nanos-secure-sdk](https://github.com/LedgerHQ/nanos-secure-sdk).

Note, what follows here comes from my *very fuzzy* understanding of the
linking and loading process and of the BOLOS architecture, and thus is
conjectural and could be very wrong, but... from these scripts it can be
devined, e.g., that UX code (I think this is BOLOS-provided library code
with different security priveledges that the app developer doesn't write,
but this is a pure guess) is loaded into a 2 kB window with a 768 byte
(wow!) stack size; and that application code is loaded into a 4 kB window
with another 768 byte stack.  Obviously, this is an *extrememly* tight
execution envirement.

Some wiggle-room is provided by the fact that there is also a read-only (to
the application) non-volatile flash ram window of 400 kB.  According to docs
at
[(Ledger docs)](http://ledger.readthedocs.io/en/latest/userspace/memory.html),
the executable code and const-declared variables are stored here, so that
the limited available volatile ram is not used up for this. And also, a
mechanism is provided to carve off *some* of the ro nvram as rw so that apps
can keep some persistant storage.

I actally have no idea how to read these linker scripts, so my conclusions
here are "as best I understand them."  There is some documentation on linker
scripts here:
[LD Scripts](https://sourceware.org/binutils/docs/ld/Scripts.html).

Another interesting oddity: the link script places "RAM-initialized
variables" into a memory region titled DISCARD and apparently mapped to a
non-existent region of address-space on the Nano.  This would have the
effect of just vaporizing ram-initialized variables altogether, I would
(naively??) think. It's weird, but I do think this is exactly what it does,
because the BOLOS documentation includes this warning:

> Initializers of global non-const variables (including NVRAM variables) are
> ignored. As such, this data must be initialized by application code.

So global data cannot have initializers.  Got it. Couldn't tell you why, but
got it. :thumbsup:.

Another point: BOLOS code, being embedded, makes frequent use of the
**volatile** keyword.  For some reminders of when/what/why `volatile` is
used, here are two links that came up in my google search:
* [How to Use C's volatile Keyword](https://barrgroup.com/Embedded-Systems/How-To/C-Volatile-Keyword)
* [Nine ways to break your systems code using volatile](https://blog.regehr.org/archives/28)

Ah, one reason for such frequent use of `volatile` is the TRY/CATCH macros
evidently can confuse the optimizer in some way.  For this reason, it is
recommended to declare variables that may be modified inside
try/catch/finally contexts as `volatile`.  Referenced in the docs here:
[Error Handling](http://ledger.readthedocs.io/en/latest/userspace/troubleshooting.html#error-handling).
