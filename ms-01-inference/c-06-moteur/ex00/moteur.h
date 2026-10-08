#ifndef MOTEUR_H
# define MOTEUR_H

/* size_t, the type of every size and count in memory */
# include <stddef.h>

/*
 * The model, as loaded from the weight file.
 *
 * The five ints are the file header, in file order. `bloc` is the only
 * pointer that comes from malloc: it holds every weight. The twelve tensor
 * pointers all point INSIDE that block, so freeing `bloc` frees everything.
 * The field names are imposed: the grader reads them by name.
 */
typedef struct s_modele
{
	int		dim;
	int		tetes;
	int		vocab;
	int		seq_max;
	int		cache;
	float	*bloc;
	float	*tok_emb;
	float	*pos_emb;
	float	*rms_att;
	float	*wq;
	float	*wk;
	float	*wv;
	float	*wo;
	float	*rms_ffn;
	float	*w1;
	float	*w2;
	float	*rms_final;
	float	*wcls;
}	t_modele;

/* ex00: 0 on success, -1 if the file is refused; nothing is left allocated */
int		charger(const char *chemin, t_modele *m);
void	liberer(t_modele *m);

/* The vocabulary: one string per symbol, the index is the line number. */
typedef struct s_tokenizer
{
	int		taille;
	char	**symboles;
}	t_tokenizer;

/* ex01 */
int		charger_vocabulaire(const char *chemin, t_tokenizer *t);
void	liberer_vocabulaire(t_tokenizer *t);
int		encoder(const t_tokenizer *t, const char *texte, int *sortie, int max);
int		decoder(const t_tokenizer *t, const int *jetons, int n, char *sortie, int max);

/* ex02 */
void	matmul(const float *W, const float *x, float *sortie, int m, int n);
void	rmsnorm(const float *x, const float *gain, float *sortie, int n);
void	softmax(float *x, int n);

/* The state of one generation: the key-value cache and the current position. */
typedef struct s_etat
{
	float	*cache_k;
	float	*cache_v;
	int		position;
}	t_etat;

/* ex03 */
int		etat_creer(const t_modele *m, t_etat *e);
void	etat_liberer(t_etat *e);
void	logits(const t_modele *m, t_etat *e, int jeton, int position, float *sortie);

/* ex04 */
int		generer(const t_modele *m, const int *amorce, int n, int combien,
			int *sortie, float temperature, unsigned int graine);

/* ex05 */
double	mesurer_debit(const t_modele *m, int jetons, int rechauffement);

/* ex06 */
double	flops_par_jeton(const t_modele *m);
double	octets_par_jeton(const t_modele *m);
double	intensite_arithmetique(const t_modele *m);
double	bande_passante_mesuree(void);

#endif