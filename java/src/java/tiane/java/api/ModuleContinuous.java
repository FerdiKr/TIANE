package tiane.java.api;

public interface ModuleContinuous {

    String name();

    default int priority() { return 0; }
    int intervall();

    default void start(ModuleWrapperContinuous tiane, LocalStorage localStorage) {}
    void run(ModuleWrapperContinuous tiane, LocalStorage localStorage);
    default void stop(ModuleWrapperContinuous tiane, LocalStorage localStorage) {}
}
