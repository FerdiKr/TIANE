package tiane.java.api;

public interface Module {

    String name();

    default int priority() { return 0; }
    default String[] words() { return new String[]{}; }

    boolean isValid(String text);
    default boolean isValidTelegram(String text) { return false; }
    boolean handle(String text, ModuleWrapper tiane, LocalStorage localStorage);
}
