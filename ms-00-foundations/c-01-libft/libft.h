/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   libft.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mcoia <maxime.coia@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/10/12 21:37:50 by mcoia             #+#    #+#             */
/*   Updated: 2026/10/12 21:37:50 by mcoia            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef LIBFT_H
# define LIBFT_H

# include <stddef.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_list
{
	void			*content;
	struct s_list	*next;
}	t_list;

int				ft_isalpha(int ch);
int				ft_isdigit(int ch);
int				ft_isalnum(int ch);
int				ft_isascii(int ch);
int				ft_isprint(int ch);
int				ft_toupper(int ch);
int				ft_tolower(int ch);

size_t			ft_strlen(const char *text);
void			*ft_memset(void *area, int value, size_t bytes);
void			ft_bzero(void *area, size_t bytes);
void			*ft_memcpy(void *dest, const void *source, size_t bytes);
void			*ft_memmove(void *dest, const void *source, size_t bytes);
void			*ft_memchr(const void *area, int target, size_t bytes);
int				ft_memcmp(const void *first, const void *second,
					size_t bytes);
void			*ft_calloc(size_t count, size_t elem_size);

size_t			ft_strlcpy(char *dest, const char *source, size_t dest_size);
size_t			ft_strlcat(char *dest, const char *source, size_t dest_size);
char			*ft_strchr(const char *text, int target);
char			*ft_strrchr(const char *text, int target);
int				ft_strncmp(const char *first, const char *second,
					size_t limit);
char			*ft_strnstr(const char *text, const char *word, size_t limit);
int				ft_atoi(const char *text);
char			*ft_strdup(const char *text);

char			*ft_substr(char const *s, unsigned int start, size_t len);
char			*ft_strjoin(char const *s1, char const *s2);
char			*ft_strtrim(char const *s1, char const *set);
char			**ft_split(char const *s, char c);
char			*ft_itoa(int n);
char			*ft_strmapi(char const *s, char (*f)(unsigned int, char));
void			ft_striteri(char *s, void (*f)(unsigned int, char *));
void			ft_putchar_fd(char c, int fd);
void			ft_putstr_fd(char *s, int fd);
void			ft_putendl_fd(char *s, int fd);
void			ft_putnbr_fd(int n, int fd);

t_list			*ft_lstnew(void *content);
void			ft_lstadd_front(t_list **lst, t_list *new);
unsigned int	ft_lstsize(t_list *lst);
t_list			*ft_lstlast(t_list *lst);
void			ft_lstadd_back(t_list **lst, t_list *new);
void			ft_lstdelone(t_list *lst, void (*del)(void *));
void			ft_lstclear(t_list **lst, void (*del)(void *));
void			ft_lstiter(t_list *lst, void (*f)(void *));
t_list			*ft_lstmap(t_list *lst, void *(*f)(void *),
					void (*del)(void *));

#endif
