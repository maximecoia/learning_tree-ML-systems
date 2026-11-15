*This activity has been created as part of the 42 curriculum by mcoia.*

# Libft

## Description

Libft is the first C project of the 42 common core. The goal is to write a
personal C library, `libft.a`, that later projects can reuse instead of the
standard library. Each function is rewritten from scratch, with the `ft_`
prefix, using only `malloc`, `free` and `write` from the system.

The project trains the basics of C: pointers and memory, strings, dynamic
allocation and its failure paths, function pointers, linked lists, and
building a static library with a Makefile.

### The library

The library holds 43 functions in three parts, plus one type.

**Part 1, libc functions.** Same prototype and behavior as the originals
described in their `man` pages.

| Group | Functions |
|---|---|
| Character tests and case | `ft_isalpha`, `ft_isdigit`, `ft_isalnum`, `ft_isascii`, `ft_isprint`, `ft_toupper`, `ft_tolower` |
| Memory | `ft_memset`, `ft_bzero`, `ft_memcpy`, `ft_memmove`, `ft_memchr`, `ft_memcmp`, `ft_calloc` |
| Strings | `ft_strlen`, `ft_strlcpy`, `ft_strlcat`, `ft_strchr`, `ft_strrchr`, `ft_strncmp`, `ft_strnstr`, `ft_strdup` |
| Conversion | `ft_atoi` |

**Part 2, additional functions.** Not in the libc, or in a different form.

| Function | What it does |
|---|---|
| `ft_substr` | allocates the substring of `len` characters starting at `start` |
| `ft_strjoin` | allocates the concatenation of two strings |
| `ft_strtrim` | allocates a copy without the characters of `set` at both ends |
| `ft_split` | splits a string on a separator into a NULL-terminated array |
| `ft_itoa` | allocates the decimal string of an `int`, `INT_MIN` included |
| `ft_strmapi` | allocates a new string, each character produced by `f(index, c)` |
| `ft_striteri` | calls `f(index, &c)` on each character, in place |
| `ft_putchar_fd`, `ft_putstr_fd`, `ft_putendl_fd`, `ft_putnbr_fd` | write a character, a string, a line or a number on a file descriptor |

**Part 3, linked lists.** Built on the `t_list` type:

```c
typedef struct s_list
{
	void			*content;
	struct s_list	*next;
}	t_list;
```

| Function | What it does |
|---|---|
| `ft_lstnew` | allocates a node holding `content` |
| `ft_lstadd_front`, `ft_lstadd_back` | add a node at the start or the end |
| `ft_lstsize`, `ft_lstlast` | count the nodes, return the last one |
| `ft_lstdelone` | frees one node and its content with `del` |
| `ft_lstclear` | frees the whole list, then sets the head pointer to NULL |
| `ft_lstiter` | calls `f` on each content |
| `ft_lstmap` | builds a new list from `f` applied to each content |

### Technical choices

- Every function that allocates checks `malloc`. On failure it frees what
  it already allocated and returns NULL. `ft_split` and `ft_lstmap` were
  tested by making each `malloc` call fail in turn: no leak.
- `ft_calloc` refuses a `count * size` product that overflows `size_t`, and
  `ft_calloc(0, 0)` returns a unique pointer that can be freed.
- Memory and comparison functions read bytes as `unsigned char`, so bytes
  above 127 compare like in the libc.
- Part 1 functions behave like the libc on NULL. Part 2 and list functions
  return NULL or do nothing when given a NULL pointer.
- Helper functions are `static`, so they stay private to their file.

## Instructions

Build the library:

```bash
make
```

This compiles every `ft_*.c` file with `cc -Wall -Wextra -Werror`, then
archives the objects with `ar rcs libft.a`. Running `make` again does
nothing until a source file or `libft.h` changes.

Other rules:

| Rule | Effect |
|---|---|
| `make clean` | removes the object files |
| `make fclean` | removes the object files and `libft.a` |
| `make re` | `fclean`, then a full build |

Use the library in a program:

```c
#include "libft.h"

int	main(void)
{
	ft_putendl_fd("hello", 1);
	return (0);
}
```

```bash
cc -Wall -Wextra -Werror -I. main.c -L. -lft -o hello
```

`-L.` tells the linker where to look, and `-lft` names `libft.a`.

## Resources

### C and the libc

- The `man` pages of each original function, section 3: `man 3 strlcpy`,
  `man 3 memmove`, and so on.
- [cppreference, C standard library](https://en.cppreference.com/w/c)
- [The 42 Norm](https://github.com/42School/norminette/blob/master/pdf/en.norm.pdf)
  and the `norminette` tool.
- [GNU make manual](https://www.gnu.org/software/make/manual/make.html),
  for pattern rules and automatic variables.
- `man ar`, for static archives.
- `man leaks` on macOS, and the
  [Valgrind quick start](https://valgrind.org/docs/manual/quick-start.html)
  on Linux, to check for memory leaks.

### Use of AI

AI was used as a tutor only. It explained C concepts in French, such as
pointers, `size_t`, `const`, function pointers and Makefile rules. It wrote
practice tests that compare each function with the libc, and failure tests
that make `malloc` return NULL. It reviewed my code and pointed out edge
cases. The code of the library was written and typed by me.
