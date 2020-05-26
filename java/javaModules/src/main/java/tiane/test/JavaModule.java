package tiane.test;

import tiane.java.api.LocalStorage;
import tiane.java.api.Module;
import tiane.java.api.ModuleWrapper;

import javax.annotation.Nonnull;

public class JavaModule implements Module {

    @Override
    @Nonnull
    public String name() {
        return "jiane_javatest";
    }

    @Override
    public int priority() {
        return -1;
    }

    @Override
    public boolean isValid(@Nonnull String text) {
        return text.toLowerCase().contains("kannst du java");
    }

    @Override
    public void handle(@Nonnull String text, @Nonnull ModuleWrapper tiane, @Nonnull LocalStorage localStorage) {
        tiane.say("Ja, natürlich.");
    }
}
