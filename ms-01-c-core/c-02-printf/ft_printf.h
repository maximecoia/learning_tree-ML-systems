/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:51:43 by mcoia             #+#    #+#             */
/*   Updated: 2026/10/12 21:51:43 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdarg.h>

/*
** What %p prints for a null pointer is left to each libc: glibc prints
** "(nil)", the libc of macOS and the BSDs prints "0x0". The reference is the
** libc of the machine that grades.
*/
# ifdef __linux__
#  define PTR_NULL "(nil)"
# else
#  define PTR_NULL "0x0"
# endif

int	ft_printf(const char *format, ...);

#endif
