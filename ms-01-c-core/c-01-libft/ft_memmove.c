/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 09:24:59 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Copies source into dest, zones may overlap. bytes = how many to copy.
 * Returns: dest.
 * How:     dest before source: copy forward. After: copy backward, so no
 *          byte of source is overwritten before it is read.
 * Edge:    "abcdef", 4 bytes from t to t + 2, gives "ababcd".
 */
void	*ft_memmove(void *dest, const void *source, size_t bytes)
{
	unsigned char		*to;
	const unsigned char	*from;

	if (!dest && !source)
		return (dest);
	to = (unsigned char *)dest;
	from = (const unsigned char *)source;
	if (to < from)
		return (ft_memcpy(dest, source, bytes));
	while (bytes > 0)
	{
		bytes--;
		to[bytes] = from[bytes];
	}
	return (dest);
}
