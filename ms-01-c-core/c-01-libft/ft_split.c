/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/05 10:50:36 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Counts the words of s: the runs of characters other than c.
 */
static size_t	count_words(char const *s, char c)
{
	size_t	word_count;

	word_count = 0;
	while (*s)
	{
		while (*s == c)
			s++;
		if (*s)
			word_count++;
		while (*s && *s != c)
			s++;
	}
	return (word_count);
}

/*
 * Frees the first word_count words of words, then the array itself.
 */
static void	free_words(char **words, size_t word_count)
{
	while (word_count > 0)
	{
		word_count--;
		free(words[word_count]);
	}
	free(words);
}

/*
 * Copies each word of s into words, then ends the array with NULL.
 * Returns: 1, or 0 when a malloc fails, after freeing everything.
 */
static int	fill_words(char **words, char const *s, char c)
{
	size_t	i;
	size_t	word_len;

	i = 0;
	while (*s)
	{
		while (*s == c)
			s++;
		word_len = 0;
		while (s[word_len] && s[word_len] != c)
			word_len++;
		if (word_len > 0)
		{
			words[i] = ft_substr(s, 0, word_len);
			if (!words[i])
			{
				free_words(words, i);
				return (0);
			}
			i++;
		}
		s += word_len;
	}
	words[i] = NULL;
	return (1);
}

/*
 * Cuts s at every c into a new array of new strings, all from malloc.
 * Returns: the array, ended by NULL, or NULL if s is NULL or a malloc
 *          fails. Every block already made is then freed.
 * Edge:    no empty word: ("--ab-cd--", '-') gives {"ab", "cd", NULL}.
 *          "" gives an allocated array holding only NULL.
 */
char	**ft_split(char const *s, char c)
{
	char	**words;

	if (!s)
		return (NULL);
	words = malloc((count_words(s, c) + 1) * sizeof(char *));
	if (!words)
		return (NULL);
	if (!fill_words(words, s, c))
		return (NULL);
	return (words);
}
