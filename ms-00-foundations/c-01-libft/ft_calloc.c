/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 09:55:42 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Allocates count * elem_size bytes, all set to 0.
 * Returns: the block, or NULL when malloc fails.
 * Edge:    count * elem_size overflows a size_t: NULL, no malloc.
 *          count or elem_size 0: a valid block that free accepts.
 */
void	*ft_calloc(size_t count, size_t elem_size)
{
	void	*block;

	if (elem_size != 0 && count > (size_t)-1 / elem_size)
		return (NULL);
	block = malloc(count * elem_size);
	if (!block)
		return (NULL);
	ft_bzero(block, count * elem_size);
	return (block);
}
