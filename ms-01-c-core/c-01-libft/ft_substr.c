/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 15:49:53 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Copies at most len characters of s, from start, into a new string.
 * Returns: the new string, or NULL if s is NULL or malloc fails.
 * Edge:    start past the end: an empty string, allocated.
 *          len past the end: cut. ("bonjour", 3, 100) gives "jour".
 */
char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*sub;
	size_t	text_len;

	if (!s)
		return (NULL);
	text_len = ft_strlen(s);
	if (start >= text_len)
		return (ft_strdup(""));
	if (len > text_len - start)
		len = text_len - start;
	sub = malloc(len + 1);
	if (!sub)
		return (NULL);
	ft_strlcpy(sub, s + start, len + 1);
	return (sub);
}
