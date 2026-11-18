/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:51:43 by mcoia             #+#    #+#             */
/*   Updated: 2026/10/12 21:51:43 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <unistd.h>
#include "ft_printf.h"

/*
 * Writes s in one write. A NULL s writes "(null)", like printf.
 * Returns: the bytes written, or -1 if write fails.
 */
static int	put_str(const char *s)
{
	int	len;

	if (!s)
		s = "(null)";
	len = 0;
	while (s[len])
		len++;
	return (write(1, s, len));
}

/*
** Writes u in the base the conversion c asks for, most significant digit
** first. The recursion reaches the leading digit before writing anything, so
** the prefix ("", "-" or "0x") is written there, just before it.
*/
static int	put_base(unsigned long u, char c, const char *prefix)
{
	char	digit;
	int		len;
	int		count;

	len = 10;
	if (c == 'x' || c == 'X' || c == 'p')
		len = 16;
	if (u >= (unsigned long)len)
		count = put_base(u / len, c, prefix);
	else
		count = put_str(prefix);
	digit = "0123456789abcdef"[u % len];
	if (c == 'X' && digit >= 'a')
		digit -= 'a' - 'A';
	if (count < 0 || write(1, &digit, 1) < 0)
		return (-1);
	return (count + 1);
}

/*
** d i u x X p. A negative int is widened to unsigned long, then negated in
** unsigned arithmetic, which is defined: INT_MIN needs no special case.
** A pointer is eight bytes, so it never goes through an unsigned int.
*/
static int	put_number(char c, va_list *ap)
{
	unsigned long	u;
	int				n;

	if (c == 'u' || c == 'x' || c == 'X')
		return (put_base(va_arg(*ap, unsigned int), c, ""));
	if (c == 'p')
	{
		u = (unsigned long)va_arg(*ap, void *);
		if (!u)
			return (put_str(PTR_NULL));
		return (put_base(u, c, "0x"));
	}
	n = va_arg(*ap, int);
	u = n;
	if (n >= 0)
		return (put_base(u, c, ""));
	return (put_base(-u, c, "-"));
}

/*
** Writes the next piece of the format, a plain character or a conversion,
** and moves past it. This is the dispatch table: the one place that maps a
** conversion character to what it writes. A '%' that ends the format writes
** nothing; an unknown conversion writes its letter alone.
*/
static int	step(const char **f, va_list *ap)
{
	char	c;

	c = **f;
	(*f)++;
	if (c != '%')
		return (write(1, &c, 1));
	c = **f;
	if (!c)
		return (0);
	(*f)++;
	if (c == 'c')
	{
		c = (char)va_arg(*ap, int);
		return (write(1, &c, 1));
	}
	if (c == 's')
		return (put_str(va_arg(*ap, char *)));
	if (c == 'd' || c == 'i' || c == 'u' || c == 'x' || c == 'X' || c == 'p')
		return (put_number(c, ap));
	return (write(1, &c, 1));
}

/*
 * Writes format to the standard output, each conversion replaced by the
 * next argument: c s p d i u x X and %.
 * Returns: the total bytes written, or -1 if format is NULL or a write
 *          fails.
 */
int	ft_printf(const char *format, ...)
{
	va_list	ap;
	int		count;
	int		n;

	if (!format)
		return (-1);
	va_start(ap, format);
	count = 0;
	n = 0;
	while (*format && n >= 0)
	{
		n = step(&format, &ap);
		count += n;
	}
	va_end(ap);
	if (n < 0)
		return (-1);
	return (count);
}
