/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 13:36:38 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Compares at most limit characters of first and second.
 * Returns: first differing character of first minus second's, as
 *          unsigned chars. 0 if equal up to limit.
 * Edge:    limit 0 gives 0. Stops at the '\0' of either string.
 */
int	ft_strncmp(const char *first, const char *second, size_t limit)
{
	size_t	i;

	i = 0;
	while (i < limit && (first[i] || second[i]))
	{
		if (first[i] != second[i])
			return ((unsigned char)first[i] - (unsigned char)second[i]);
		i++;
	}
	return (0);
}
