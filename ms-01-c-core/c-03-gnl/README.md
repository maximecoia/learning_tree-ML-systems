*This activity has been created as part of the 42 curriculum by mcoia.*

# get_next_line

## Description

`get_next_line` returns the next line of a file descriptor at each call,
its `\n` included, and `NULL` once nothing is left to read or on an error.
It reads with `read` alone, `BUFFER_SIZE` bytes at a time, and works the
same on a regular file, a pipe and the standard input. The last line keeps
no `\n` when the file does not end with one, and an empty line, `"\n"`, is
a line like any other: only `NULL` means the end.

## Instructions

### Compile

Compile the two `.c` files with your program, and give the size of a read
on the command line; without it, the header falls back to 42:

```bash
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 main.c get_next_line.c get_next_line_utils.c -o gnl
```

A program includes `get_next_line.h`, and frees every line it receives.
The `main.c` of the tests below reads the file named on the command line,
or the standard input without one, and prints each line between brackets,
so the place where a line stops is visible:

```c
#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

int	main(int argc, char **argv)
{
	int		fd;
	char	*line;

	fd = 0;
	if (argc > 1)
		fd = open(argv[1], O_RDONLY);
	line = get_next_line(fd);
	while (line)
	{
		printf("[%s]", line);
		free(line);
		line = get_next_line(fd);
	}
	if (fd > 0)
		close(fd);
	return (0);
}
```

### Tests for the review

Run them in order, from the folder of the project. Each one says what must
come out.

**1. Norm and allowed functions.** Every file must print `OK!`:

```bash
norminette get_next_line.c get_next_line_utils.c get_next_line.h
```

Then list what the code calls from outside. Only `read`, `malloc`, `free`
and the three `gnl_` helpers may appear; no `lseek`, no libft:

```bash
cc -Wall -Wextra -Werror -c get_next_line.c get_next_line_utils.c && nm -u get_next_line.o get_next_line_utils.o; rm -f get_next_line.o get_next_line_utils.o
```

The only `static` variable is the stash, declared inside `get_next_line`.
This must print that one line:

```bash
grep -n "static.*;" get_next_line.c get_next_line_utils.c
```

**2. Every line, at several sizes.** The file holds a normal line, an empty
line, two short lines, and a last line without `\n`. The loop compiles at
five sizes and compares the output with what is expected, byte for byte.
It must print five `ok` lines:

```bash
printf 'first line\n\nab\nc\nlast line without newline' > lines.txt
printf '[first line\n][\n][ab\n][c\n][last line without newline]' > expected.txt
for size in 1 2 42 9999 10000000; do
	cc -Wall -Wextra -Werror -D BUFFER_SIZE=$size main.c get_next_line.c get_next_line_utils.c -o gnl
	./gnl lines.txt | cmp - expected.txt && echo "BUFFER_SIZE=$size ok"
done
```

**3. Without `-D BUFFER_SIZE`.** The header's default must compile and read
the same. It must print `default ok`:

```bash
cc -Wall -Wextra -Werror main.c get_next_line.c get_next_line_utils.c -o gnl && ./gnl lines.txt | cmp - expected.txt && echo "default ok"
```

The tests 4 to 8 keep this program.

**4. Edge files.**

| Command | What must come out |
|---|---|
| `: > empty.txt; ./gnl empty.txt` | nothing: the first call returns `NULL` |
| `printf '\n\n\n' > newlines.txt; ./gnl newlines.txt` | three times `[` then a line break then `]` |
| `printf 'x' > one.txt; ./gnl one.txt` | `[x]` |

**5. A very long line.** One line of a million bytes, without `\n`. The
count must be 1000002, the line and its two brackets:

```bash
head -c 1000000 /dev/zero | tr '\0' 'a' > long.txt
cc -Wall -Wextra -Werror -D BUFFER_SIZE=4096 main.c get_next_line.c get_next_line_utils.c -o gnl && ./gnl long.txt | wc -c
```

**6. The standard input.** Through a pipe, it must print `[one` and `][two`
and `]` on three lines:

```bash
printf 'one\ntwo\n' | ./gnl
```

Typed by hand: run `./gnl`, type a line, press Enter. The line comes back
between brackets at once. Ctrl-D ends the input.

**7. Errors.** Each command must print nothing and must not crash: a file
that does not exist gives the descriptor -1, a folder makes `read` fail,
and `<&-` closes the standard input before the program starts.

```bash
./gnl missing.txt
```

```bash
./gnl .
```

```bash
./gnl <&-
```

A `BUFFER_SIZE` of 0 or less must compile and print nothing:

```bash
for size in 0 -1; do
	cc -Wall -Wextra -Werror -D BUFFER_SIZE=$size main.c get_next_line.c get_next_line_utils.c -o gnl && ./gnl lines.txt
done
```

**8. Memory.** Rebuild at 42 first. On Linux, the summary must say that all
heap blocks were freed and count 0 errors:

```bash
cc -Wall -Wextra -Werror -g -D BUFFER_SIZE=42 main.c get_next_line.c get_next_line_utils.c -o gnl
valgrind --leak-check=full --show-leak-kinds=all ./gnl lines.txt
```

On macOS, the last line must say `0 leaks for 0 total leaked bytes`:

```bash
leaks --atExit -- ./gnl lines.txt
```

A program that stops before the last `NULL` leaves the rest of the file in
the stash: that block is still reachable, and it is freed by reading the
file to its end.

**9. Clean up.**

```bash
rm -rf gnl gnl.dSYM lines.txt expected.txt empty.txt newlines.txt one.txt long.txt
```

## Algorithm

`read` returns bytes, not lines, so a read often goes past the `\n`. What it
took too much must wait for the next call: it is kept in a stash, a `static`
pointer local to `get_next_line`, the only state that survives between two
calls. The subject forbids global variables, and a local `static` is visible
to this one function alone.

Each call first fills the stash. It reads blocks of `BUFFER_SIZE` bytes and
joins each one at the end of the stash, until the stash holds a `\n` or
`read` returns 0. Then it cuts the stash after its first `\n`, or at its end
when there is none: the first part is the line returned, the second part
becomes the new stash.

The stash is never kept empty. When nothing follows the line, it is freed
and set to `NULL`. A `NULL` stash after a read that returned 0 is therefore
the one end of file, and an empty line cannot be mistaken for it. On a read
error or a failed `malloc`, the stash is freed and set to `NULL` as well, so
nothing of a failed file comes out at a later call.

Joining copies the whole stash at every block. That is the simplest correct
choice, and it costs: a line of 10 MB read 4096 bytes at a time takes 2561
reads, and the joins copy about 13.4 GB in all. Growing the stash by
doubling its capacity would copy about 27 MB instead, at the price of a
second variable to track the capacity. The lines this function meets are
short, so the simple join was kept.

## Resources

- `man 2 read` and `man 2 open`, for the three kinds of value `read` returns.
- The C11 standard, section 6.2.4, on the storage duration of a `static`
  local variable.
- Python's `str.splitlines(keepends=True)`, the reference the tests compare
  every line with.

### Use of AI

AI was used as a tutor only. It explained C concepts in French, such as
file descriptors, the return values of `read`, `static` variables and who
frees each block. It wrote practice tests that compare every line with
Python, and failure tests that make `malloc` and `read` fail. It reviewed my
code and pointed out edge cases. The code of the function was written and
typed by me.
