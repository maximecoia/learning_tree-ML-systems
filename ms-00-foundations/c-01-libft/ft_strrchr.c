/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 10:47:55 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Looks for the last (char)target in text.
 * Returns: its address, or NULL.
 * Edge:    target '\0' gives the address of the final '\0'.
 */
char	*ft_strrchr(const char *text, int target)
{
	const char	*last;

	last = NULL;
	while (*text)
	{
		if (*text == (char)target)
			last = text;
		text++;
	}
	if ((char)target == '\0')
		return ((char *)text);
	return ((char *)last);
}
