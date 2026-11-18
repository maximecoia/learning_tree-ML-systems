/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line_utils.c                              :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/21 13:15:26 by mcoia             #+#    #+#             */
/*   Updated: 2026/10/21 13:15:26 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

/*
 * get_next_line_utils.c: the helpers of get_next_line.
 *
 * gnl_strlen and gnl_has_newline measure and search a string that may be
 * NULL: the stash is NULL before the first read and after the last line.
 * copy_bytes and gnl_join grow the stash: gnl_join makes a new block that
 * holds the old stash, then n bytes of the buffer, and frees the old one.
 *
 * Only read, malloc and free are called: strlen, strchr and memcpy are
 * not allowed, nor the libft. Every loop is written here.
 *
 * gnl_strlen, gnl_has_newline and gnl_join are declared in
 * get_next_line.h, for get_next_line.c calls them. copy_bytes is static:
 * only gnl_join, in this file, calls it.
 *
 * No function here keeps anything between two calls: the stash lives in
 * get_next_line.c, which owns it.
 */
#include "get_next_line.h"

/*
 * gnl_strlen: the length of a string.
 *
 * Receives s, a string, or NULL. Returns the number of characters before its
 * '\0'. "" gives 0, "abc" gives 3, and NULL gives 0: the stash starts out
 * NULL, and a NULL stash holds nothing yet. NULL is never read through.
 */
size_t	gnl_strlen(const char *s)
{
	size_t	len;

	if (!s)
		return (0);
	len = 0;
	while (s[len])
		len++;
	return (len);
}

/*
 * gnl_has_newline: is there a '\n' in s?
 *
 * Receives s, a string, or NULL. Returns 1 if a '\n' comes before its '\0',
 * 0 otherwise. NULL and "" give 0. NULL is never read through.
 */
int	gnl_has_newline(const char *s)
{
	size_t	i;

	if (!s)
		return (0);
	i = 0;
	while (s[i])
	{
		if (s[i] == '\n')
			return (1);
		i++;
	}
	return (0);
}

/*
 * copy_bytes: copy n bytes.
 *
 * Copies the first n bytes of src to the first n places of dst, and adds
 * nothing after them. With n at 0, src is not read, so it may be NULL.
 * static: only gnl_join, below, calls it.
 */
static void	copy_bytes(char *dst, const char *src, size_t n)
{
	size_t	i;

	i = 0;
	while (i < n)
	{
		dst[i] = src[i];
		i++;
	}
}

/*
 * gnl_join: a new block that holds old, then n bytes of add.
 *
 * Receives old, a string allocated by malloc, or NULL, which counts as
 * empty; add, which may hold more than n bytes, or a '\0' before them; and
 * n, the number of bytes of add to take. Returns a new block, allocated by
 * malloc, that holds the characters of old, then the first n bytes of add,
 * then a '\0'. gnl_join(NULL, "", 0) returns "", a block of one byte, not
 * NULL.
 * old is freed in every case, even when malloc fails: the caller replaces
 * its pointer by what gnl_join returns. Returns NULL if malloc fails.
 */
char	*gnl_join(char *old, const char *add, size_t n)
{
	size_t	old_len;
	char	*joined;

	old_len = gnl_strlen(old);
	joined = malloc(old_len + n + 1);
	if (!joined)
	{
		free(old);
		return (NULL);
	}
	copy_bytes(joined, old, old_len);
	copy_bytes(joined + old_len, add, n);
	joined[old_len + n] = '\0';
	free(old);
	return (joined);
}
