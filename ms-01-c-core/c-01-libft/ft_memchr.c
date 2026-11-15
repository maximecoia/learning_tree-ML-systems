/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 09:39:47 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Looks for (unsigned char)target in area. bytes = how many to search.
 * Returns: the address of the first match, or NULL.
 * Edge:    a '\0' does not stop it. Nothing past that count is read.
 */
void	*ft_memchr(const void *area, int target, size_t bytes)
{
	const unsigned char	*bytes_ptr;

	bytes_ptr = (const unsigned char *)area;
	while (bytes > 0)
	{
		if (*bytes_ptr == (unsigned char)target)
			return ((void *)bytes_ptr);
		bytes_ptr++;
		bytes--;
	}
	return (NULL);
}
