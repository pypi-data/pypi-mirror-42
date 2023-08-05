# DOTDROP

[![Build Status](https://travis-ci.org/deadc0de6/dotdrop.svg?branch=master)](https://travis-ci.org/deadc0de6/dotdrop)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)
[![Coverage Status](https://coveralls.io/repos/github/deadc0de6/dotdrop/badge.svg?branch=master)](https://coveralls.io/github/deadc0de6/dotdrop?branch=master)
[![PyPI version](https://badge.fury.io/py/dotdrop.svg)](https://badge.fury.io/py/dotdrop)
[![AUR](https://img.shields.io/aur/version/dotdrop.svg)](https://aur.archlinux.org/packages/dotdrop)
[![Python](https://img.shields.io/pypi/pyversions/dotdrop.svg)](https://pypi.python.org/pypi/dotdrop)

*Save your dotfiles once, deploy them everywhere*

[Dotdrop](https://github.com/deadc0de6/dotdrop)  makes the management of dotfiles between different hosts easy.
It allows to store your dotfiles on git and automagically deploy
different versions of the same file on different setups.

It also allows to manage different *sets* of dotfiles.
For example you can have a set of dotfiles for your home laptop and
a different set for your office desktop. Those sets may overlap and different
versions of the same dotfiles can be deployed on different predefined *profiles*.
Or you may have a main set of dotfiles for your
everyday's host and a sub-set you only need to deploy to temporary
hosts (cloud VM, etc) that may be using
a slightly different version of some of the dotfiles.

Features:

* Sync once every dotfile on git for different usages
* Allow dotfiles templating by leveraging [jinja2](http://jinja.pocoo.org/)
* Dynamically generated dotfile content with variables
* Comparison between local and stored dotfiles
* Handling multiple profiles with different sets of dotfiles
* Easy import dotfiles
* Handle files and directories
* Allow to symlink dotfiles
* Associate an action to the deployment of specific dotfiles
* Associate transformations for storing encrypted dotfiles
* Provide different solutions for handling dotfiles containing sensitive information

Check also the [blog post](https://deadc0de.re/articles/dotfiles.html), the [example](#example) or how [people are using dotdrop](#people-using-dotdrop) for more.

Quick start:
```bash
mkdir dotfiles && cd dotfiles
git init
git submodule add https://github.com/deadc0de6/dotdrop.git
sudo pip3 install -r dotdrop/requirements.txt
./dotdrop/bootstrap.sh
./dotdrop.sh --help
```

A mirror of this repository is available on gitlab under <https://gitlab.com/deadc0de6/dotdrop>.

## Why dotdrop ?

There exist many tools to manage dotfiles however not
many allow to deploy different versions of the same dotfile
on different hosts. Moreover dotdrop allows to specify the
set of dotfiles that need to be deployed on a specific profile.

See the [example](#example) for a concrete example on
why [dotdrop](https://github.com/deadc0de6/dotdrop) rocks.

---

**Table of Contents**

* [Installation](#installation)
* [Usage](#usage)
* How to
  * [Install dotfiles](#install-dotfiles)
  * [Compare dotfiles](#compare-dotfiles)
  * [Import dotfiles](#import-dotfiles)
  * [List profiles](#list-profiles)
  * [List dotfiles](#list-dotfiles)
  * [Use actions](#use-actions)
  * [Use transformations](#use-transformations)
  * [Update dotdrop](#update-dotdrop)
  * [Update dotfiles](#update-dotfiles)
  * [Store sensitive dotfiles](#store-sensitive-dotfiles)
  * [Symlink dotfiles](#symlink-dotfiles)
* [Config](#config)
* [Templating](#templating)
  * [Available variables](#available-variables)
  * [Available methods](#available-methods)
  * [Dynamic dotfile paths](#dynamic-dotfile-paths)
  * [Dynamic actions](#dynamic-actions)
  * [Dotdrop header](#dotdrop-header)
* [Example](#example)
* [User tricks](#user-tricks)
* [People using dotdrop](#people-using-dotdrop)

# Installation

There are two ways of installing and using dotdrop, either [as a submodule](#as-a-submodule)
to your dotfiles git tree or system-wide with [pypi](https://pypi.org/project/dotdrop/).

Having dotdrop as a submodule guarantees that anywhere your are cloning your
dotfiles git tree from you'll have dotdrop shipped with it. It is the recommended way.

Below instructions show how to install dotdrop as a submodule. For alternative
installation instructions (with virtualenv, pypi, etc), see the
[wiki installation page](https://github.com/deadc0de6/dotdrop/wiki/installation).

Dotdrop is also available on aur:
* stable: https://aur.archlinux.org/packages/dotdrop/
* git version: https://aur.archlinux.org/packages/dotdrop-git/

## As a submodule

The following will create a git repository for your dotfiles and
keep dotdrop as a submodule:
```bash
$ mkdir dotfiles; cd dotfiles
$ git init
$ git submodule add https://github.com/deadc0de6/dotdrop.git
$ sudo pip3 install -r dotdrop/requirements.txt
$ ./dotdrop/bootstrap.sh
$ ./dotdrop.sh --help
```

For MacOS users, make sure to install `realpath` through homebrew
(part of *coreutils*).

Using this solution will need you to work with dotdrop by
using the generated script `dotdrop.sh` at the root
of your dotfiles repository.

To ease the use of dotdrop, it is recommended to add an alias to it in your
shell with the config file path, for example
```
alias dotdrop=<absolute-path-to-dotdrop.sh> --cfg=<path-to-your-config.yaml>'
```

Finally import your dotfiles as described [below](#usage).

# Usage

If starting fresh, the `import` command of dotdrop
allows to easily and quickly get a running setup.

Install dotdrop on one of your host and then import any dotfiles you want dotdrop to
manage (be it a file or a directory):
```bash
$ dotdrop import ~/.vimrc ~/.xinitrc
```

Dotdrop does two things:

* Copy the dotfiles in the *dotpath* directory
* Create the entries in the *config.yaml* file

Commit and push your changes.

Then go to another host where your dotfiles need to be managed as well,
clone the previously setup git tree
and compare local dotfiles with the ones stored by dotdrop:
```bash
$ dotdrop list
$ dotdrop compare --profile=<other-host-profile>
```

Then adapt any dotfile using the [template](#template) feature (if needed)
and set a new profile for the current host by simply adding lines in
the config files, for example:

```yaml
...
profiles:
  host1:
    dotfiles:
    - f_vimrc
    - f_xinitrc
  host2:
    dotfiles:
    - f_vimrc
...
```

When done, you can install your dotfiles using

```bash
$ dotdrop install
```

That's it, a single repository with all your dotfiles for your different hosts.

For more options see `dotdrop --help`.

For easy deployment the default profile used by dotdrop reflects the
hostname of the host on which it runs. It can be changed either with the
`--profile` switch or by defining the `DOTDROP_PROFILE` environment variable.

## Install dotfiles

Simply run
```bash
$ dotdrop install
```

## Compare dotfiles

Compare local dotfiles with the ones stored in dotdrop:
```bash
$ dotdrop compare
```

The diffing is done by `diff` in the backend, one can provide specific
options to diff using the `-o` switch.

It is possible to add patterns to ignore when using `compare` for example
when a directory is managed by dotdrop and might contain temporary files
that don't need to appear in the output of compare.
Either use the command line switch `-i --ignore` or add a line in the dotfile
directly in the `cmpignore` entry (see [Config](#config)).
The ignore pattern must follow Unix shell-style wildcards like for example `*/path/file`.
Make sure to quote those when using wildcards in the config file.

It is also possible to install all dotfiles for a specific profile
in a temporary directory in order to manually compare them with
the local version by using `install` and the `-t` switch.

## Import dotfiles

Dotdrop allows to import dotfiles directly from the
filesystem. It will copy the dotfile and update the
config file automatically.

For example to import `~/.xinitrc`
```bash
$ dotdrop import ~/.xinitrc
```

You can control how the dotfile key is generated in the config file
with the option `longkey` (per default to *false*).

Two formats are available:

  * *short format* (default): take the shortest unique path
  * *long format*: take the full path

For example `~/.config/awesome/rc.lua` gives

  * `f_rc.lua` in the short format
  * `f_config_awesome_rc.lua` in the long format

Importing `~/.mutt/colors` and then `~/.vim/colors` will result in

  * `d_colors` and `d_vim_colors` in the short format
  * `d_mutt_colors` and `d_vim_colors` in the long format

## List profiles

```bash
$ dotdrop list
```

Dotdrop allows to choose which profile to use
with the `--profile` switch if you use something
else than the default (the hostname).

The default profile can also be changed by defining the
`DOTDROP_PROFILE` environment variable.

## List dotfiles

The following command lists the different dotfiles
configured for a specific profile:

```bash
$ dotdrop listfiles --profile=<some-profile>
```

For example:
```
Dotfile(s) for profile "some-profile":
f_vimrc (file: "vimrc", link: nolink)
	-> ~/.vimrc
f_dunstrc (file: "config/dunst/dunstrc", link: nolink)
	-> ~/.config/dunst/dunstrc
```

By using the `-T --template` switch, only the dotfiles that
are using [jinja2](http://jinja.pocoo.org/) directives are listed.

It is also possible to list all files related to each dotfile entries
by invoking the `detail` command, for example:
```bash
$ dotdrop detail
dotfiles details for profile "some-profile":
f_tmux.conf (dst: "~/.tmux.conf", link: nolink)
        -> /home/user/dotfiles/tmux.conf (template:no)
f_vimrc (dst: "~/.vimrc", link: nolink)
        -> /home/user/dotfiles/vimrc (template:no)
```

This is especially useful when the dotfile entry is a directory
and one wants to have information on the different files (is it
a templated file, etc).

## Use actions

It is sometimes useful to execute some kind of action
when deploying a dotfile. For example let's consider
[Vundle](https://github.com/VundleVim/Vundle.vim) is used
to manage vim's plugins, the following action could
be set to update and install the plugins when `vimrc` is
deployed:

```yaml
actions:
  vundle: vim +VundleClean! +VundleInstall +VundleInstall! +qall
config:
  backup: true
  create: true
  dotpath: dotfiles
dotfiles:
  f_vimrc:
    dst: ~/.vimrc
    src: vimrc
    actions:
      - vundle
profiles:
  home:
    dotfiles:
    - f_vimrc
```

Thus when `f_vimrc` is installed, the command
`vim +VundleClean! +VundleInstall +VundleInstall! +qall` will
be executed.

Sometimes, you may even want to execute some action prior to deploying a dotfile.
Let's take another example with
[vim-plug](https://github.com/junegunn/vim-plug):

```yaml
actions:
  pre:
    vim-plug-install: test -e ~/.vim/autoload/plug.vim || (mkdir -p ~/.vim/autoload; curl
      -fLo ~/.vim/autoload/plug.vim https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim)
  vim-plug: vim +PlugInstall +qall
config:
  backup: true
  create: true
  dotpath: dotfiles
dotfiles:
  f_vimrc:
    dst: ~/.vimrc
    src: vimrc
    actions:
       - vim-plug-install
       - vim-plug
profiles:
  home:
    dotfiles:
    - f_vimrc
```

This way, we make sure [vim-plug](https://github.com/junegunn/vim-plug)
is installed prior to deploying the `~/.vimrc` dotfile.

You can also define `post` actions like this:

```yaml
actions:
  post:
    some-action: echo "Hello, World!" >/tmp/log
```

If you don't specify neither `post` nor `pre`, the action will be executed
after the dotfile deployment (which is equivalent to `post`).
Actions cannot obviously be named `pre` or `post`.

Actions can even be parameterized. For example:
```yaml
actions:
  echoaction: echo '{0}' > {1}
config:
  backup: true
  create: true
  dotpath: dotfiles
dotfiles:
  f_vimrc:
    dst: ~/.vimrc
    src: vimrc
    actions:
      - echoaction "vim installed" /tmp/mydotdrop.log
  f_xinitrc:
    dst: ~/.xinitrc
    src: xinitrc
    actions:
      - echoaction "xinitrc installed" /tmp/myotherlog.log
profiles:
  home:
    dotfiles:
    - f_vimrc
    - f_xinitrc
```

The above will execute `echo 'vim installed' > /tmp/mydotdrop.log` when
vimrc is installed and `echo 'xinitrc installed' > /tmp/myotherlog.log'`
when xinitrc is installed.

## Use transformations

There are two types of transformations available:

* **read transformations**: used to transform dotfiles before they are installed ([Config](#config) key *trans*)
  * Used for commands `install` and `compare`
  * They have two arguments:
    * **{0}** will be replaced with the dotfile to process
    * **{1}** will be replaced with a temporary file to store the result of the transformation

* **write transformations**: used to transform files before updating a dotfile ([Config](#config) key *trans_write*)
  * Used for command `update`
  * They have two arguments:
    * **{0}** will be replaced with the file path to update the dotfile with
    * **{1}** will be replaced with a temporary file to store the result of the transformation

A typical use-case for transformations is when dotfiles need to be
stored encrypted.

Here's an example of part of a config file to use PGP encrypted dotfiles:
```yaml
dotfiles:
  f_secret:
    dst: ~/.secret
    src: secret
    trans: gpg
trans:
  gpg: gpg2 -q --for-your-eyes-only --no-tty -d {0} > {1}
```

The above config allows to store the dotfile `~/.secret` encrypted in the *dotpath*
directory and uses `gpg2` to decrypt it when `install` is run.

See the wiki page for a walkthrough on how to deploy this solution as well
as more information on transformations:
[wiki transformation page](https://github.com/deadc0de6/dotdrop/wiki/transformations).

Note that transformations cannot be used if the dotfiles is to be linked (when `link: true`).

## Update dotdrop

If used as a submodule, update it with
```bash
$ git submodule update --init --recursive
$ git submodule update --remote dotdrop
```

You will then need to commit the changes with
```bash
$ git add dotdrop
$ git commit -m 'update dotdrop'
$ git push
```

Or if installed through pypi:
```bash
$ sudo pip3 install dotdrop --upgrade
```

## Update dotfiles

Dotfiles managed by dotdrop can be updated using the `update` command. When updating, only
dotfiles that have differences with the stored version are updated.
A confirmation is requested from the user before any overwrite/update unless the
`-f --force` switch is used.

Either provide the path of the file containing the new version of the dotfile or
provide the dotfile key to update (as found in the config file) along with the `-k --key` switch.
When using the `-k --key` switch and no key is provided, all dotfiles for that profile are updated.
```bash
# update by path
$ dotdrop update ~/.vimrc

# update by key with the --key switch
$ dotdrop update --key f_vimrc
```

It is possible to ignore files to update using unix patterns by providing those
either through the switch `-i --ignore` or as part of the dotfile under the
key `upignore` (see [Config](#config)).
The ignore pattern must follow Unix shell-style wildcards like for example `*/path/file`.
Make sure to quote those when using wildcards in the config file.
```yaml
dotfiles:
  d_vim
    dst: ~/.vim
    src: vim
    upignore:
    - "*/undo-dir"
    - "*/plugged"
```

There are two cases when updating a dotfile:

**The dotfile doesn't use [templating](#template)**

The new version of the dotfile is copied to the *dotpath* directory and overwrites
the old version. If git is used to version the dotfiles stored by dotdrop, the git command
`diff` can be used to view the changes.

```bash
$ dotdrop update ~/.vimrc
$ git diff
```

**The dotfile uses [templating](#template)**

The dotfile must be manually updated, three solutions can be used to identify the
changes to apply to the template:

* Use dotdrop's `compare` command
```bash
# use compare to identify change(s)
$ dotdrop compare --file=~/.vimrc
```

* Call `update` with the `-P --show-patch` switch that will provide with an ad-hoc solution
  to manually patch the template file using a temporary generated version of the template
  (this isn't a bullet proof solution and might need manual checking)
```bash
# get an ad-hoc solution to manually patch the template
$ dotdrop update --show-patch ~/.vimrc
[WARN] /home/user/dotfiles/vimrc uses template, update manually
[WARN] try patching with: "diff -u /tmp/dotdrop-sbx6hw0r /home/user/.vimrc | patch /home/user/dotfiles/vimrc"
```

* Install the dotfiles to a temporary directory (using the `install` command and the
  `-t` switch) and compare the generated dotfile with the local one.
```bash
# use install to identify change(s)
$ dotdrop install -t
Installed to tmp /tmp/dotdrop-6ajz7565
$ diff ~/.vimrc /tmp/dotdrop-6ajz7565/home/user/.vimrc
```

It is also possible to install only specific dotfiles by providing their keys
in the command line. For example for a dotfile having a key `f_zshrc` in the config file.
```bash
$ dotdrop install -t f_zshrc
```

## Store sensitive dotfiles

Two solutions exist, the first one using an unversioned file (see [Environment variables](#environment-variables))
and the second using transformations (see [Transformations](#use-transformations)).

## Symlink dotfiles

Dotdrop offers two ways to symlink dotfiles. The first simply links `dst` to
`src`. To enable it, simply set `link: true` under the dotfile entry in the
config file.

The second symlink method allows to have every files/directories under `src` to
be symlinked in `dst`. It is enabled by setting `link_children: true`.

### Link children

This feature can be very useful for dotfiles when you don't want the entire
directory to be symlink but still want to keep a clean config files (with a
limited number of entries). A good example of its use is when managing `~/.vim` with dotdrop.

Here's what it looks like when using `link: true`.
```yaml
config:
  dotpath: dotfiles
vim:
  dst: ~/.vim
  src: vim
  link: true
```

The top directory `~/.vim` is symlinked to the *dotpath* location
```bash
$ readlink ~/.vim
~/.dotfiles/vim/
$ ls ~/.dotfiles/vim/
after  autoload  plugged  plugin  snippets  spell  swap  vimrc
```

As a result, all files under `~/.vim` will be managed by
dotdrop (including unwanted directories like `spell`, `swap`, etc).

A cleaner solution is to use `link_children` which allows to only symlink specific
files under the dotfile directory. Let's say only `after`, `plugin`, `snippets`, and `vimrc`
need to be managed in dotdrop. `~/.vim` is imported in dotdrop, cleaned off all unwanted
files and directories and then the `link_children` entry is set to `true` in the config file.
```yaml
config:
  dotpath: dotfiles
vim:
  dst: ~/.vim/
  src: vim
  link_children: true
```

Now all children of the `vim` dotfile's directory in the *dotpath* will be symlinked under `~/.vim/`
without affecting the rest of the local files, keeping the config file clean
and all unwanted files only on the local system.
```bash
$ readlink -f ~/.vim
~/.vim
$ tree -L 1 ~/.vim
~/.vim
├── after -> ~/.dotfiles/vim/after
├── autoload
├── plugged
├── plugin -> ~/.dotfiles/vim/plugin
├── snippets -> ~/.dotfiles/vim/snippets
├── spell
├── swap
└── vimrc -> ~/.dotfiles/vim/vimrc
```

### Templating symlinked dotfiles

For dotfiles not using any templating directives, those are directly linked
to dotdrop's `dotpath` directory (see [Config](#config)).
When using templating directives, the dotfiles are first installed into
`workdir` (defaults to *~/.config/dotdrop*, see [Config](#config))
and then symlinked there. This applies to both dotfiles with `link: true` and
`link_children: true`.

For example
```bash
# with template
/home/user/.xyz -> /home/user/.config/dotdrop/.xyz

# without template
/home/user/.xyz -> /home/user/dotfiles/xyz
```

# Config

The config file (defaults to *config.yaml*) is a yaml file containing
the following entries:

* **config** entry: contains settings for the deployment
  * `backup`: create a backup of the dotfile in case it differs from the
    one that will be installed by dotdrop (default *true*)
  * `create`: create directory hierarchy when installing dotfiles if
    it doesn't exist (default *true*)
  * `dotpath`: path to the directory containing the dotfiles to be managed
    by dotdrop (absolute path or relative to the config file location)
  * `banner`: display the banner (default *true*)
  * `longkey`: use long keys for dotfiles when importing (default *false*)
  * `keepdot`: preserve leading dot when importing hidden file in the `dotpath` (default *false*)
  * `link_by_default`: when importing a dotfile set `link` to that value per default (default *false*)
  * `workdir`: path to the directory where templates are installed before being symlinked when using `link`
    (absolute path or relative to the config file location, defaults to *~/.config/dotdrop*)
  * `showdiff`: on install show a diff before asking to overwrite (see `--showdiff`) (default *false*)
  * `ignoreempty`: do not deploy template if empty (default *false*)

* **dotfiles** entry: a list of dotfiles
  * `dst`: where this dotfile needs to be deployed (can use `variables` and `dynvariables`, make sure to quote).
  * `src`: dotfile path within the `dotpath` (can use `variables` and `dynvariables`, make sure to quote).
  * `link`: if true dotdrop will create a symlink instead of copying (default *false*).
  * `link_children`: if true dotdrop will create a symlink for each file under `src` (default *false*).
  * `cmpignore`: list of pattern to ignore when comparing (enclose in quotes when using wildcards).
  * `upignore`: list of pattern to ignore when updating (enclose in quotes when using wildcards).
  * `actions`: list of action keys that need to be defined in the **actions** entry below.
  * `trans`: transformation key to apply when installing this dotfile (must be defined in the **trans** entry below).
  * `trans_write`: transformation key to apply when updating this dotfile (must be defined in the **trans_write** entry below).
  * `ignoreempty`: if true empty template will not be deployed (defaults to the value of `ignoreempty` above)

```yaml
  <dotfile-key-name>:
    dst: <where-this-file-is-deployed>
    src: <filename-within-the-dotpath>
    # Optional
    (link|link_children): <true|false>
    ignoreempty: <true|false>
    cmpignore:
      - "<ignore-pattern>"
    upignore:
      - "<ignore-pattern>"
    actions:
      - <action-key>
    trans: <transformation-key>
    trans_write: <transformation-key>
```

* **profiles** entry: a list of profiles with the different dotfiles that
  need to be managed
  * `dotfiles`: the dotfiles associated to this profile
  * `include`: include all dotfiles from another profile (optional)
  * `variables`: profile specific variables (see [Variables](#variables))
  * `dynvariables`: profile specific interpreted variables (see [Interpreted variables](#interpreted-variables))

```yaml
  <some-name-usually-the-hostname>:
    dotfiles:
    - <some-dotfile-key-name-defined-above>
    - <some-other-dotfile-key-name>
    - ...
    # Optional
    include:
    - <some-other-profile>
    - ...
    variables:
      <name>: <value>
    dynvariables:
      <name>: <value>
```

* **actions** entry (optional): a list of action (see [Use actions](#use-actions))

```
  <action-key>: <command-to-execute>
```

* **trans** entry (optional): a list of transformations (see [Use transformations](#use-transformations))

```
   <trans-key>: <command-to-execute>
```

* **trans_write** entry (optional): a list of write transformations (see [Use transformations](#use-transformations))

```
   <trans-key>: <command-to-execute>
```

* **variables** entry (optional): a list of template variables (see [Variables](#variables))

```
  <variable-name>: <variable-content>
```

* **dynvariables** entry (optional): a list of interpreted variables (see [Interpreted variables](#interpreted-variables))

```
  <variable-name>: <shell-oneliner>
```

## All dotfiles for a profile

To use all defined dotfiles for a profile, simply use
the keyword `ALL`.

For example:
```yaml
dotfiles:
  f_xinitrc:
    dst: ~/.xinitrc
    src: xinitrc
  f_vimrc:
    dst: ~/.vimrc
    src: vimrc
profiles:
  host1:
    dotfiles:
    - ALL
  host2:
    dotfiles:
    - f_vimrc
```

## Include dotfiles from another profile

If one profile is using the entire set of another profile, one can use
the `include` entry to avoid redundancy.

For example:
```yaml
profiles:
  host1:
    dotfiles:
      - f_xinitrc
    include:
      - host2
  host2:
    dotfiles:
      - f_vimrc
```
Here profile *host1* contains all the dotfiles defined for *host2* plus `f_xinitrc`.

## Ignore empty template

It is possible to avoid having an empty rendered template being
deployed by setting the `ignoreempty` entry to *true*. This can be set
globally for all dotfiles or only for specific dotfiles.
For more see the [Config](#config).

# Templating

Dotdrop leverage the power of [jinja2](http://jinja.pocoo.org/) to handle the
templating of dotfiles. See [jinja2 template doc](http://jinja.pocoo.org/docs/2.9/templates/)
or the [example section](#example) for more information on how to template your dotfiles.

Note that dotdrop uses different delimiters than
[jinja2](http://jinja.pocoo.org/)'s defaults:

* block start = `{%@@`
* block end = `@@%}`
* variable start = `{{@@`
* variable end = `@@}}`
* comment start = `{#@@`
* comment end = `@@#}`

## Available variables

Following template variables are available:

* `{{@@ profile @@}}` contains the profile provided to dotdrop.
* `{{@@ env['MY_VAR'] @@}}` contains environment variables (see [Environment variables](#environment-variables)).
* `{{@@ header() @@}}` insert dotdrop header (see [Dotdrop header](#dotdrop-header)).
* defined variables (see [Variables](#variables))
* interpreted variables (see [Interpreted variables](#interpreted-variables))

All variables are recursively evaluated what means that
a config like the below
```yaml
variables:
  var1: "var1"
  var2: "{{@@ var1 @@}} var2"
  var3: "{{@@ var2 @@}} var3"
  var4: "{{@@ dvar4 @@}}"
dynvariables:
  dvar1: "echo dvar1"
  dvar2: "{{@@ dvar1 @@}} dvar2"
  dvar3: "{{@@ dvar2 @@}} dvar3"
  dvar4: "echo {{@@ var3 @@}}"
```

will result in the following available variables
* var3: `var1 var2 var3`
* dvar3: `dvar1 dvar2 dvar3`
* var4: `echo var1 var2 var3`
* dvar4: `var1 var2 var3`

## Variables

Variables can be added in the config file under the `variables` entry.
The variables added there are directly reachable in any templates.

For example in the config file:
```yaml
variables:
  var1: some variable content
  var2: some other content
```

These can then be used in any template with
```
{{@@ var1 @@}}
```

Profile variables will take precedence over globally defined variables what
means that you could do something like this:
```yaml
variables:
  git_email: home@email.com
dotfiles:
  f_gitconfig:
    dst: ~/.gitconfig
    src: gitconfig
profiles:
  work:
    dotfiles:
    - f_gitconfig
    variables:
      git_email: work@email.com
  private:
    dotfiles:
    - f_gitconfig
```

## Interpreted variables

It is also possible to have *dynamic* variables in the sense that their
content will be interpreted by the shell before being replaced in the templates.

For example:
```yaml
dynvariables:
  dvar1: head -1 /proc/meminfo
  dvar2: "echo 'this is some test' | rev | tr ' ' ','"
  dvar3: /tmp/my_shell_script.sh
```

These can be used as any variables in the templates
```
{{@@ dvar1 @@}}
```

As for variables (see [Variables](#variables)) profile dynvariables will take
precedence over globally defined dynvariables.

## Environment variables

It's possible to access environment variables inside the templates.
```
{{@@ env['MY_VAR'] @@}}
```

This allows for storing host-specific properties and/or secrets in environment variables.
It is recommended to use `variables` (see [Available variables](#available-variables))
instead of environment variables unless these contain sensitive information that
shouldn't be versioned in git.

For example you can have a `.env` file in the directory where your `config.yaml` lies:
```
## Some secrets
pass="verysecurepassword"
```
If this file contains secrets that should not be tracked by git,
put it in your `.gitignore`.

You can then invoke dotdrop with the help of an alias
```bash
# when dotdrop is installed as a submodule
alias dotdrop='eval $(grep -v "^#" ~/dotfiles/.env) ~/dotfiles/dotdrop.sh'

# when dotdrop is installed from pypi or aur
alias dotdrop='eval $(grep -v "^#" ~/dotfiles/.env) /usr/bin/dotdrop --cfg=~/dotfiles/config.yaml'
```

The above aliases load all the variables from `~/dotfiles/.env`
(while omitting lines starting with `#`) before calling dotdrop.

## Available methods

Beside jinja2 global functions
(see [jinja2 global functions](http://jinja.pocoo.org/docs/2.10/templates/#list-of-global-functions)
the following functions are available and can be used within the templates:

* `exists(path)`: return true when path exists
```
{%@@ if exists('/dev/null') @@%}
it does exist
{%@@ endif @@%}
```

If you'd like a specific function to be available, either open an issue
or do a PR.

## Dynamic dotfile paths

Dotfile source (`src`) and destination (`dst`) can be dynamically constructed using
defined variables (`variables` or `dynvariables`).

For example to have a dotfile deployed on the unique firefox profile where the
profile path is dynamically found using a shell oneliner stored in a dynvariable:
```yaml
dynvariables:
  mozpath: find ~/.mozilla/firefox -name '*.default'
dotfiles:
  f_somefile:
    dst: "{{@@ mozpath @@}}/somefile"
    src: firefox/somefile
profiles:
  home:
    dotfiles:
    - f_somefile
```

Make sure to quote the path in the config file.

## Dynamic actions

Variables (`variables` and `dynvariables`) can be used
in actions for more advanced use-cases:

```yaml
dotfiles:
  f_test:
    dst: ~/.test
    src: test
    actions:
      - cookie_mv_somewhere "/tmp/moved-cookie"
variables:
  cookie_dir_available: (test -d /tmp/cookiedir || mkdir -p /tmp/cookiedir)
  cookie_header: "{{@@ cookie_dir_available @@}} && echo 'header' > /tmp/cookiedir/cookie"
  cookie_mv: "{{@@ cookie_header @@}} && mv /tmp/cookiedir/cookie"
actions:
  cookie_mv_somewhere: "{{@@ cookie_mv @@}} {0}"
```

Make sure to quote the actions using variables.

## Dotdrop header

Dotdrop is able to insert a header in the generated dotfiles. This allows
to remind anyone opening the file for editing that this file is managed by dotdrop.

Here's what it looks like:
```
This dotfile is managed using dotdrop
```

The header can be automatically added using [jinja2](http://jinja.pocoo.org/) directive:
```
{{@@ header() @@}}
```

Properly commenting the header in templates is the responsability of the user
as [jinja2](http://jinja.pocoo.org/) has no way of knowing what is the proper char(s) used for comments.
Either prepend the directive with the commenting char(s) used in the dotfile (for example `# {{@@ header() @@}}`)
or provide it as an argument `{{@@ header('# ') @@}}`. The result is equivalent.

## Debug template

To debug the result of a template, one can install the dotfiles to a temporary
directory with the `install` command and the `-t` switch:
```bash
$ dotdrop install -t
Installed to tmp /tmp/dotdrop-6ajz7565
```

# Example

Let's consider two hosts:

* **home**: home computer with hostname *home*
* **office**: office computer with hostname *office*

The home computer is running [awesomeWM](https://awesomewm.org/)
and the office computer [bspwm](https://github.com/baskerville/bspwm).
The *.xinitrc* file will therefore be different while still sharing some lines.
Dotdrop allows to store only one single *.xinitrc* but
to deploy different versions depending on where it is run from.

The following file is the dotfile stored in dotdrop containing
[jinja2](http://jinja.pocoo.org/) directives for the deployment based on the profile used.

Dotfile `<dotpath>/xinitrc`:
```bash
#!/bin/bash

# load Xresources
userresources=$HOME/.Xresources
if [ -f "$userresources" ]; then
      xrdb -merge "$userresources" &
fi

# launch the wm
{%@@ if profile == "home" @@%}
exec awesome
{%@@ elif profile == "office" @@%}
exec bspwm
{%@@ endif @@%}
```

The *if branch* will define which part is deployed based on the
hostname of the host on which dotdrop is run from.

And here's how the config file looks like with this setup.
Of course any combination of the dotfiles (different sets)
can be done if more dotfiles have to be deployed.

`config.yaml` file:
```yaml
config:
  backup: true
  create: true
  dotpath: dotfiles
dotfiles:
  f_xinitrc:
    dst: ~/.xinitrc
    src: xinitrc
profiles:
  home:
    dotfiles:
    - f_xinitrc
  office:
    dotfiles:
    - f_xinitrc
```

Installing the dotfiles (the `--profile` switch is not needed if
the hostname matches the *profile* entry in the config file):
```bash
# on home computer
$ dotdrop install --profile=home

# on office computer
$ dotdrop install --profile=office
```

Comparing the dotfiles:
```bash
# on home computer
$ dotdrop compare

# on office computer
$ dotdrop compare
```

# User tricks

See the [related wiki page](https://github.com/deadc0de6/dotdrop/wiki/user-tricks)

# People using dotdrop

For more examples, see how people are using dotdrop

* [https://github.com/open-dynaMIX/dotfiles](https://github.com/open-dynaMIX/dotfiles)
* [https://github.com/moyiz/dotfiles](https://github.com/moyiz/dotfiles)
* [https://github.com/japorized/dotfiles](https://github.com/japorized/dotfiles)
* [https://gitlab.com/lyze237/dotfiles-public](https://gitlab.com/lyze237/dotfiles-public)
* [https://github.com/whitelynx/dotfiles](https://github.com/whitelynx/dotfiles)

# Related projects

See [github does dotfiles](https://dotfiles.github.io/)

# Contribution

If you are having trouble installing or using dotdrop, open an issue.

If you want to contribute, feel free to do a PR (please follow PEP8).

# License

This project is licensed under the terms of the GPLv3 license.

