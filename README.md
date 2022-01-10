# Introduction

A simple project to solve the 13th challenge of [The Pragmatic Programmer](https://www.pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/).

## Examples

An `input.txt` file

```bash
# Instructions:
# The data types used to specify the structure is almost similar to C++
# Start with a # sign to comment
# Use M flag to create a new data structure
# Use F flag to specify field and type separated by space(s)
# Use E flag to end the creation of the data structure

M Product
F id            int
F name          char(30)
F order_code    int
E
```

will generate:

`output.cpp`

```cpp
typedef struct {
  int id;
  char(30) name;
  int order_code;
} Product;
```

`output.ts`

```ts
export interface Product {
  id: number;
  name: string[];
  order_code: number;
}
```
