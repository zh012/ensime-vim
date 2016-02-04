# Ensime for vim `ensime-vim`

[![Join the chat at https://gitter.im/ensime/ensime-vim](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ensime/ensime-vim?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://drone.io/github.com/yazgoo/ensime-vim/status.png)](https://drone.io/github.com/yazgoo/ensime-vim/latest)
[![Coverage Status](https://coveralls.io/repos/yazgoo/ensime-vim/badge.svg?branch=master&service=github)](https://coveralls.io/github/yazgoo/ensime-vim?branch=master)

Vim, the editor of the Beast, has got an **Ensime** plugin to convert your preferred text editor
into a Java/Scala **IDE**. It's not time for half measures and `ensime-vim` aims at
becoming your go-to option to easily edit your source code in an efficient and fast way.

# Demo

![First demo](doc/ensime-vim.gif)
![Second demo](doc/ensime-vim2.gif)

# How to get to heaven!
  
Just follow the next steps and you'll be able to get `ensime-vim` in your vim in the blink of an eye.
  
## Installation
First, you need to install the `websocket-client` python package:

    $ sudo pip install websocket-client

Then, export your `$BROWSER` variable, for example in your `.bashrc`:

    $ export BROWSER=firefox

*If this variable is pointing to a script, make sure the shebang line (`#!/bin/bash` or whatever) 
is on top of the file to be executed properly.*

You also need the [ensime-sbt](https://github.com/ensime/ensime-sbt) plugin. You can
install it with a pretty one-liner (make sure `0.3.3` is the latest released version):
    
    $ echo 'addSbtPlugin("org.ensime" % "ensime-sbt" % "0.3.3")' \
        >> ~/.sbt/0.13/plugins/plugins.sbt

In order to install this plugin in your vim, you have two de facto options. Other plugin managers
should properly installed this plugin but their installation is not documented here.

Plugins                                           |Your .{n}vimrc
--------------------------------------------------|-------------------------------
[Vim-Plug](https://github.com/junegunn/vim-plug)  | `Plug 'ensime/ensime-vim'`
[Vundle](https://github.com/VundleVim/Vundle.vim) | `Plugin 'ensime/ensime-vim'`

After this, update your configuration and install them. With `vim-plug` this is done
by executing `:PlugInstall` followed by `:UpdateRemotePlugins`. With `Vundle` run `:PluginInstall`.

If you happen to use neovim, remember that you must install the neovim python module. Execute:

    $ pip install neovim

## Per project configuration

The `ensime-server` needs to know a little bit about your project. Hence you must generate an
`.ensime` file for any project in which you would like to use `ensime-vim`. The most easiest way to
do this is by executing in your root project folder:

    $ sbt gen-ensime

Afterwards, you are done and ready to enjoy the most of this project. If you want to contribute,
please check [this](#developer-howto).

# Event handling and remote plugin

Under neovim, for all commands except autocomplete, events are only handled when you move your cursor 
(that is the `CursorMoved` event). A well-known vim constraint is that it doesn't allow a plugin to 
have a real timer executing functions. In order to mimic this behavior, we use the `CursorHold` event 
and the `updatetime` vim global variable. The first one is triggered after a certain duration of time 
specified in `updatetime` in milliseconds. `Ensime-vim` sets this value to 1 second by default. 
  
If this is causing any problem with other plugins like `easytags`, please consider proposing to that 
plugin to allow low `updatetime`s times or open an issue to explain your problem. More information 
about timers in vim can be found [here](http://vim.wikia.com/wiki/Timer_to_execute_commands_periodically).
  
This plugin is implemented on `neovim` as an **rplugin**, bringing a better and faster user experience.
For people using `vim`, `ensime-vim` will be slower. The benefit of using `neovim` instead
is to make use of the new remote plugin architecture, which allows better speedups by using a
client-server approach for plugin developments.

# More refactorings...

Refactorings are on their way! Right now only the rename refactoring has been implemented and it's
not completed (only local renaming works). There are some issues with the `ensime-server` that
hopefully will be fixed in the following weeks. When that's finished and the new API is polished,
`ensime-vim` will get all the possible refactorings implemented.

# Do you want to know more?

Check the vim documentation of the plugin, which is just [here](doc/ensime-vim.txt). It's also available
from `vim` by running:

    :help ensime-vim

# Hey, devs, we need you!

All the logic of the plugin is under [ensime_shared](ensime_shared/). Take a peek into it and start contributing!
  
Before, we were using the great [neo2vim plugin](https://github.com/yazgoo/neo2vim) made by yazgoo. Now, this is 
no longer necessary as all the logic has been centralized and any change applied to `ensime_shared` will be propagated 
to both `vim` and `neovim`, helping readability and maintainability.
  
If you need to touch specific text editors configuration, especially if you register/unregister functions, check which
files are used by `vim` and `neovim`.
  
Vim-specific files                    | Neovim specific files
--------------------------------------|----------------------
[Vim ensime folder](autoload/)        | [Neovim rplugin](rplugin/python/ensime.py)
[Vim plugin folder](plugin/ensime.vim)|
  

All merges should be done on the `dev` branch before being merged onto master.

# Integrating with your own plugin

It is possible to register callbacks and send events to ensime.
Check [this plugin example](https://github.com/yazgoo/ensime-vim-typecheck).

# Contact

Would you like to have a new feature? Are you missing something? Do you need a dog? Contact us, 
open an issue and tell us your request/problem. We may help you!

# External references

* [Vimside](https://github.com/megaannum/vimside)
* [Envim](https://github.com/jlc/envim)
* [Vim-Ensime](https://github.com/psuter/vim-ensime)
* [Ensime](https://github.com/andreypopp/ensime)

The reference launch script is [here](https://gist.github.com/fommil/4ff3ad5b134280de5e46) 
(only works on Linux but should be adaptable to OS X, but you don't probably need it).
