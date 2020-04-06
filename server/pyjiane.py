try:
    import jiane
except ImportError:
    jiane = None
    '''Ignore. Methods should never be called when this is not a java start.'''

def javaPrint(text):
    jiane.javaPrint(text)