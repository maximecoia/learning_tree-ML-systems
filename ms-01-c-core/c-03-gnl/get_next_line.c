/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/21 13:15:26 by mcoia             #+#    #+#             */
/*   Updated: 2026/10/21 13:15:26 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

/*
 * get_next_line.c: get_next_line and the two functions it calls.
 *
 * get_next_line returns the next line of a file descriptor, '\n' included
 * when the file has one, or NULL once the file is read through or on an
 * error. A call may read more than one line: what is read past the line
 * waits in the stash, a static variable of get_next_line, for the next call.
 *
 * C needs a function defined above the place that calls it, so the file
 * goes fill_stash, cut_line, get_next_line: the callees first.
 *
 * fill_stash reads BUFFER_SIZE bytes at a time into a buffer of its own,
 * and joins them to the stash, until the stash holds a '\n' or read
 * reaches the end of the file. cut_line splits the stash after its first
 * line: it returns that line and keeps the rest for the next call.
 *
 * Only read, malloc and free are called, plus the helpers of
 * get_next_line_utils.c. No global variable: the subject forbids them, and
 * a static written outside a function is one. The stash is a static
 * written inside get_next_line, so it is not a global.
 *
 * Every error leaves no block behind. A read or a malloc that fails frees
 * the buffer, the stash and the line, and sets the stash to NULL. A
 * negative fd and a BUFFER_SIZE of 0 or less return NULL before any read
 * or malloc.
 *
 * BUFFER_SIZE is set by the -D option of cc, -D BUFFER_SIZE=n.
 * get_next_line.h gives it a default, used when the option is not
 * given.
 */
#include "get_next_line.h"

/*
 * fill_stash: read until the stash holds a line.
 *
 * Receives fd, the file to read; stash, the address of the caller's
 * stash: a string allocated by malloc, or NULL when it holds nothing; and
 * size, the BUFFER_SIZE get_next_line passes once it has tested it.
 * Reads fd size bytes at a time, and joins each block read at the end of
 * the stash, until the stash holds a '\n' or read returns 0, the end of
 * the file. A stash that already holds a '\n' reads nothing.
 * read may return fewer bytes than asked while the file goes on: only its
 * return says how many bytes the block holds.
 * Returns 0. Returns -1 if read returns -1 or a malloc fails: the stash is
 * then freed and set to NULL, so nothing read before the error comes out
 * later.
 * The block of size bytes comes from malloc, not from an array: size may
 * be 10000000, more than the stack holds. It is freed before returning, in
 * every case.
 */
static int	fill_stash(int fd, char **stash, size_t size)
{
	char	*buf;
	ssize_t	got;

	buf = malloc(size);
	got = 1;
	if (!buf)
		got = -1;
	while (got > 0 && !gnl_has_newline(*stash))
	{
		got = read(fd, buf, size);
		if (got > 0)
			*stash = gnl_join(*stash, buf, (size_t)got);
		if (got > 0 && !*stash)
			got = -1;
	}
	free(buf);
	if (got < 0)
	{
		free(*stash);
		*stash = NULL;
		return (-1);
	}
	return (0);
}

/*
 * cut_line: split the stash after its first line.
 *
 * Receives stash, the address of the caller's stash, which is not NULL and
 * not empty. The line is everything up to its first '\n', that '\n'
 * included; or the whole stash, when it holds no '\n'. Returns the line, a
 * new block allocated by malloc. The stash becomes what follows the line,
 * in a new block, or NULL when nothing follows: an empty stash is never
 * kept. The old stash is freed.
 * "ab\ncd" gives the line "ab\n" and the stash "cd". "ab\n" gives "ab\n"
 * and NULL. "ab" gives "ab" and NULL.
 * Returns NULL if a malloc fails, with the stash freed and set to NULL.
 */
static char	*cut_line(char **stash)
{
	size_t	len;
	char	*line;
	char	*rest;

	len = 0;
	while ((*stash)[len] && (*stash)[len] != '\n')
		len++;
	if ((*stash)[len] == '\n')
		len++;
	line = gnl_join(NULL, *stash, len);
	rest = NULL;
	if (line && (*stash)[len])
	{
		rest = gnl_join(NULL, *stash + len, gnl_strlen(*stash + len));
		if (!rest)
		{
			free(line);
			line = NULL;
		}
	}
	free(*stash);
	*stash = rest;
	return (line);
}

/*
 * get_next_line: the next line of fd.
 *
 * Receives fd, a file descriptor. Returns the next line of fd, its '\n'
 * included, as a block allocated by malloc that the caller frees. Returns
 * NULL when nothing is left to read, and on any error: a negative or closed
 * fd, a failed read or malloc, a BUFFER_SIZE of 0 or less.
 * An empty line, "\n", is a line, not the end. The last line has no '\n'
 * when the file does not end with one.
 * The stash, what a read took past the line, must survive between two
 * calls: it is a static variable declared inside this function, never a
 * global one.
 */
char	*get_next_line(int fd)
{
	static char	*stash;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	if (fill_stash(fd, &stash, BUFFER_SIZE) < 0)
		return (NULL);
	if (!stash)
		return (NULL);
	return (cut_line(&stash));
}
