/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 15:12:15 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Copies text, '\0' included, into a new block from malloc.
 * Returns: the copy, or NULL when malloc fails.
 * Edge:    "" gives a 1 byte block holding '\0'.
 */
char	*ft_strdup(const char *text)
{
	char	*copy;
	size_t	len;

	len = ft_strlen(text) + 1;
	copy = malloc(len);
	if (!copy)
		return (NULL);
	ft_memcpy(copy, text, len);
	return (copy);
}
