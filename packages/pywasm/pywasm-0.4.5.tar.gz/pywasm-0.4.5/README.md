# pywasm: A WebAssembly interpreter written in pure Python.

[![Build Status](https://travis-ci.org/mohanson/pywasm.svg?branch=master)](https://travis-ci.org/mohanson/pywasm)

A WebAssembly interpreter written in pure Python. JIT used.

Current specification wasm version is: [WebAssembly Core Specification W3C Working Draft, 4 September 2018](https://www.w3.org/TR/2018/WD-wasm-core-1-20180904/). Just like Firefox or Chrome does.

# Installation

```sh
$ pip3 install pywasm
```

# Some simple examples

1. First we need a wasm module! Grab our `./examples/fib.wasm` file and save a copy in a new directory on your local machine. Note: `fib.wasm` was compiled from `./examples/fib.c` by [WasmFiddle](https://wasdk.github.io/WasmFiddle/).

2. Now, compile and instantiate WebAssembly modules directly from underlying sources. This is achieved using the `pywasm.load` method.

```py
import pywasm
# pywasm.on_debug()

vm = pywasm.load('/src/pywasm/examples/fib.wasm')
r = vm.exec('fib', [10])
print(r) # 55
```

A brief description for `./examples`

| File                | Description                                  |
|---------------------|----------------------------------------------|
| ./examples/add.wasm | Export i32.add function                      |
| ./examples/env.wasm | Call python/native function in wasm          |
| ./examples/fib.wasm | Fibonacci, which contains loop and recursion |
| ./examples/str.wasm | Export a function which returns string       |
| ./examples/sum.wasm | Equal difference series summation            |

# Thanks

- [wagon](https://github.com/go-interpreter/wagon), The author is very kind
- [warpy](https://github.com/kanaka/warpy)

# License

[WTFPL](./LICENSE)
