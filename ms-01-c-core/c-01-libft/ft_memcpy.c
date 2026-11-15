/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 09:16:09 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Copies source into dest. bytes = how many to copy.
 * Returns: dest.
 * Edge:    zones must not overlap: ft_memmove handles that.
 *          dest and source both NULL: returns dest, touches nothing.
 */
void	*ft_memcpy(void *dest, const void *source, size_t bytes)
{
	unsigned char		*to;
	const unsigned char	*from;
	size_t				i;

	if (!dest && !source)
		return (dest);
	to = (unsigned char *)dest;
	from = (const unsigned char *)source;
	i = 0;
	while (i < bytes)
	{
		to[i] = from[i];
		i++;
	}
	return (dest);
}
