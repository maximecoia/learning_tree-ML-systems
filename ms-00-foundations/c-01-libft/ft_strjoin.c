/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 16:13:17 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Builds a new string: s1 followed by s2.
 * Returns: the new string, or NULL if s1 or s2 is NULL or malloc fails.
 * Edge:    ("bon", "jour") gives "bonjour". s1 and s2 are unchanged.
 */
char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*joined;
	size_t	first_len;
	size_t	second_len;

	if (!s1 || !s2)
		return (NULL);
	first_len = ft_strlen(s1);
	second_len = ft_strlen(s2);
	joined = malloc(first_len + second_len + 1);
	if (!joined)
		return (NULL);
	ft_memcpy(joined, s1, first_len);
	ft_memcpy(joined + first_len, s2, second_len + 1);
	return (joined);
}
