/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 10:37:06 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Appends source to dest. dest never exceeds dest_size bytes, '\0' in.
 * Returns: start length of dest + ft_strlen(source). >= dest_size: cut.
 * Edge:    no '\0' in dest's first dest_size bytes: writes nothing,
 *          returns dest_size + ft_strlen(source).
 *          "ab" + "cdef" in 6 bytes gives "abcde" and returns 6.
 */
size_t	ft_strlcat(char *dest, const char *source, size_t dest_size)
{
	size_t	dest_len;
	size_t	src_len;
	size_t	i;

	src_len = ft_strlen(source);
	dest_len = 0;
	while (dest_len < dest_size && dest[dest_len])
		dest_len++;
	if (dest_len == dest_size)
		return (dest_size + src_len);
	i = 0;
	while (source[i] && dest_len + i + 1 < dest_size)
	{
		dest[dest_len + i] = source[i];
		i++;
	}
	dest[dest_len + i] = '\0';
	return (dest_len + src_len);
}
