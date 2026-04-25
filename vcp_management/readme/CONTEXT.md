The aim of this module is to allow any community to import data from a version control system.

The system should be done in a way that is agnostic to the system and the connections are handled directly by specific modules.

## Definitions

### Hosts

Hosts are the origin of data.
Each host has a type that helps us know how to integrate with the system.
For example, on Github there is only one host (github.com).
However, in Gitlab there could be one for each instance that we are integrating too.

### Platform

We understand that a platform is an entity that can provide code and information to our Version Control Platform (VCP).
A platform could be an organization on Github (like OCA) or Gitlab for example.

### Repository

A repository is an origin of code. For example, [this repository](https://github.com/OCA/version-control-platform) could be a VCP repository.

### Requests

A request is what contributors do to propose new codes.
In Github it is a Pull request, however in Gitlab it is called Merge Request.

When a user makes a review on a request, it markes their resolution and some comments. 
That would correspond to Reviews and Comments.

### Rules

Inside a Platform or repository, we can apply some rules to get some basic statistics.
This rules are usually done by downloading the code locally and then it can give some basic information like number of lines of code.
