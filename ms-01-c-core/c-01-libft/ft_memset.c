/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 08:54:10 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Fills area with (unsigned char)value. bytes = how many to write.
 * Returns: area.
 * Edge:    bytes 0 writes nothing.
 */
void	*ft_memset(void *area, int value, size_t bytes)
{
	unsigned char	*bytes_ptr;

	bytes_ptr = (unsigned char *)area;
	while (bytes > 0)
	{
		*bytes_ptr = (unsigned char)value;
		bytes_ptr++;
		bytes--;
	}
	return (area);
}
