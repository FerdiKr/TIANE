package tiane.java;

public class TIANEWrapper {

    public static native void startTiane(String runPy, String runDir, String[] dlopen);

    public static void printSomething(String toPrint) {
        System.out.println(toPrint);
    }
}
