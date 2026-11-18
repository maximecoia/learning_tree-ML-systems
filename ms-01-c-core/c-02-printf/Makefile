# Makefile - the last step: builds libftprintf.a.
#
# make reads this file and builds libftprintf.a for you. The subject asks
# for five rules, $(NAME), all, clean, fclean and re; for every cc line
# with -Wall -Wextra -Werror; for an archive made with ar, never libtool;
# and for no relink: a second make, with nothing changed, rebuilds nothing.
#
# Grade the hand-in, from pratique/c-03-printf:
#   ./corriger
NAME	= libftprintf.a
CC		= cc
CFLAGS	= -Wall -Wextra -Werror

SRCS	= ft_printf.c
OBJS	= $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)

%.o: %.c ft_printf.h
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
