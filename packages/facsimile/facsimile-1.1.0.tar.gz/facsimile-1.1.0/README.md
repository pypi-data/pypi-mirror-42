
Facsimile
=========

Contents
--------

.toc 0


Introduction
------------

Facsimile is designed to create exact environment copies for local development
instances and deployed staging and production environments.

It supports multiple hosts, as well as multiple geographic regions.

You can use either by making a separate repo for a conglomerate, or by putting
definitions in config/facsimile.json

Internals
---------

### Definitions

* project : highest level of facsimile config, can contain other subprojects
* modules : project wide pieces, these are used to specify any sections that might be used between subprojects, or need separate passwords, etc

* instances :
  An instance is a set of machines, acting on concert to
  produce the full experience of using the platform. Another meaning of
  instance, in the deploy sense, is the set of configurations (including extra
  directory, instance.json, passwd.json generated file, etc) that allow the
  instance to be updated using the deploy scripts.

instance data is shared across projects

* targets : instances may be broken into different node types (e.g., frontend, database, app) called targets



rename:
An instance in a daemon
  level sense refers to the fact that we sometimes run more than one copy of the
  same code, off the same binary filename - usually with different arguments.
  For now we are doing this purely for an HA/LB or sharding perspective, but we may
  add further uses as well (such as hot spares - our existing HA is load
  balanced).

* definition : defines a project down to each instance, contains no state info. Definitions can be inherited infinately to avoid redefining anything
* state : configured and generated information that is instance specific.  For example, passwords, directories


rm:
per instance specific configuration for the deployment system to set up an install.
* environment : environment specific
* subinstance : sometimes, the 1:1 nature of the instance term becomes 1:2, or
  1:3.. or 1:n. For example, iceberg: we don't want to separately maintain the
  configurations for dev4.ch1's instance, dev0.ch0's instance, and
  dev5.ch1's instance separately, and we want to keep the passwords and
uiid in sync, for clarity.  However, there are subtle differences that should
be tracked. This is like an overlay, in a way - but it's for the whole
instance (in a deploy sense), not just one of the software packages.

### Directory Layout

* SRC/
  source checkouts - not separated by instance, assumes version tags are enough
* BUILD/
  out of source build trees, subdirectoried under $instance/
* define/
  instance definition files

* extra/
  extra files to be deployed
* tmpl/
  tmpl files to be rendered and then deployed


Templates
---------

Available structures are `instance` and `module`

config file templates should be kept with the source repository as much as possible, so changes are versioned along with the code that uses them


Modules
-------

name: module name
genconfig: should facs genarate a config for this
write_sql: <remove>

db::

Class Overrides
---------------

_init_<system>



Notes
-----

if project name matches a directory in deploy, rsync --delete is used to clean up the deploy
