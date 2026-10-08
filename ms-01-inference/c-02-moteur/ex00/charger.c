/*
 * charger.c - load the model file into one block of memory.
 *
 * File layout, little-endian:
 *   4 bytes    the magic "LMS1"
 *   5 int32    dim, tetes, vocab, seq_max, cache
 *   floats     the 12 tensors, one after the other, in a fixed order
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "moteur.h"

/* Read the magic and the 5 header ints into m. 1 if both read fine, 0 otherwise. */
static int	read_header(FILE *file, t_modele *m)
{
	char	magic[4];
	int		header[5];

	if (fread(magic, 1, 4, file) != 4)
		return (0);
	if (memcmp(magic, "LMS1", 4) != 0)
		return (0);
	if (fread(header, sizeof(int), 5, file) != 5)
		return (0);
	m->dim = header[0];
	m->tetes = header[1];
	m->vocab = header[2];
	m->seq_max = header[3];
	m->cache = header[4];
	return (1);
}

/* 1 if the five header numbers describe a usable model, 0 otherwise. */
static int	header_is_valid(const t_modele *m)
{
	if (m->dim <= 0 || m->tetes <= 0)
		return (0);
	if (m->vocab <= 0 || m->seq_max <= 0 || m->cache <= 0)
		return (0);
	if (m->dim % m->tetes != 0)
		return (0);
	return (1);
}

/* The number of floats in the 12 tensors, counted in file order, in size_t. */
static size_t	count_floats(const t_modele *m)
{
	size_t	dim;
	size_t	total;

	dim = (size_t)m->dim;
	total = 0;
	total += (size_t)m->vocab * dim;
	total += (size_t)m->seq_max * dim;
	total += dim;
	total += 4 * dim * dim;
	total += dim;
	total += 2 * (size_t)m->cache * dim;
	total += dim;
	total += (size_t)m->vocab * dim;
	return (total);
}

/* Return where the cursor points, then move it forward by `count` floats. */
static float	*take(float **cursor, size_t count)
{
	float	*start;

	start = *cursor;
	*cursor = *cursor + count;
	return (start);
}

/* Point each of the 12 tensors into the block, in file order. */
static void	place_tensors(t_modele *m)
{
	float	*cursor;
	size_t	dim;

	dim = (size_t)m->dim;
	cursor = m->bloc;
	m->tok_emb = take(&cursor, (size_t)m->vocab * dim);
	m->pos_emb = take(&cursor, (size_t)m->seq_max * dim);
	m->rms_att = take(&cursor, dim);
	m->wq = take(&cursor, dim * dim);
	m->wk = take(&cursor, dim * dim);
	m->wv = take(&cursor, dim * dim);
	m->wo = take(&cursor, dim * dim);
	m->rms_ffn = take(&cursor, dim);
	m->w1 = take(&cursor, (size_t)m->cache * dim);
	m->w2 = take(&cursor, dim * (size_t)m->cache);
	m->rms_final = take(&cursor, dim);
	m->wcls = take(&cursor, (size_t)m->vocab * dim);
}

int	charger(const char *chemin, t_modele *m)
{
	FILE	*file;
	size_t	count;

	memset(m, 0, sizeof(*m));
	file = fopen(chemin, "rb");
	if (file == NULL)
		return (-1);
	if (!read_header(file, m) || !header_is_valid(m))
	{
		fclose(file);
		return (-1);
	}
	count = count_floats(m);
	m->bloc = malloc(count * sizeof(float));
	if (m->bloc == NULL)
	{
		fclose(file);
		return (-1);
	}
	if (fread(m->bloc, sizeof(float), count, file) != count)
	{
		fclose(file);
		liberer(m);
		return (-1);
	}
	fclose(file);
	place_tensors(m);
	return (0);
}

/* Free the one block, then clear every field: a second call does nothing. */
void	liberer(t_modele *m)
{
	free(m->bloc);
	memset(m, 0, sizeof(*m));
}