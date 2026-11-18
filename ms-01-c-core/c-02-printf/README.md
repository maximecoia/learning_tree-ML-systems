*This activity has been created as part of the 42 curriculum by mcoia.*

# ft_printf

## Description

ft_printf is a C project of the 42 common core. The goal is to rewrite the
libc's `printf` and ship it as a static library, `libftprintf.a`, that later
projects can reuse. The project trains variadic functions, `stdarg.h`, the
default argument promotions, writing numbers in a base, and error paths.

`ft_printf` has the prototype of `printf`:

```c
int	ft_printf(const char *format, ...);
```

It writes to the standard output with `write` alone, without a buffer, and
returns the number of characters written, or `-1` when the format is `NULL`
or a write fails.

### The conversions

| Conversion | What it writes |
|---|---|
| `%c` | one character |
| `%s` | a string |
| `%p` | a pointer in hexadecimal, after `0x` |
| `%d`, `%i` | a signed decimal `int` |
| `%u` | an unsigned decimal `unsigned int` |
| `%x`, `%X` | an `unsigned int` in hexadecimal, lowercase or uppercase |
| `%%` | a percent sign |

Output and return value match the system's `printf` byte for byte,
including the cases the subject does not spell out:

- `%s` on a null pointer writes `(null)`.
- `%c` on the null character writes one byte.
- `%p` on a null pointer writes what the local libc writes, `(nil)` on
  Linux and `0x0` on macOS.
- A `%` that ends the format writes nothing. An unknown conversion writes
  its letter alone.

### Algorithm and data structure

The format is read once, from left to right, by a loop that hands each
piece to `step`. Outside a `%`, `step` writes the character. On a `%`, it
reads the next character and dispatches on it. That dispatch is the whole
data structure: a chain of comparisons in one function, the only place that
maps a conversion letter to what it writes. A table of function pointers
was the other candidate; with nine letters and six of them sharing one
routine, the chain is shorter and reads in one screen.

Each conversion asks `va_arg` for the type the caller actually pushed,
after the default promotions: `int` for `%c`, `unsigned int` for `%u`, `%x`
and `%X`, `void *` for `%p`. The `va_list` travels by pointer, so every
helper moves the same cursor.

### Technical choices

- All numbers go through one recursive routine, `put_base`. It divides by
  the base until the leading digit and writes on the way back, most
  significant digit first, with no buffer to size.
- `put_base` takes the prefix as an argument and writes it just before the
  leading digit: `-` for a negative `%d`, `0x` for `%p`.
- Negative values are widened to `unsigned long` and negated there, where
  the arithmetic is defined, so `INT_MIN` needs no special case.
- Pointers stay in `unsigned long`, eight bytes, and never lose their high
  half through an `unsigned int`.
- The first failed `write` makes the whole call return `-1`.
- Helper functions are `static`, so they stay private to `ft_printf.c`.

## Instructions

Build the library:

```bash
make
```

This compiles `ft_printf.c` with `cc -Wall -Wextra -Werror`, then archives
the object with `ar rcs libftprintf.a`. Running `make` again does nothing
until `ft_printf.c` or `ft_printf.h` changes.

Other rules:

| Rule | Effect |
|---|---|
| `make clean` | removes the object files |
| `make fclean` | removes the object files and `libftprintf.a` |
| `make re` | `fclean`, then a full build |

Use the library in a program:

```c
#include "ft_printf.h"

int	main(void)
{
	ft_printf("%s is %d years old, at %p\n", "Ada", 36, (void *)0x42);
	return (0);
}
```

```bash
cc -Wall -Wextra -Werror -I. main.c -L. -lftprintf -o hello
```

`-L.` tells the linker where to look, and `-lftprintf` names
`libftprintf.a`.

## Resources

### C and the libc

- `man 3 printf` and `man 3 stdarg`, for the conversions and the variadic
  macros.
- The C11 standard, section 7.16 on `<stdarg.h>` and section 6.5.2.2 on the
  default argument promotions.
- [cppreference, printf](https://en.cppreference.com/w/c/io/fprintf) and
  [cppreference, variadic arguments](https://en.cppreference.com/w/c/variadic).
- [The 42 Norm](https://github.com/42School/norminette/blob/master/pdf/en.norm.pdf)
  and the `norminette` tool.
- [GNU make manual](https://www.gnu.org/software/make/manual/make.html),
  for pattern rules and automatic variables.
- The local `printf`, called on each case, as the reference for what the
  output must be.

### Use of AI

AI was used as a tutor only. It explained C concepts in French, such as
variadic functions, `va_list`, the default promotions, recursion and
writing a number in a base. It wrote practice tests that compare each
conversion with the libc, and failure tests that make `write` fail. It
reviewed my code and pointed out edge cases. The code of the library was
written and typed by me.
