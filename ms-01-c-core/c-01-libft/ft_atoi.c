/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/03 15:32:53 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Converts the start of text to an int.
 * Returns: the number, or 0 when there is no digit.
 * How:     skip spaces, codes 9 to 13 and 32; one optional '+' or '-';
 *          then digits until the first non digit. Computed in a long.
 * Edge:    "+-5" gives 0. "  -42abc" gives -42.
 */
int	ft_atoi(const char *text)
{
	long	result;
	int		sign;

	result = 0;
	sign = 1;
	while (*text == ' ' || (*text >= 9 && *text <= 13))
		text++;
	if (*text == '-' || *text == '+')
	{
		if (*text == '-')
			sign = -1;
		text++;
	}
	while (ft_isdigit(*text))
	{
		result = result * 10 + (*text - '0');
		text++;
	}
	return ((int)(result * sign));
}
