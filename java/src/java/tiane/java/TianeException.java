package tiane.java;

/**
 * Wird geworfen, wenn TIANE wegen eines Fehlers beendet wurde.
 */
public class TianeException extends RuntimeException {

    public TianeException() {
        super();
    }

    public TianeException(String s) {
        super(s);
    }

    public TianeException(String s, Throwable throwable) {
        super(s, throwable);
    }

    public TianeException(Throwable throwable) {
        super(throwable);
    }

    protected TianeException(String s, Throwable throwable, boolean b, boolean b1) {
        super(s, throwable, b, b1);
    }
}
