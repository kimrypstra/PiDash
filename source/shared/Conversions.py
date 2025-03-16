# Conversions

CONVERSION_TEST = lambda can_frame: f'{can_frame.value:.1f}'
CONVERSION_POS_NEG = lambda can_frame: 'positive' if can_frame.value > 0 else 'negative'