/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 15:09:47 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Looks for word in the first limit characters of text.
 * Returns: the first match that fits whole before limit, or NULL.
 * Edge:    empty word returns text.
 *          ("bonjour", "jour", 5) gives NULL; with 7, "jour".
 */
char	*ft_strnstr(const char *text, const char *word, size_t limit)
{
	size_t	word_len;
	size_t	i;

	word_len = ft_strlen(word);
	if (word_len == 0)
		return ((char *)text);
	i = 0;
	while (i + word_len <= limit && text[i])
	{
		if (ft_strncmp(text + i, word, word_len) == 0)
			return ((char *)text + i);
		i++;
	}
	return (NULL);
}
