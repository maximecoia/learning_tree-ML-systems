/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/05 11:12:42 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Counts the characters n needs: its digits, plus 1 for '-' or for 0.
 */
static size_t	count_digits(long n)
{
	size_t	digits;

	digits = (n <= 0);
	while (n)
	{
		n /= 10;
		digits++;
	}
	return (digits);
}

/*
 * Writes n in decimal into a new string, from malloc.
 * Returns: the string, or NULL when malloc fails.
 * How:     count the characters, malloc, fill the digits from the end.
 * Edge:    n goes in a long, so -2147483648 can be negated. 0 gives "0".
 */
char	*ft_itoa(int n)
{
	char	*result;
	size_t	digits;
	long	value;

	value = n;
	digits = count_digits(value);
	result = malloc(digits + 1);
	if (!result)
		return (NULL);
	result[digits] = '\0';
	if (value < 0)
	{
		result[0] = '-';
		value = -value;
	}
	if (value == 0)
		result[0] = '0';
	while (value > 0)
	{
		digits--;
		result[digits] = '0' + value % 10;
		value /= 10;
	}
	return (result);
}
