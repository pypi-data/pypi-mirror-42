[![logo](/resources/logo.svg)](https://ejrbuss.net/mekpie/)

# Make Building C as Simple as Pie

Mekpie is an opinionated build system for small scale C projects. The core premise of Mekpie is that you should not be spending time worrying about Make files, compiler arguments, or build times, when working on a small C projects. By enforcing a simple directory structure and always providing a clean build, Mekpie saves you time and effort. For added convenience Mekpie takes notes from tools like [Rust's cargo](https://doc.rust-lang.org/cargo/guide/index.html) and [Node's npm](https://www.npmjs.com/) and provides options for building, running, cleaning, and testing your current project.

Mekpie is a small scale project and is not supposed to replace tools like [CMake](https://cmake.org/) or provide any sort of package management capabilities. Use Mekpie when the alternative is a shoddy Make file or manually compiling.

Currently Mekpie supports the gcc, clang, avr-gcc, and emscripten compilers, as well as allows users to write custom compiler configurations.

## Installing

Mekpie is a python package. Use pip to install it!
```bash
$ pip install mekpie
```

## Getting Started

Create a new project by running `mekpie new`. Mekpie will walk you through the configuration
```
$ mekpie new "project-name"
┌ Configuring mekpie...
│ Please provide a name for your project (default project-name):
│ Selected project-name.
│ Mekpie supports the following c compilers, please select one (compilers must be installed seperately):
│     - gcc_clang   for use with the gcc or clang compiler
│     - emscripten  for use with the emscripten c to js compiler
│     - avr_gcc     for use with avr-gcc and avrdude
│ Please select a cc (default gcc_clang):
│ Selected gcc_clang.
│ ┌ Configuring gcc_clang...
│ │ Please select a compiler command (default cc):
│ │ Selected cc.
│ │ Please select a debug command (default lldb):
│ │ Selected lldb.
│ └ gcc_clang configured!
└ mekpie configured!
project-name created successfully!
```

Then navigate to the project directory and run
```
$ mekpie run
Project succesfully cleaned.
Project succesfully built. (0.060s)
Hello, World!
```

That's it!

## [Read More](https://ejrbuss.net/mekpie)

## Contact

Feel free to send be bug reports or feature requests. If you are interested in my other work, checkout my [website](https://ejrbuss.net).

Email ejrbuss@gmail.com
