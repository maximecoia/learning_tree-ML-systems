/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlen.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 09:57:30 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Counts the characters of text before its '\0'.
 * Returns: that count. "" gives 0, "bonjour" gives 7.
 * Edge:    text NULL crashes, like the libc strlen.
 */
size_t	ft_strlen(const char *text)
{
	size_t	i;

	i = 0;
	while (text[i])
		i++;
	return (i);
}
