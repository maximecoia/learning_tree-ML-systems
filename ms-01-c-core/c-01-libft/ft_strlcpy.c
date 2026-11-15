/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 10:01:02 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Copies source into dest: at most dest_size - 1 characters, then '\0'.
 * Returns: ft_strlen(source). A return >= dest_size means it was cut.
 * Edge:    dest_size 0 writes nothing, not even '\0'.
 *          "bonjour" into 4 bytes gives "bon" and returns 7.
 */
size_t	ft_strlcpy(char *dest, const char *source, size_t dest_size)
{
	size_t	i;
	size_t	src_len;

	src_len = ft_strlen(source);
	if (dest_size == 0)
		return (src_len);
	i = 0;
	while (i < dest_size - 1 && source[i])
	{
		dest[i] = source[i];
		i++;
	}
	dest[i] = '\0';
	return (src_len);
}
