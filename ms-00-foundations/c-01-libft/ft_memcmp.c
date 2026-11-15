/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 09:44:10 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Compares first and second. bytes = how many to compare.
 * Returns: first differing byte of first minus second's, as unsigned
 *          chars. 0 if all equal or bytes is 0.
 * Edge:    a '\0' does not stop it. '\xff' against '\x01' is positive.
 */
int	ft_memcmp(const void *first, const void *second, size_t bytes)
{
	const unsigned char	*first_bytes;
	const unsigned char	*second_bytes;

	first_bytes = (const unsigned char *)first;
	second_bytes = (const unsigned char *)second;
	while (bytes > 0)
	{
		if (*first_bytes != *second_bytes)
			return (*first_bytes - *second_bytes);
		first_bytes++;
		second_bytes++;
		bytes--;
	}
	return (0);
}
