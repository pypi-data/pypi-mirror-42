from jellyfish import jaro_winkler


def _string_distance_score(s1, s2, method='jw'):
	if method.lower() in ['jw', 'jaro winkler']:
		return jaro_winkler(s1=s1, s2=s2)
	else:
		return 0


