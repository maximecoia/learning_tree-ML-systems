/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.h                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/21 13:15:26 by mcoia             #+#    #+#             */
/*   Updated: 2026/10/21 13:15:26 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

/*
 * get_next_line.h: what the two .c files share.
 *
 * #ifndef, #define and #endif around the whole file: the header guard. A
 * second #include of this file in the same .c then adds nothing.
 * <stdlib.h> declares malloc, free and size_t; <unistd.h> declares read and
 * ssize_t.
 * BUFFER_SIZE, the number of bytes asked of each read, comes from the
 * compiler, -D BUFFER_SIZE=n. The #ifndef below gives it a value only when
 * the compiler did not: without it, a -D would define it twice, and -Werror
 * turns that warning into an error. Never define BUFFER_SIZE in a .c.
 * Then the four functions the other files share: get_next_line, the one
 * the subject asks for, and the three helpers of get_next_line_utils.c.
 * The helpers start with gnl_, so they never clash with a function of the
 * program that uses yours, ft_strlen from a libft say.
 */
#ifndef GET_NEXT_LINE_H
# define GET_NEXT_LINE_H

# include <stdlib.h>
# include <unistd.h>

# ifndef BUFFER_SIZE
#  define BUFFER_SIZE 42
# endif

char	*get_next_line(int fd);
size_t	gnl_strlen(const char *s);
int		gnl_has_newline(const char *s);
char	*gnl_join(char *old, const char *add, size_t n);

#endif
