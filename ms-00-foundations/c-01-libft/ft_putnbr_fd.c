/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/11/05 13:06:45 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

/*
 * Writes n in decimal on the file descriptor fd.
 * How:     write n / 10 first, by recursion, then the last digit.
 * Edge:    n goes in a long, so -2147483648 can be negated.
 */
void	ft_putnbr_fd(int n, int fd)
{
	long	value;
	char	digit;

	value = n;
	if (value < 0)
	{
		ft_putchar_fd('-', fd);
		value = -value;
	}
	if (value >= 10)
		ft_putnbr_fd((int)(value / 10), fd);
	digit = '0' + value % 10;
	ft_putchar_fd(digit, fd);
}
