# Frequently asked questions

## How to use IPv6 for Calibre's content server?

* https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1021175

> The embedded only listens on 0.0.0.0, aka AF_INET, aka IPv4.  This makes
> the content server quite unusable in the current internet, where IPv4
> connectivity gets sparingly, either by CG-NAT used by the provider or by
> IPv6-only environments.

You can change listening address from preferences window.
Change listening address from "Preferences"->"Sharing"->"Sharing over
the net"->"Advanced"->"The interface on which to listen for
connections:".
The default value is "0.0.0.0", but you can change to "::" for IPv6.
And use "127.0.0.1" or "::1" to limit access from localhost.

Here is document text for this option:
> The default is to listen on all available IPv4 interfaces. You can
> change this to, for example, "127.0.0.1" to only listen for connections
> from the local machine, or to "::" to listen to all incoming IPv6 and
> IPv4 connections.
