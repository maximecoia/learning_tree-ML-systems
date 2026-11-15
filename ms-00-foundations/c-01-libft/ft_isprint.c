/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isprint.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 08:20:40 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Is ch printable, ' ' = 32 to '~' = 126?
 * Returns: 1 if yes, 0 if no.
 * Edge:    127, DEL, is a control character: 0.
 */
int	ft_isprint(int ch)
{
	return (ch >= 32 && ch <= 126);
}
