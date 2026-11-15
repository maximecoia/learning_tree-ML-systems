/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 10:44:15 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Looks for the first (char)target in text.
 * Returns: its address, or NULL.
 * Edge:    target '\0' gives the address of the final '\0'.
 *          target is cast to char: 'a' + 256 finds 'a'.
 */
char	*ft_strchr(const char *text, int target)
{
	while (*text)
	{
		if (*text == (char)target)
			return ((char *)text);
		text++;
	}
	if ((char)target == '\0')
		return ((char *)text);
	return (NULL);
}
