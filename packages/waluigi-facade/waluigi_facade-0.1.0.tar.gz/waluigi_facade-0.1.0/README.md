# Waluigi

With the power of pycall and some metaprogramming magic is possible to facade a ruby class into a luigi task. Not everything works, but looks promising.

## What works

- Executing the run method
- Declaring outputs defined in Python code
- Declaring requirements programmed either in Ruby or Python
- Parameters declaration in Ruby
- Getting information from the Python side (output(), input(), parameters, etc)

## What doesn't

- Utility classes: WrapperTask, ExternalTask, etc
